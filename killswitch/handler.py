"""Killswitch Handler — Core kill logic with audit trail."""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class KillReason(str, Enum):
    TERMINAL = "terminal"       # Ctrl+K
    MATTERMOST = "mattermost"   # /killswitch command
    API = "api"                 # REST endpoint
    TOOL = "tool"               # stop_agent tool
    TIMEOUT = "timeout"         # Max execution time
    NSS_BLOCK = "nss_block"     # NSS SHIELD blocked


class KillEvent(BaseModel):
    agent_name: str
    reason: KillReason
    triggered_by: str
    timestamp: float
    details: str = ""
    hash: str = ""  # SHA-256 for audit chain


class KillswitchHandler:
    """Manages agent termination with audit logging."""

    def __init__(
        self,
        agent_name: str,
        authorized_users: list[str] | None = None,
        audit_log_path: str = "killswitch_audit.log",
    ):
        self.agent_name = agent_name
        self.authorized_users = authorized_users or ["joe"]
        self.audit_log_path = Path(audit_log_path)
        self._active_tasks: dict[str, asyncio.Task] = {}
        self._killed = False
        self._kill_callbacks: list[Any] = []
        self._last_hash = ""

    @property
    def is_killed(self) -> bool:
        return self._killed

    def on_kill(self, callback):
        """Register a callback for kill events."""
        self._kill_callbacks.append(callback)

    async def kill(
        self,
        reason: KillReason,
        triggered_by: str,
        details: str = "",
    ) -> KillEvent:
        """Execute killswitch — stop all agent activity."""
        # Authorization check
        if triggered_by not in self.authorized_users:
            logger.warning(f"Unauthorized kill attempt by {triggered_by}")
            raise PermissionError(f"User {triggered_by} not authorized for killswitch")

        self._killed = True

        # Cancel all active tasks
        cancelled = 0
        for task_id, task in list(self._active_tasks.items()):
            if not task.done():
                task.cancel()
                cancelled += 1
                logger.info(f"Cancelled task: {task_id}")

        # Create audit event
        event = KillEvent(
            agent_name=self.agent_name,
            reason=reason,
            triggered_by=triggered_by,
            timestamp=time.time(),
            details=f"{details} (cancelled {cancelled} tasks)",
        )

        # SHA-256 hash chain for tamper-evident audit
        chain_data = f"{self._last_hash}{event.model_dump_json()}"
        event.hash = hashlib.sha256(chain_data.encode()).hexdigest()
        self._last_hash = event.hash

        # Write audit log
        await self._write_audit(event)

        # Notify callbacks
        for cb in self._kill_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(event)
                else:
                    cb(event)
            except Exception as e:
                logger.error(f"Kill callback error: {e}")

        logger.warning(f"KILLSWITCH ACTIVATED for {self.agent_name} by {triggered_by} ({reason.value})")
        return event

    async def revive(self, authorized_by: str):
        """Re-enable the agent after killswitch."""
        if authorized_by not in self.authorized_users:
            raise PermissionError(f"User {authorized_by} not authorized")

        self._killed = False
        logger.info(f"Agent {self.agent_name} revived by {authorized_by}")

    def register_task(self, task_id: str, task: asyncio.Task):
        """Register an active task for potential cancellation."""
        self._active_tasks[task_id] = task
        task.add_done_callback(lambda _: self._active_tasks.pop(task_id, None))

    def check_alive(self) -> bool:
        """Check if agent is allowed to continue. Call before each operation."""
        if self._killed:
            raise RuntimeError(f"Agent {self.agent_name} is killed. Use revive() to restart.")
        return True

    async def _write_audit(self, event: KillEvent):
        """Append kill event to audit log."""
        try:
            self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(event.model_dump_json() + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
