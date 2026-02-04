"""
Context Window Tracker

Real-time token tracking for context window management.
"""

import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from .models import (
    ContextWindow,
    ContextItem,
    ContextStatus,
    MessageType,
    ModelType
)
from .utils import count_tokens, get_model_limit

logger = logging.getLogger(__name__)


class ContextTracker:
    """
    Tracks token usage in real-time for a context window.
    
    Features:
    - Real-time token counting
    - Multiple message types
    - Auto-calculation of usage
    - Support for multiple AI models
    """
    
    def __init__(
        self,
        session_id: str,
        model: ModelType = ModelType.CLAUDE,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize context tracker.
        
        Args:
            session_id: Unique session identifier
            model: AI model being used
            max_tokens: Override default max tokens for model
        """
        self.session_id = session_id
        self.model = model
        self.max_tokens = max_tokens or get_model_limit(model)
        
        # Initialize context window
        self.context = ContextWindow(
            session_id=session_id,
            model=model,
            max_tokens=self.max_tokens
        )
        
        logger.info(
            f"ContextTracker initialized for session {session_id} "
            f"with model {model.value} (max: {self.max_tokens} tokens)"
        )
    
    def add_system_prompt(
        self,
        content: str,
        pinned: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextItem:
        """
        Add system prompt to context.
        
        Args:
            content: System prompt content
            pinned: Whether to pin (prevent pruning)
            metadata: Additional metadata
            
        Returns:
            Created context item
        """
        tokens = count_tokens(content, self.model)
        
        item = ContextItem(
            id=f"system_{uuid.uuid4().hex[:8]}",
            type=MessageType.SYSTEM,
            content=content,
            tokens=tokens,
            importance=1.0,  # System prompts always important
            pinned=pinned,
            metadata=metadata or {}
        )
        
        self.context.items.append(item)
        self.context.system_prompt_tokens += tokens
        self._recalculate_total()
        
        logger.debug(f"Added system prompt: {tokens} tokens")
        return item
    
    def add_user_message(
        self,
        content: str,
        importance: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextItem:
        """
        Add user message to context.
        
        Args:
            content: User message content
            importance: Importance score (0-1)
            metadata: Additional metadata
            
        Returns:
            Created context item
        """
        tokens = count_tokens(content, self.model)
        
        item = ContextItem(
            id=f"user_{uuid.uuid4().hex[:8]}",
            type=MessageType.USER,
            content=content,
            tokens=tokens,
            importance=importance,
            metadata=metadata or {}
        )
        
        self.context.items.append(item)
        self._recalculate_total()
        
        logger.debug(f"Added user message: {tokens} tokens")
        return item
    
    def add_assistant_message(
        self,
        content: str,
        importance: float = 0.8,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextItem:
        """
        Add assistant response to context.
        
        Args:
            content: Assistant response content
            importance: Importance score (0-1)
            metadata: Additional metadata
            
        Returns:
            Created context item
        """
        tokens = count_tokens(content, self.model)
        
        item = ContextItem(
            id=f"assistant_{uuid.uuid4().hex[:8]}",
            type=MessageType.ASSISTANT,
            content=content,
            tokens=tokens,
            importance=importance,
            metadata=metadata or {}
        )
        
        self.context.items.append(item)
        self._recalculate_total()
        
        logger.debug(f"Added assistant message: {tokens} tokens")
        return item
    
    def add_tool_call(
        self,
        content: str,
        tool_name: str,
        importance: float = 0.6,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextItem:
        """
        Add tool call to context.
        
        Args:
            content: Tool call content
            tool_name: Name of the tool
            importance: Importance score (0-1)
            metadata: Additional metadata
            
        Returns:
            Created context item
        """
        tokens = count_tokens(content, self.model)
        
        meta = metadata or {}
        meta['tool_name'] = tool_name
        
        item = ContextItem(
            id=f"tool_call_{uuid.uuid4().hex[:8]}",
            type=MessageType.TOOL_CALL,
            content=content,
            tokens=tokens,
            importance=importance,
            metadata=meta
        )
        
        self.context.items.append(item)
        self._recalculate_total()
        
        logger.debug(f"Added tool call ({tool_name}): {tokens} tokens")
        return item
    
    def add_tool_result(
        self,
        content: str,
        tool_name: str,
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextItem:
        """
        Add tool result to context.
        
        Args:
            content: Tool result content
            tool_name: Name of the tool
            importance: Importance score (0-1)
            metadata: Additional metadata
            
        Returns:
            Created context item
        """
        tokens = count_tokens(content, self.model)
        
        meta = metadata or {}
        meta['tool_name'] = tool_name
        
        item = ContextItem(
            id=f"tool_result_{uuid.uuid4().hex[:8]}",
            type=MessageType.TOOL_RESULT,
            content=content,
            tokens=tokens,
            importance=importance,
            metadata=meta
        )
        
        self.context.items.append(item)
        self._recalculate_total()
        
        logger.debug(f"Added tool result ({tool_name}): {tokens} tokens")
        return item
    
    def remove_item(self, item_id: str) -> bool:
        """
        Remove an item from context.
        
        Args:
            item_id: ID of item to remove
            
        Returns:
            True if removed, False if not found
        """
        for i, item in enumerate(self.context.items):
            if item.id == item_id:
                removed = self.context.items.pop(i)
                if removed.type == MessageType.SYSTEM:
                    self.context.system_prompt_tokens -= removed.tokens
                self._recalculate_total()
                logger.debug(f"Removed item {item_id}: freed {removed.tokens} tokens")
                return True
        return False
    
    def _recalculate_total(self):
        """Recalculate total token usage"""
        self.context.total_tokens = sum(item.tokens for item in self.context.items)
        self.context.updated_at = datetime.now()
    
    def get_status(self) -> ContextStatus:
        """
        Get current context status.
        
        Returns:
            Current status information
        """
        # Calculate token breakdown by type
        message_tokens = sum(
            item.tokens for item in self.context.items 
            if item.type in [MessageType.USER, MessageType.ASSISTANT]
        )
        tool_tokens = sum(
            item.tokens for item in self.context.items 
            if item.type in [MessageType.TOOL_CALL, MessageType.TOOL_RESULT]
        )
        
        return ContextStatus(
            session_id=self.session_id,
            model=self.model,
            total_tokens=self.context.total_tokens,
            max_tokens=self.max_tokens,
            usage_percent=self.context.usage_percent,
            available_tokens=self.context.available_tokens,
            is_near_full=self.context.is_near_full,
            item_count=len(self.context.items),
            system_tokens=self.context.system_prompt_tokens,
            message_tokens=message_tokens,
            tool_tokens=tool_tokens
        )
    
    def get_items(self) -> List[ContextItem]:
        """
        Get all context items.
        
        Returns:
            List of context items
        """
        return self.context.items.copy()
    
    def get_item_by_id(self, item_id: str) -> Optional[ContextItem]:
        """
        Get context item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            Context item or None if not found
        """
        for item in self.context.items:
            if item.id == item_id:
                return item
        return None
    
    def clear(self):
        """Clear all non-pinned items from context"""
        original_count = len(self.context.items)
        self.context.items = [item for item in self.context.items if item.pinned]
        self._recalculate_total()
        
        removed = original_count - len(self.context.items)
        logger.info(f"Cleared context: removed {removed} items")
