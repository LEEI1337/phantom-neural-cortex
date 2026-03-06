"""HRM Planner — High-level task planning via Cloud LLMs.

Takes a complex task and breaks it into executable steps
that the Executor can handle with local models.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PlanStep(BaseModel):
    step_id: int
    description: str
    tool: str | None = None
    tool_args: dict[str, Any] | None = None
    depends_on: list[int] | None = None
    estimated_complexity: str = "low"


class Plan(BaseModel):
    task_id: str
    original_task: str
    steps: list[PlanStep]
    planner_model: str
    total_steps: int


_PLAN_SYSTEM_PROMPT = """You are a task planner for an AI agent system.
Break down the given task into concrete, executable steps.
Each step should be simple enough for a local LLM to execute.

Respond ONLY with a JSON array of steps:
[
  {
    "step_id": 1,
    "description": "What to do",
    "tool": "tool_name or null",
    "tool_args": {"key": "value"} or null,
    "depends_on": [step_ids] or null,
    "estimated_complexity": "low|medium|high"
  }
]

Available tools: file_read, file_write, file_edit, shell_exec, http_request,
docker_status, docker_exec, mattermost_send, mattermost_read, knowledge_search,
system_status, git_status, git_commit, deploy.
"""


class Planner:
    """Creates execution plans from complex tasks using Cloud LLMs."""

    def __init__(
        self,
        ollama_url: str = "http://10.40.10.90:11434",
        default_model: str = "opus-4.6",
        timeout: float = 120.0,
    ):
        self.ollama_url = ollama_url.rstrip("/")
        self.default_model = default_model
        self.timeout = timeout

    async def create_plan(
        self,
        task_id: str,
        task_description: str,
        model: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> Plan:
        """Create an execution plan for a complex task.

        For cloud models, this would call the cloud API.
        For local models, it calls Ollama.
        """
        model = model or self.default_model
        logger.info(f"Creating plan for task {task_id} using {model}")

        # Build prompt
        user_prompt = task_description
        if context:
            user_prompt = f"Context: {json.dumps(context, default=str)}\n\nTask: {task_description}"

        steps = await self._call_llm(model, user_prompt)

        return Plan(
            task_id=task_id,
            original_task=task_description,
            steps=steps,
            planner_model=model,
            total_steps=len(steps),
        )

    async def _call_llm(self, model: str, prompt: str) -> list[PlanStep]:
        """Call LLM to generate plan steps."""
        # Use Ollama API for all models (local and proxied)
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": _PLAN_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.3, "num_predict": 4096},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(f"{self.ollama_url}/api/chat", json=payload)
                resp.raise_for_status()
                data = resp.json()

            content = data.get("message", {}).get("content", "[]")
            raw_steps = json.loads(content)

            # Normalize — could be a dict with "steps" key or a direct list
            if isinstance(raw_steps, dict):
                raw_steps = raw_steps.get("steps", [])

            return [PlanStep(**s) for s in raw_steps]

        except Exception as e:
            logger.error(f"Planner LLM call failed: {e}")
            # Fallback: single-step plan
            return [
                PlanStep(
                    step_id=1,
                    description=prompt,
                    estimated_complexity="high",
                )
            ]

    async def refine_plan(
        self,
        plan: Plan,
        feedback: str,
        model: str | None = None,
    ) -> Plan:
        """Refine an existing plan based on execution feedback."""
        model = model or self.default_model
        refinement_prompt = (
            f"Original task: {plan.original_task}\n\n"
            f"Current plan:\n{json.dumps([s.model_dump() for s in plan.steps], indent=2)}\n\n"
            f"Feedback from execution:\n{feedback}\n\n"
            f"Please provide an improved plan that addresses the feedback."
        )

        steps = await self._call_llm(model, refinement_prompt)

        return Plan(
            task_id=plan.task_id,
            original_task=plan.original_task,
            steps=steps,
            planner_model=model,
            total_steps=len(steps),
        )
