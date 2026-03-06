"""HRM Executor — Low-level task execution via Ollama local models.

Takes plan steps from the Planner and executes them using
the echo_log Voice Gateway tools via HTTP.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx
from pydantic import BaseModel

from .planner import Plan, PlanStep

logger = logging.getLogger(__name__)


class StepResult(BaseModel):
    step_id: int
    success: bool
    output: Any = None
    error: str | None = None
    duration_ms: float = 0.0
    model_used: str = ""


class ExecutionResult(BaseModel):
    task_id: str
    success: bool
    step_results: list[StepResult]
    total_duration_ms: float
    steps_completed: int
    steps_failed: int
    needs_escalation: bool = False
    escalation_reason: str | None = None


class Executor:
    """Executes plan steps via echo_log Voice Gateway."""

    def __init__(
        self,
        echoLog_url: str = "http://10.40.10.82:8085",
        ollama_url: str = "http://10.40.10.90:11434",
        default_model: str = "mistral-small3.2",
        fallback_models: list[str] | None = None,
        timeout: float = 60.0,
        max_retries: int = 2,
    ):
        self.echoLog_url = echoLog_url.rstrip("/")
        self.ollama_url = ollama_url.rstrip("/")
        self.default_model = default_model
        self.fallback_models = fallback_models or ["llama3.1:8b"]
        self.timeout = timeout
        self.max_retries = max_retries

    async def execute_plan(
        self,
        plan: Plan,
        session_id: str = "hrm-executor",
        nss_client: Any = None,
    ) -> ExecutionResult:
        """Execute all steps in a plan sequentially, respecting dependencies."""
        start = time.time()
        results: list[StepResult] = []
        completed_steps: set[int] = set()
        failed = 0

        for step in plan.steps:
            # Check dependencies
            if step.depends_on:
                unmet = [d for d in step.depends_on if d not in completed_steps]
                if unmet:
                    results.append(StepResult(
                        step_id=step.step_id,
                        success=False,
                        error=f"Unmet dependencies: {unmet}",
                    ))
                    failed += 1
                    continue

            # NSS security check before execution
            if nss_client:
                risk = await nss_client.check_risk(step.description)
                if risk and risk.get("tier", 3) <= 1:
                    results.append(StepResult(
                        step_id=step.step_id,
                        success=False,
                        error=f"Blocked by NSS: risk tier {risk.get('tier')} ({risk.get('category', 'unknown')})",
                    ))
                    failed += 1
                    continue

            result = await self._execute_step(step, session_id)
            results.append(result)

            if result.success:
                completed_steps.add(step.step_id)
            else:
                failed += 1
                # If a critical step fails, check if we should escalate
                if step.estimated_complexity in ("medium", "high"):
                    total_ms = (time.time() - start) * 1000
                    return ExecutionResult(
                        task_id=plan.task_id,
                        success=False,
                        step_results=results,
                        total_duration_ms=total_ms,
                        steps_completed=len(completed_steps),
                        steps_failed=failed,
                        needs_escalation=True,
                        escalation_reason=f"Step {step.step_id} failed: {result.error}",
                    )

        total_ms = (time.time() - start) * 1000
        return ExecutionResult(
            task_id=plan.task_id,
            success=failed == 0,
            step_results=results,
            total_duration_ms=total_ms,
            steps_completed=len(completed_steps),
            steps_failed=failed,
        )

    async def _execute_step(self, step: PlanStep, session_id: str) -> StepResult:
        """Execute a single step, trying fallback models on failure."""
        models_to_try = [self.default_model] + self.fallback_models
        last_error = ""

        for model in models_to_try:
            start = time.time()
            try:
                if step.tool:
                    output = await self._call_tool(step, session_id)
                else:
                    output = await self._call_chat(step, model, session_id)

                duration = (time.time() - start) * 1000
                return StepResult(
                    step_id=step.step_id,
                    success=True,
                    output=output,
                    duration_ms=duration,
                    model_used=model,
                )
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Step {step.step_id} failed with {model}: {e}")
                continue

        return StepResult(
            step_id=step.step_id,
            success=False,
            error=f"All models failed. Last error: {last_error}",
        )

    async def _call_tool(self, step: PlanStep, session_id: str) -> Any:
        """Execute a tool via echo_log Voice Gateway."""
        payload = {
            "message": f"Execute tool: {step.tool} with args: {step.tool_args}",
            "session_id": session_id,
            "use_tools": True,
            "use_context": False,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{self.echoLog_url}/chat", json=payload)
            resp.raise_for_status()
            return resp.json()

    async def _call_chat(self, step: PlanStep, model: str, session_id: str) -> Any:
        """Execute a reasoning step via Ollama directly."""
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Execute the following task step precisely. Respond with the result only."},
                {"role": "user", "content": step.description},
            ],
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 2048},
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{self.ollama_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "")
