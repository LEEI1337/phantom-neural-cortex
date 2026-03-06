"""PhantomAgent — The unified AI employee.

Integrates PNC (orchestration), NSS (security), echo_log (tools),
and Mattermost (communication) into a single deployable agent.
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Any

from config.schema import AgentConfig
from hrm.router import HRMRouter, ComplexityLevel
from hrm.planner import Planner
from hrm.executor import Executor, ExecutionResult
from integrations.nss_client import NSSClient
from integrations.echoLog_client import EchoLogClient
from integrations.mm_bridge import MattermostBridge
from killswitch.handler import KillswitchHandler, KillReason
from killswitch.api import register_handler

logger = logging.getLogger(__name__)


class PhantomAgent:
    """A fully configured AI agent instance.

    Lifecycle:
        agent = PhantomAgent.from_config("config/templates/lisa01.yaml")
        await agent.start()
        result = await agent.handle_task("Deploy new container")
        await agent.stop()
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.role = config.role

        # HRM — Hierarchical Reasoning
        self.hrm_router = HRMRouter(
            planner_model=config.llm.planner,
            executor_model=config.llm.executor,
            fallback_models=config.llm.fallback,
            local_only=config.llm.local_only,
        )
        self.planner = Planner(
            ollama_url=config.llm.ollama_url,
            default_model=config.llm.planner,
        )
        self.executor = Executor(
            echoLog_url=config.echoLog_url,
            ollama_url=config.llm.ollama_url,
            default_model=config.llm.executor,
            fallback_models=config.llm.fallback,
        )

        # NSS Security
        self.nss: NSSClient | None = None
        if config.security.nss_enabled:
            self.nss = NSSClient(
                gateway_url=config.security.nss_gateway_url,
                guardian_url=config.security.nss_guardian_url,
                governance_url=config.security.nss_governance_url,
            )

        # echo_log tools
        self.echoLog = EchoLogClient(base_url=config.echoLog_url)

        # Mattermost
        self.mm_bridge: MattermostBridge | None = None

        # Killswitch
        self.killswitch = KillswitchHandler(
            agent_name=config.name,
            authorized_users=config.security.killswitch_owners,
        )
        register_handler(config.name, self.killswitch)

        # State
        self._running = False
        self._task_count = 0

    @classmethod
    def from_config(cls, config_path: str) -> PhantomAgent:
        """Create agent from YAML config file."""
        config = AgentConfig.from_yaml(config_path)
        return cls(config)

    async def start(self):
        """Start the agent and all its subsystems."""
        logger.info(f"Starting agent {self.name} ({self.role})")

        # Start Mattermost bridge if configured
        mm_cfg = self.config.communication.mattermost
        if mm_cfg.token_vault_path:
            token = self._resolve_vault_token(mm_cfg.token_vault_path)
            if token:
                self.mm_bridge = MattermostBridge(
                    url=mm_cfg.url,
                    token=token,
                    bot_username=self.name,
                    channels=mm_cfg.channels,
                    home_channel=mm_cfg.home_channel,
                )
                self.mm_bridge.on_message(self._handle_mm_message)
                await self.mm_bridge.start()

        self._running = True

        # Announce
        if self.mm_bridge:
            await self.mm_bridge.send_to_home(
                f"Agent `{self.name}` online. Role: {self.role}. "
                f"Models: {self.config.llm.planner} (planner), {self.config.llm.executor} (executor)."
            )

        logger.info(f"Agent {self.name} started successfully")

    async def stop(self):
        """Stop the agent gracefully."""
        self._running = False

        if self.mm_bridge:
            await self.mm_bridge.send_to_home(f"Agent `{self.name}` shutting down.")
            await self.mm_bridge.stop()

        logger.info(f"Agent {self.name} stopped")

    async def handle_task(self, task_description: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Main entry point — handle a task using the HRM pipeline.

        1. Assess complexity
        2. NSS security check
        3. If complex → Plan with Cloud LLM → Execute steps locally
        4. If simple → Execute directly with Ollama
        5. Feedback loop on failure → escalate to planner
        """
        self.killswitch.check_alive()
        self._task_count += 1
        task_id = f"{self.name}-{self._task_count}-{uuid.uuid4().hex[:6]}"
        start_time = time.time()

        logger.info(f"[{task_id}] Handling task: {task_description[:80]}...")

        # 1. NSS pre-check
        if self.nss:
            injection = await self.nss.check_injection(task_description)
            if injection.is_injection:
                return {
                    "task_id": task_id,
                    "success": False,
                    "error": f"SENTINEL blocked: injection detected ({injection.confidence:.0%})",
                }

            risk = await self.nss.check_risk(task_description)
            if risk.blocked:
                return {
                    "task_id": task_id,
                    "success": False,
                    "error": f"MARS blocked: risk tier {risk.tier} ({risk.category})",
                }

        # 2. Assess complexity
        assessment = self.hrm_router.assess_complexity(task_description)
        logger.info(f"[{task_id}] Complexity: {assessment.level.value} ({assessment.score:.2f})")

        # 3. Route
        if assessment.requires_planner:
            result = await self._plan_and_execute(task_id, task_description, context)
        else:
            result = await self._direct_execute(task_id, task_description)

        duration = time.time() - start_time
        result["duration_s"] = round(duration, 2)
        result["complexity"] = assessment.model_dump()

        # 4. Notify via MM
        if self.mm_bridge:
            status = "OK" if result.get("success") else "FAILED"
            await self.mm_bridge.send_to_home(
                f"Task `{task_id}` {status} ({duration:.1f}s) — {task_description[:60]}"
            )

        return result

    async def _plan_and_execute(
        self, task_id: str, task_description: str, context: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Complex path: Plan → Execute → Feedback Loop."""
        # Create plan
        plan = await self.planner.create_plan(task_id, task_description, context=context)
        logger.info(f"[{task_id}] Plan created: {plan.total_steps} steps via {plan.planner_model}")

        # Execute plan
        exec_result = await self.executor.execute_plan(
            plan, session_id=task_id, nss_client=self.nss
        )

        # Feedback loop — if execution failed, try to refine the plan
        if exec_result.needs_escalation and exec_result.escalation_reason:
            logger.warning(f"[{task_id}] Escalating: {exec_result.escalation_reason}")

            refined_plan = await self.planner.refine_plan(
                plan, feedback=exec_result.escalation_reason
            )
            exec_result = await self.executor.execute_plan(
                refined_plan, session_id=task_id, nss_client=self.nss
            )

        return {
            "task_id": task_id,
            "success": exec_result.success,
            "steps_completed": exec_result.steps_completed,
            "steps_failed": exec_result.steps_failed,
            "total_duration_ms": exec_result.total_duration_ms,
            "step_results": [r.model_dump() for r in exec_result.step_results],
        }

    async def _direct_execute(self, task_id: str, task_description: str) -> dict[str, Any]:
        """Simple path: Direct execution via echo_log."""
        try:
            response = await self.echoLog.chat(
                message=task_description,
                session_id=task_id,
                use_tools=True,
            )
            return {
                "task_id": task_id,
                "success": True,
                "response": response.response,
                "tool_results": response.tool_results,
                "tokens_used": response.tokens_used,
            }
        except Exception as e:
            return {
                "task_id": task_id,
                "success": False,
                "error": str(e),
            }

    async def _handle_mm_message(self, post: dict[str, Any]):
        """Handle incoming Mattermost messages."""
        message = post.get("message", "")

        # Only respond to @mentions
        if f"@{self.name}" not in message:
            return

        # Strip mention
        clean_msg = message.replace(f"@{self.name}", "").strip()
        if not clean_msg:
            return

        # Handle the message as a task
        result = await self.handle_task(clean_msg)

        # Reply
        channel_id = post.get("channel_id", "")
        if channel_id and self.mm_bridge:
            response_text = result.get("response", "")
            if not response_text:
                if result.get("success"):
                    response_text = f"Task completed ({result.get('steps_completed', 0)} steps)."
                else:
                    response_text = f"Task failed: {result.get('error', 'unknown error')}"

            sender = post.get("user_id", "unknown")
            await self.mm_bridge.send_message(channel_id, f"@{sender} {response_text}")

    def _resolve_vault_token(self, vault_path: str) -> str:
        """Resolve a token from the vault. Returns empty string on failure."""
        try:
            import subprocess
            vault_script = "C:/Users/Legion/Documents/2026 Echo_log_local/phantom-ai/.claude/credentials/vault.py"
            parts = vault_path.split("/")
            if len(parts) >= 3:
                result = subprocess.run(
                    ["python", vault_script, "get", parts[0], parts[1], parts[2]],
                    capture_output=True, text=True, timeout=10,
                )
                return result.stdout.strip()
        except Exception as e:
            logger.warning(f"Vault resolve failed for {vault_path}: {e}")
        return ""
