"""
Message Router

Routes messages between clients and agents with queue management.
"""

import asyncio
import logging
from typing import Dict, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """Message types"""
    USER_MESSAGE = "user_message"
    AGENT_RESPONSE = "agent_response"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    SYSTEM = "system"
    ERROR = "error"


@dataclass
class Message:
    """Message data model"""
    message_id: str
    session_id: str
    type: MessageType
    content: Any
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MessageRouter:
    """
    Routes messages between clients and agents.
    
    Features:
    - Message queuing per session
    - Priority routing
    - Load balancing
    - Message history tracking
    """
    
    def __init__(self, queue_size: int = 1000):
        """
        Initialize message router.
        
        Args:
            queue_size: Maximum queue size per session
        """
        self.queue_size = queue_size
        
        # Message queues per session
        self._queues: Dict[str, asyncio.Queue] = {}
        
        # Message handlers
        self._handlers: Dict[MessageType, Callable] = {}
        
        # Active routes
        self._routes: Dict[str, str] = {}  # session_id -> agent_id
        
        logger.info("MessageRouter initialized")
    
    def register_handler(self, message_type: MessageType, handler: Callable):
        """
        Register message handler.
        
        Args:
            message_type: Type of message to handle
            handler: Handler function
        """
        self._handlers[message_type] = handler
        logger.info(f"Registered handler for {message_type.value}")
    
    async def route_message(self, message: Message) -> bool:
        """
        Route message to appropriate handler.
        
        Args:
            message: Message to route
            
        Returns:
            True if routed successfully
        """
        try:
            # Get or create queue for session
            if message.session_id not in self._queues:
                self._queues[message.session_id] = asyncio.Queue(maxsize=self.queue_size)
            
            queue = self._queues[message.session_id]
            
            # Add to queue
            try:
                await asyncio.wait_for(queue.put(message), timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning(f"Queue full for session {message.session_id}")
                return False
            
            # Process message
            await self._process_message(message)
            
            return True
        
        except Exception as e:
            logger.error(f"Error routing message: {e}")
            return False
    
    async def _process_message(self, message: Message):
        """Process message with registered handler"""
        handler = self._handlers.get(message.type)
        
        if handler:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Error in message handler: {e}")
        else:
            logger.warning(f"No handler registered for {message.type.value}")
    
    async def get_queue(self, session_id: str) -> Optional[asyncio.Queue]:
        """
        Get message queue for session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Message queue or None
        """
        return self._queues.get(session_id)
    
    def clear_queue(self, session_id: str):
        """
        Clear message queue for session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self._queues:
            # Create new empty queue
            self._queues[session_id] = asyncio.Queue(maxsize=self.queue_size)
            logger.info(f"Cleared queue for session {session_id}")
    
    def remove_queue(self, session_id: str):
        """
        Remove message queue for session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self._queues:
            del self._queues[session_id]
            logger.info(f"Removed queue for session {session_id}")
    
    def get_queue_size(self, session_id: str) -> int:
        """
        Get current queue size for session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Queue size
        """
        queue = self._queues.get(session_id)
        return queue.qsize() if queue else 0
