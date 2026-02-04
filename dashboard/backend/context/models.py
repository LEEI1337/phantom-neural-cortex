"""
Context Management Data Models

Pydantic models for context window management system.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Type of message in context"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class ModelType(str, Enum):
    """Supported AI model types"""
    CLAUDE = "claude"
    GEMINI = "gemini"
    GPT4 = "gpt4"
    GPT35 = "gpt35"
    OLLAMA = "ollama"


class ContextItem(BaseModel):
    """A single item in the context window"""
    id: str = Field(..., description="Unique identifier for this context item")
    type: MessageType = Field(..., description="Type of message")
    content: str = Field(..., description="Content of the message")
    tokens: int = Field(..., description="Token count for this item")
    timestamp: datetime = Field(default_factory=datetime.now, description="When item was added")
    importance: float = Field(default=1.0, description="Importance score (0-1)")
    pinned: bool = Field(default=False, description="Whether item is pinned (never pruned)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ContextWindow(BaseModel):
    """Complete context window state"""
    session_id: str = Field(..., description="Session identifier")
    model: ModelType = Field(..., description="AI model being used")
    max_tokens: int = Field(..., description="Maximum context window size")
    items: List[ContextItem] = Field(default_factory=list, description="Items in context")
    system_prompt_tokens: int = Field(default=0, description="Tokens used by system prompt")
    total_tokens: int = Field(default=0, description="Total tokens currently used")
    created_at: datetime = Field(default_factory=datetime.now, description="When context was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")

    @property
    def usage_percent(self) -> float:
        """Calculate context window usage percentage"""
        return (self.total_tokens / self.max_tokens) * 100 if self.max_tokens > 0 else 0

    @property
    def available_tokens(self) -> int:
        """Calculate available tokens"""
        return max(0, self.max_tokens - self.total_tokens)

    @property
    def is_near_full(self) -> bool:
        """Check if context is near full (>80%)"""
        return self.usage_percent >= 80


class ContextStatus(BaseModel):
    """Status information for context window"""
    session_id: str
    model: ModelType
    total_tokens: int
    max_tokens: int
    usage_percent: float
    available_tokens: int
    is_near_full: bool
    item_count: int
    system_tokens: int
    message_tokens: int
    tool_tokens: int


class PruneResult(BaseModel):
    """Result of pruning operation"""
    pruned_items: List[ContextItem] = Field(default_factory=list)
    tokens_freed: int
    new_total: int
    new_usage_percent: float
    strategy_used: str


class CompactResult(BaseModel):
    """Result of compaction operation"""
    original_tokens: int
    compacted_tokens: int
    tokens_saved: int
    compression_ratio: float
    summary: str
    items_compacted: int


class ContextInspection(BaseModel):
    """Detailed context inspection data"""
    session_id: str
    status: ContextStatus
    items: List[ContextItem]
    breakdown: Dict[str, int]
