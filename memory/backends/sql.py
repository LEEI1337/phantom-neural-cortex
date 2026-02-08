import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from . import BaseMemoryBackend

# Use relative imports when possible, but for models we might need absolute if this is used from different locations
import sys
import os
# Ensure root is in path to import dashboard.backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dashboard.backend.models import ContextSession, ContextItem

logger = logging.getLogger(__name__)

class SQLMemoryBackend(BaseMemoryBackend):
    """SQLAlchemy-based memory backend (Phase 4)"""
    
    def __init__(self, db_factory):
        """
        Initialize SQL backend.
        
        Args:
            db_factory: Callable/Generator that yields an AsyncSession
        """
        self.db_factory = db_factory
        
    async def save_session(self, session_id: str, data: Dict[str, Any]):
        """Save session state to SQL"""
        async for db in self.db_factory():
            try:
                # Check if session exists
                stmt = select(ContextSession).filter(ContextSession.id == session_id)
                result = await db.execute(stmt)
                session = result.scalar_one_or_none()
                
                if not session:
                    session = ContextSession(
                        id=session_id,
                        model=data.get('model', 'unknown'),
                        max_tokens=data.get('max_tokens', 0)
                    )
                    db.add(session)
                
                # Update attributes
                session.user_id = data.get('user_id')
                session.system_prompt_tokens = data.get('system_prompt_tokens', 0)
                session.total_tokens = data.get('total_tokens', 0)
                session.metadata_json = data.get('metadata', {})
                session.updated_at = datetime.utcnow()
                
                await db.commit()
                logger.debug(f"Saved session {session_id} to SQL")
            except Exception as e:
                await db.rollback()
                logger.error(f"Error saving session {session_id} to SQL: {e}")
                raise
                
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session state from SQL"""
        async for db in self.db_factory():
            stmt = select(ContextSession).filter(ContextSession.id == session_id)
            result = await db.execute(stmt)
            session = result.scalar_one_or_none()
            
            if not session:
                return None
            
            return {
                "session_id": session.id,
                "user_id": session.user_id,
                "model": session.model,
                "max_tokens": session.max_tokens,
                "system_prompt_tokens": session.system_prompt_tokens,
                "total_tokens": session.total_tokens,
                "metadata": session.metadata_json or {},
                "created_at": session.created_at,
                "updated_at": session.updated_at
            }
            
    async def add_item(self, session_id: str, item_id: str, data: Dict[str, Any]):
        """Add item to session history in SQL"""
        async for db in self.db_factory():
            try:
                item = ContextItem(
                    id=item_id,
                    session_id=session_id,
                    type=data.get('type'),
                    content=data.get('content'),
                    tokens=data.get('tokens', 0),
                    importance=data.get('importance', 1.0),
                    pinned=data.get('pinned', False),
                    tool_name=data.get('tool_name'),
                    metadata_json=data.get('metadata', {}),
                    timestamp=data.get('timestamp', datetime.utcnow())
                )
                db.add(item)
                await db.commit()
            except Exception as e:
                await db.rollback()
                logger.error(f"Error adding item {item_id} to SQL: {e}")
                raise
                
    async def get_items(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all items for a session from SQL"""
        async for db in self.db_factory():
            stmt = select(ContextItem).filter(ContextItem.session_id == session_id).order_by(ContextItem.timestamp)
            result = await db.execute(stmt)
            items = result.scalars().all()
            
            return [
                {
                    "id": item.id,
                    "type": item.type,
                    "content": item.content,
                    "tokens": item.tokens,
                    "timestamp": item.timestamp,
                    "importance": item.importance,
                    "pinned": item.pinned,
                    "tool_name": item.tool_name,
                    "metadata": item.metadata_json or {}
                }
                for item in items
            ]
            
    async def delete_session(self, session_id: str):
        """Delete session and its items from SQL"""
        async for db in self.db_factory():
            try:
                stmt = delete(ContextSession).filter(ContextSession.id == session_id)
                await db.execute(stmt)
                await db.commit()
            except Exception as e:
                await db.rollback()
                logger.error(f"Error deleting session {session_id} from SQL: {e}")
                raise

    async def clear_items(self, session_id: str, keep_pinned: bool = True):
        """Clear session items from SQL"""
        async for db in self.db_factory():
            try:
                stmt = delete(ContextItem).filter(ContextItem.session_id == session_id)
                if keep_pinned:
                    stmt = stmt.filter(ContextItem.pinned == False)
                await db.execute(stmt)
                await db.commit()
            except Exception as e:
                await db.rollback()
                logger.error(f"Error clearing items for session {session_id} from SQL: {e}")
                raise
