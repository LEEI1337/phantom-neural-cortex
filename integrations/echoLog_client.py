"""HTTP client for echo_log Voice Gateway (:8085).

Provides access to:
- Chat API (with optional tools + RAG)
- Tool execution
- Memory management
- Health/status
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ChatResponse(BaseModel):
    response: str
    tool_results: list[dict[str, Any]] | None = None
    session_id: str = ""
    tokens_used: int = 0


class EchoLogClient:
    """Client for echo_log Voice Gateway REST API."""

    def __init__(
        self,
        base_url: str = "http://10.40.10.82:8085",
        api_key: str | None = None,
        timeout: float = 60.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._headers = {"Content-Type": "application/json"}
        if api_key:
            self._headers["X-API-Key"] = api_key

    async def chat(
        self,
        message: str,
        session_id: str = "pnc-agent",
        use_tools: bool = True,
        use_context: bool = True,
        memory_scope: str = "session",
    ) -> ChatResponse:
        """Send a chat message to echo_log."""
        payload = {
            "message": message,
            "session_id": session_id,
            "use_tools": use_tools,
            "use_context": use_context,
            "memory_scope": memory_scope,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/chat",
                    json=payload,
                    headers=self._headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return ChatResponse(
                    response=data.get("response", ""),
                    tool_results=data.get("tool_results"),
                    session_id=data.get("session_id", session_id),
                    tokens_used=data.get("tokens_used", 0),
                )
        except Exception as e:
            logger.error(f"echo_log chat failed: {e}")
            raise

    async def execute_tool(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
        session_id: str = "pnc-agent",
    ) -> dict[str, Any]:
        """Execute a specific tool via echo_log's chat interface."""
        message = f"[TOOL_CALL] {tool_name}({tool_args})"
        response = await self.chat(
            message=message,
            session_id=session_id,
            use_tools=True,
            use_context=False,
        )
        return {
            "tool_name": tool_name,
            "response": response.response,
            "tool_results": response.tool_results,
        }

    async def get_tools(self) -> list[dict[str, Any]]:
        """List available tools from echo_log."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(
                    f"{self.base_url}/tools",
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json().get("tools", [])
        except Exception as e:
            logger.error(f"Failed to list echo_log tools: {e}")
            return []

    async def memory_store(
        self,
        key: str,
        value: Any,
        memory_type: str = "semantic",
        ttl: int | None = None,
    ) -> bool:
        """Store data in echo_log's memory system."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/memory/store",
                    json={"key": key, "value": value, "type": memory_type, "ttl": ttl},
                    headers=self._headers,
                )
                resp.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Memory store failed: {e}")
            return False

    async def memory_recall(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Recall memories from echo_log's RAG system."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/memory/recall",
                    json={"query": query, "limit": limit},
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json().get("results", [])
        except Exception as e:
            logger.error(f"Memory recall failed: {e}")
            return []

    async def health(self) -> dict[str, Any]:
        """Check echo_log health."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(
                    f"{self.base_url}/health",
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            return {"status": "offline", "error": str(e)}

    async def status(self) -> dict[str, Any]:
        """Get detailed echo_log status."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{self.base_url}/status",
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            return {"status": "offline", "error": str(e)}
