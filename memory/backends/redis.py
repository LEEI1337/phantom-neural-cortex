import logging
import json
from typing import List, Optional, Dict, Any
from . import BaseMemoryBackend

logger = logging.getLogger(__name__)

class RedisMemoryBackend(BaseMemoryBackend):
    """Redis-based memory backend (Phase 4)"""
    
    def __init__(self, redis_client):
        """
        Initialize Redis backend.
        
        Args:
            redis_client: Initialized redis-py or aioredis client
        """
        self.redis = redis_client
        self.prefix = "cortex:memory"
        
    def _session_key(self, session_id: str) -> str:
        return f"{self.prefix}:session:{session_id}"
        
    def _items_key(self, session_id: str) -> str:
        return f"{self.prefix}:items:{session_id}"

    async def save_session(self, session_id: str, data: Dict[str, Any]):
        """Save session state to Redis"""
        key = self._session_key(session_id)
        await self.redis.set(key, json.dumps(data))
        logger.debug(f"Saved session {session_id} to Redis")
        
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session state from Redis"""
        key = self._session_key(session_id)
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None
        
    async def add_item(self, session_id: str, item_id: str, data: Dict[str, Any]):
        """Add item to session history in Redis (stored in a list)"""
        key = self._items_key(session_id)
        # Store as JSON string in a list
        await self.redis.rpush(key, json.dumps(data))
        
    async def get_items(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all items for a session from Redis"""
        key = self._items_key(session_id)
        items = await self.redis.lrange(key, 0, -1)
        return [json.loads(item) for item in items]
        
    async def delete_session(self, session_id: str):
        """Delete session and its items from Redis"""
        await self.redis.delete(self._session_key(session_id))
        await self.redis.delete(self._items_key(session_id))

    async def clear_items(self, session_id: str, keep_pinned: bool = True):
        """Clear session items from Redis"""
        if not keep_pinned:
            await self.redis.delete(self._items_key(session_id))
        else:
            # More complex: filter list
            items = await self.get_items(session_id)
            pinned_items = [item for item in items if item.get('pinned')]
            await self.redis.delete(self._items_key(session_id))
            if pinned_items:
                for item in pinned_items:
                    await self.add_item(session_id, item.get('id'), item)
