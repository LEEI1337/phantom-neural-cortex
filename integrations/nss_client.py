"""HTTP client for NSS (Neural Security System) microservices.

Connects to:
- Cognitive Gateway (:11337) — PII redaction, STEER, PNC compression
- Guardian Shield  (:11338) — MARS, SENTINEL, VIGIL, SHIELD, APEX
- Governance Plane (:11339) — Policy Engine, Privacy Budget, DPIA
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class RiskCheckResult(BaseModel):
    score: float
    tier: int  # 0=CRITICAL, 1=HIGH, 2=MEDIUM, 3=LOW
    category: str
    details: str
    blocked: bool = False


class SentinelResult(BaseModel):
    is_injection: bool
    confidence: float
    pattern: str | None = None


class PIIRedactionResult(BaseModel):
    redacted_text: str
    entities_found: int
    entity_types: list[str]


class NSSClient:
    """Unified client for all NSS security services."""

    def __init__(
        self,
        gateway_url: str = "http://localhost:11337",
        guardian_url: str = "http://localhost:11338",
        governance_url: str = "http://localhost:11339",
        timeout: float = 30.0,
        auth_token: str | None = None,
    ):
        self.gateway_url = gateway_url.rstrip("/")
        self.guardian_url = guardian_url.rstrip("/")
        self.governance_url = governance_url.rstrip("/")
        self.timeout = timeout
        self._headers = {}
        if auth_token:
            self._headers["Authorization"] = f"Bearer {auth_token}"

    # -- Guardian Shield (:11338) --

    async def check_risk(self, text: str, language: str = "de") -> RiskCheckResult:
        """MARS risk scoring for a text input."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.guardian_url}/mars/score",
                    json={"text": text, "language": language},
                    headers=self._headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return RiskCheckResult(
                    score=data["score"],
                    tier=data["tier"],
                    category=data.get("category", "unknown"),
                    details=data.get("details", ""),
                    blocked=data["tier"] <= 1,
                )
        except httpx.ConnectError:
            logger.warning("NSS Guardian not reachable, defaulting to SAFE")
            return RiskCheckResult(score=0.0, tier=3, category="unavailable", details="NSS offline")
        except Exception as e:
            logger.error(f"MARS risk check failed: {e}")
            return RiskCheckResult(score=0.0, tier=3, category="error", details=str(e))

    async def check_injection(self, text: str) -> SentinelResult:
        """SENTINEL injection defense check."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.guardian_url}/sentinel/check",
                    json={"text": text},
                    headers=self._headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return SentinelResult(**data)
        except httpx.ConnectError:
            logger.warning("NSS Sentinel not reachable")
            return SentinelResult(is_injection=False, confidence=0.0)
        except Exception as e:
            logger.error(f"SENTINEL check failed: {e}")
            return SentinelResult(is_injection=False, confidence=0.0)

    async def check_tool_safety(self, tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
        """VIGIL tool safety check (CIA classification)."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.guardian_url}/vigil/check",
                    json={"tool_name": tool_name, "args": tool_args},
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"VIGIL check failed: {e}")
            return {"safe": True, "reason": "VIGIL offline, defaulting to safe"}

    async def enhance_prompt(self, prompt: str) -> str:
        """SHIELD prompt enhancement for safety."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.guardian_url}/shield/enhance",
                    json={"prompt": prompt},
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json().get("enhanced_prompt", prompt)
        except Exception as e:
            logger.error(f"SHIELD enhance failed: {e}")
            return prompt

    # -- Cognitive Gateway (:11337) --

    async def redact_pii(self, text: str) -> PIIRedactionResult:
        """Redact PII from text via Cognitive Gateway."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.gateway_url}/pii/redact",
                    json={"text": text},
                    headers=self._headers,
                )
                resp.raise_for_status()
                data = resp.json()
                return PIIRedactionResult(**data)
        except Exception as e:
            logger.error(f"PII redaction failed: {e}")
            return PIIRedactionResult(redacted_text=text, entities_found=0, entity_types=[])

    # -- Governance Plane (:11339) --

    async def check_privacy_budget(self, operation: str, data_subject: str) -> dict[str, Any]:
        """Check if privacy budget allows this operation."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.governance_url}/privacy/budget/check",
                    json={"operation": operation, "data_subject": data_subject},
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Privacy budget check failed: {e}")
            return {"allowed": True, "reason": "Governance offline"}

    async def check_policy(self, action: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Check action against policy engine."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.governance_url}/policy/check",
                    json={"action": action, "context": context or {}},
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error(f"Policy check failed: {e}")
            return {"allowed": True, "reason": "Policy engine offline"}

    # -- Health --

    async def health(self) -> dict[str, str]:
        """Check health of all NSS services."""
        results = {}
        for name, url in [
            ("gateway", self.gateway_url),
            ("guardian", self.guardian_url),
            ("governance", self.governance_url),
        ]:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    resp = await client.get(f"{url}/health")
                    results[name] = "OK" if resp.status_code == 200 else f"ERROR ({resp.status_code})"
            except Exception:
                results[name] = "OFFLINE"
        return results
