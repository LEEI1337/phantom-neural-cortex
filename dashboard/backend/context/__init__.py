"""
Context Window Management System

OpenClaw-inspired context management for Phantom Neural Cortex.

Features:
- Real-time token tracking
- Automatic pruning
- AI-powered compaction
- CLI commands for inspection
"""

from .models import (
    MessageType,
    ModelType,
    ContextItem,
    ContextWindow,
    ContextStatus,
    PruneResult,
    CompactResult,
    ContextInspection
)

from .tracker import ContextTracker
from .pruner import ContextPruner
from .compactor import ContextCompactor
from .inspector import ContextInspector
from .utils import (
    count_tokens,
    get_model_limit,
    format_token_count,
    calculate_usage_color
)

__all__ = [
    # Models
    'MessageType',
    'ModelType',
    'ContextItem',
    'ContextWindow',
    'ContextStatus',
    'PruneResult',
    'CompactResult',
    'ContextInspection',
    # Core classes
    'ContextTracker',
    'ContextPruner',
    'ContextCompactor',
    'ContextInspector',
    # Utils
    'count_tokens',
    'get_model_limit',
    'format_token_count',
    'calculate_usage_color',
]

__version__ = '1.0.0'
