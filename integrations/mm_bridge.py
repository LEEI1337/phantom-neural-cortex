"""Mattermost Bridge — WebSocket + REST integration.

Ported from Jak Bot's native_mm_bridge pattern.
Handles real-time message receiving and sending via Mattermost.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Callable, Coroutine

import httpx
import websockets

logger = logging.getLogger(__name__)

# Type alias for message handlers
MessageHandler = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class MattermostBridge:
    """WebSocket + REST bridge to Mattermost."""

    def __init__(
        self,
        url: str = "http://10.40.10.83:8065",
        token: str = "",
        bot_username: str = "phantom-agent",
        channels: list[str] | None = None,
        home_channel: str = "",
    ):
        self.url = url.rstrip("/")
        self.token = token
        self.bot_username = bot_username
        self.channels = channels or []
        self.home_channel = home_channel
        self._ws = None
        self._running = False
        self._handlers: list[MessageHandler] = []
        self._user_id: str = ""
        self._headers = {"Authorization": f"Bearer {self.token}"}

    def on_message(self, handler: MessageHandler):
        """Register a message handler."""
        self._handlers.append(handler)

    async def start(self):
        """Connect to Mattermost WebSocket and start listening."""
        # Get bot user ID
        self._user_id = await self._get_user_id()
        if not self._user_id:
            logger.error("Failed to get bot user ID")
            return

        self._running = True
        asyncio.create_task(self._ws_loop())
        logger.info(f"Mattermost bridge started as {self.bot_username}")

    async def stop(self):
        """Disconnect from Mattermost."""
        self._running = False
        if self._ws:
            await self._ws.close()
        logger.info("Mattermost bridge stopped")

    async def send_message(self, channel_id: str, message: str) -> dict[str, Any] | None:
        """Send a message to a Mattermost channel."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{self.url}/api/v4/posts",
                    json={"channel_id": channel_id, "message": message},
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Failed to send MM message: {e}")
            return None

    async def send_to_home(self, message: str) -> dict[str, Any] | None:
        """Send a message to the home channel."""
        if not self.home_channel:
            logger.warning("No home channel configured")
            return None
        return await self.send_message(self.home_channel, message)

    async def _get_user_id(self) -> str:
        """Get the bot's user ID from Mattermost."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{self.url}/api/v4/users/me",
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json().get("id", "")
        except Exception as e:
            logger.error(f"Failed to get user ID: {e}")
            return ""

    async def _ws_loop(self):
        """WebSocket reconnection loop (Jak Bot pattern)."""
        ws_url = self.url.replace("http://", "ws://").replace("https://", "wss://")
        ws_url = f"{ws_url}/api/v4/websocket"

        while self._running:
            try:
                extra_headers = {"Authorization": f"Bearer {self.token}"}
                async with websockets.connect(ws_url, extra_headers=extra_headers) as ws:
                    self._ws = ws
                    logger.info("WebSocket connected to Mattermost")

                    # Auth challenge
                    auth_msg = json.dumps({
                        "seq": 1,
                        "action": "authentication_challenge",
                        "data": {"token": self.token},
                    })
                    await ws.send(auth_msg)

                    async for raw_msg in ws:
                        try:
                            event = json.loads(raw_msg)
                            await self._handle_event(event)
                        except json.JSONDecodeError:
                            continue

            except websockets.ConnectionClosed:
                logger.warning("MM WebSocket closed, reconnecting in 5s...")
            except Exception as e:
                logger.error(f"MM WebSocket error: {e}, reconnecting in 5s...")

            if self._running:
                await asyncio.sleep(5)

    async def _handle_event(self, event: dict[str, Any]):
        """Process a WebSocket event."""
        event_type = event.get("event")
        if event_type != "posted":
            return

        data = event.get("data", {})
        post_str = data.get("post", "{}")
        try:
            post = json.loads(post_str)
        except json.JSONDecodeError:
            return

        # Ignore own messages
        if post.get("user_id") == self._user_id:
            return

        # Check if it's in a monitored channel
        channel_id = post.get("channel_id", "")
        if self.channels and channel_id not in self.channels:
            return

        # Dispatch to handlers
        for handler in self._handlers:
            try:
                await handler(post)
            except Exception as e:
                logger.error(f"Message handler error: {e}")
