import logging
import os
from typing import Optional, Dict, Any, List
from .backends.sql import SQLMemoryBackend
from .backends.redis import RedisMemoryBackend
from dashboard.backend.database import get_async_db

# Attempt to import redis, but don't fail if not installed
try:
    import redis.asyncio as redis
except ImportError:
    redis = None

logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Manages persistent memory across sessions (Phase 4).
    Acts as a bridge between the application and storage backends.
    """
    
    def __init__(self, backend_type: str = None):
        """
        Initialize memory manager.
        
        Args:
            backend_type: 'sql' or 'redis' (defaults to GATEWAY_STORAGE_BACKEND env var)
        """
        self.backend_type = backend_type or os.getenv("GATEWAY_STORAGE_BACKEND", "sql")
        
        if self.backend_type == "sql":
            # Pass the async db generator directly
            self.backend = SQLMemoryBackend(get_async_db)
        elif self.backend_type == "redis":
            if redis:
                redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
                client = redis.from_url(redis_url, decode_responses=True)
                self.backend = RedisMemoryBackend(client)
                logger.info(f"Initialized Redis memory backend at {redis_url}")
            else:
                logger.warning("redis-py not installed, falling back to SQL memory backend")
                self.backend = SQLMemoryBackend(get_async_db)
        else:
            logger.info(f"Using {self.backend_type} backend for memory")
            self.backend = SQLMemoryBackend(get_async_db) # Default fallback
            
    async def save_context_session(self, session_id: str, model: str, max_tokens: int, **kwargs):
        """Save context session state"""
        data = {
            "model": model,
            "max_tokens": max_tokens,
            **kwargs
        }
        await self.backend.save_session(session_id, data)
        
    async def load_context_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load context session state"""
        return await self.backend.load_session(session_id)
        
    async def add_context_item(self, session_id: str, item_id: str, item_data: Dict[str, Any]):
        """Add individual item to session history"""
        await self.backend.add_item(session_id, item_id, item_data)
        
    async def get_context_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieve full context history for a session"""
        return await self.backend.get_items(session_id)
        
    async def delete_context(self, session_id: str):
        """Delete all memory associated with a session"""
        await self.backend.delete_session(session_id)

    async def clear_context_items(self, session_id: str, keep_pinned: bool = True):
        """Clear context items while optionally preserving pinned items"""
        await self.backend.clear_items(session_id, keep_pinned)
