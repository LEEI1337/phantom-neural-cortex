"""HRM (Hierarchical Reasoning Model) Controller.

Routes tasks between high-level planners (Cloud LLMs) and
low-level executors (Ollama local models) based on complexity.
"""

from .router import HRMRouter, ComplexityLevel
from .planner import Planner
from .executor import Executor

__all__ = ["HRMRouter", "ComplexityLevel", "Planner", "Executor"]
