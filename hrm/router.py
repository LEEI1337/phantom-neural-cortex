"""HRM Router — Complexity assessment and model routing.

Evaluates task complexity and routes to the appropriate tier:
- HIGH complexity → Planner (Cloud LLM: Opus/Codex)
- LOW complexity  → Executor (Ollama local model)
"""

from __future__ import annotations

import logging
import re
from enum import Enum
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ComplexityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ComplexityAssessment(BaseModel):
    level: ComplexityLevel
    score: float  # 0.0 - 1.0
    reasoning: str
    requires_planner: bool


# Keywords that indicate high complexity
_HIGH_COMPLEXITY_SIGNALS = [
    "architect", "design", "refactor", "debug", "security", "audit",
    "complex", "multi-step", "pipeline", "integration", "migrate",
    "optimize", "analyse", "plan", "strategy", "compliance", "dsgvo",
    "eu ai act", "risk", "vulnerability",
]

# Keywords that indicate simple execution
_LOW_COMPLEXITY_SIGNALS = [
    "format", "rename", "list", "status", "check", "health", "log",
    "simple", "restart", "deploy", "send", "post", "read", "get",
    "count", "delete", "create file", "copy",
]


class HRMRouter:
    """Routes tasks to Planner or Executor based on complexity."""

    def __init__(
        self,
        high_threshold: float = 0.6,
        planner_model: str = "opus-4.6",
        executor_model: str = "mistral-small3.2",
        fallback_models: list[str] | None = None,
        local_only: bool = False,
    ):
        self.high_threshold = high_threshold
        self.planner_model = planner_model
        self.executor_model = executor_model
        self.fallback_models = fallback_models or ["llama3.1:8b"]
        self.local_only = local_only

    def assess_complexity(self, task_description: str) -> ComplexityAssessment:
        """Assess task complexity using keyword heuristics and structure analysis."""
        text = task_description.lower()
        score = 0.5  # Base score

        # Keyword matching
        high_hits = sum(1 for kw in _HIGH_COMPLEXITY_SIGNALS if kw in text)
        low_hits = sum(1 for kw in _LOW_COMPLEXITY_SIGNALS if kw in text)

        score += high_hits * 0.08
        score -= low_hits * 0.06

        # Length heuristic — longer descriptions often mean more complex tasks
        word_count = len(text.split())
        if word_count > 100:
            score += 0.15
        elif word_count > 50:
            score += 0.08

        # Multi-step detection
        step_patterns = [
            r"\d+\.\s",  # "1. ", "2. "
            r"then\s",
            r"after that",
            r"next,?\s",
            r"finally",
            r"danach",
            r"anschliessend",
            r"zuerst",
        ]
        step_count = sum(len(re.findall(p, text)) for p in step_patterns)
        if step_count >= 3:
            score += 0.2
        elif step_count >= 1:
            score += 0.1

        # Code-related complexity
        if any(kw in text for kw in ["class ", "function ", "async ", "import "]):
            score += 0.1

        # Clamp
        score = max(0.0, min(1.0, score))

        # Classify
        if score >= self.high_threshold:
            level = ComplexityLevel.HIGH
        elif score >= 0.35:
            level = ComplexityLevel.MEDIUM
        else:
            level = ComplexityLevel.LOW

        requires_planner = level == ComplexityLevel.HIGH and not self.local_only

        reasoning = (
            f"Complexity score {score:.2f} "
            f"(high_kw={high_hits}, low_kw={low_hits}, steps={step_count}, words={word_count})"
        )

        return ComplexityAssessment(
            level=level,
            score=score,
            reasoning=reasoning,
            requires_planner=requires_planner,
        )

    def select_model(self, assessment: ComplexityAssessment) -> str:
        """Select the best model for the given complexity."""
        if assessment.requires_planner:
            return self.planner_model
        return self.executor_model

    def get_fallback_chain(self, assessment: ComplexityAssessment) -> list[str]:
        """Get the ordered list of models to try."""
        primary = self.select_model(assessment)
        chain = [primary]

        if assessment.requires_planner:
            # Planner failed → try executor → fallbacks
            chain.append(self.executor_model)

        chain.extend(self.fallback_models)
        # Deduplicate while preserving order
        seen = set()
        return [m for m in chain if not (m in seen or seen.add(m))]
