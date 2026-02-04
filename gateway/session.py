"""
Session Management

Manages session lifecycle, persistence, and state across restarts.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class SessionStatus(str, Enum):
    """Session status enum"""
    ACTIVE = "active"
    IDLE = "idle"
    EXPIRED = "expired"
    CLOSED = "closed"


@dataclass
class Session:
    """Session data model"""
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime = None
    last_activity: datetime = None
    status: SessionStatus = SessionStatus.ACTIVE
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_activity is None:
            self.last_activity = datetime.now()
        if self.metadata is None:
            self.metadata = {}
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
        if self.status == SessionStatus.IDLE:
            self.status = SessionStatus.ACTIVE
    
    def is_expired(self, timeout_seconds: int) -> bool:
        """Check if session has expired"""
        if self.status == SessionStatus.CLOSED:
            return True
        
        time_since_activity = datetime.now() - self.last_activity
        return time_since_activity.total_seconds() > timeout_seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_activity'] = self.last_activity.isoformat()
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        """Create session from dictionary"""
        data = data.copy()
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_activity'] = datetime.fromisoformat(data['last_activity'])
        data['status'] = SessionStatus(data['status'])
        return cls(**data)


class SessionManager:
    """
    Session manager with persistence support.
    
    Features:
    - Create/destroy sessions
    - Persist session state
    - Resume sessions after restart
    - Track active sessions
    - Automatic cleanup of expired sessions
    """
    
    def __init__(
        self,
        storage_backend: str = "memory",
        redis_client = None,
        db_session = None,
        session_timeout: int = 3600
    ):
        """
        Initialize session manager.
        
        Args:
            storage_backend: Storage backend (memory, redis, database)
            redis_client: Redis client instance
            db_session: Database session instance
            session_timeout: Session timeout in seconds
        """
        self.storage_backend = storage_backend
        self.redis_client = redis_client
        self.db_session = db_session
        self.session_timeout = session_timeout
        
        # In-memory cache
        self._sessions: Dict[str, Session] = {}
        self._cleanup_task: Optional[asyncio.Task] = None
        
        logger.info(f"SessionManager initialized with {storage_backend} backend")
    
    async def start(self):
        """Start session manager and background tasks"""
        # Load existing sessions from storage
        await self._load_sessions()
        
        # Start cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        
        logger.info("SessionManager started")
    
    async def stop(self):
        """Stop session manager and save state"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Save all active sessions
        await self._save_sessions()
        
        logger.info("SessionManager stopped")
    
    async def create_session(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Session:
        """
        Create new session.
        
        Args:
            user_id: Optional user identifier
            session_id: Optional session ID (generated if not provided)
            metadata: Optional session metadata
            
        Returns:
            Created session
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            metadata=metadata or {}
        )
        
        self._sessions[session_id] = session
        await self._persist_session(session)
        
        logger.info(f"Created session {session_id}")
        return session
    
    async def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session or None if not found
        """
        session = self._sessions.get(session_id)
        
        if session:
            # Check if expired
            if session.is_expired(self.session_timeout):
                await self.close_session(session_id)
                return None
            
            session.update_activity()
            await self._persist_session(session)
        
        return session
    
    async def close_session(self, session_id: str) -> bool:
        """
        Close session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if closed, False if not found
        """
        session = self._sessions.get(session_id)
        if not session:
            return False
        
        session.status = SessionStatus.CLOSED
        await self._persist_session(session)
        del self._sessions[session_id]
        
        logger.info(f"Closed session {session_id}")
        return True
    
    async def list_sessions(
        self,
        user_id: Optional[str] = None,
        status: Optional[SessionStatus] = None
    ) -> List[Session]:
        """
        List sessions with optional filtering.
        
        Args:
            user_id: Filter by user ID
            status: Filter by status
            
        Returns:
            List of sessions
        """
        sessions = list(self._sessions.values())
        
        if user_id:
            sessions = [s for s in sessions if s.user_id == user_id]
        
        if status:
            sessions = [s for s in sessions if s.status == status]
        
        return sessions
    
    async def _persist_session(self, session: Session):
        """Persist session to storage backend"""
        if self.storage_backend == "redis" and self.redis_client:
            key = f"session:{session.session_id}"
            data = json.dumps(session.to_dict())
            await self.redis_client.set(key, data, ex=self.session_timeout)
        
        elif self.storage_backend == "database" and self.db_session:
            # Database persistence not yet implemented
            # Sessions will only persist in memory for database backend
            logger.warning("Database persistence not implemented, using memory storage")
    
    async def _load_sessions(self):
        """Load sessions from storage backend"""
        if self.storage_backend == "redis" and self.redis_client:
            try:
                keys = await self.redis_client.keys("session:*")
                for key in keys:
                    data = await self.redis_client.get(key)
                    if data:
                        session_dict = json.loads(data)
                        session = Session.from_dict(session_dict)
                        self._sessions[session.session_id] = session
                
                logger.info(f"Loaded {len(self._sessions)} sessions from Redis")
            except Exception as e:
                logger.error(f"Failed to load sessions from Redis: {e}")
    
    async def _save_sessions(self):
        """Save all active sessions to storage"""
        for session in self._sessions.values():
            if session.status != SessionStatus.CLOSED:
                await self._persist_session(session)
        
        logger.info(f"Saved {len(self._sessions)} sessions")
    
    async def _cleanup_loop(self):
        """Background task to cleanup expired sessions"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                expired_ids = [
                    sid for sid, session in self._sessions.items()
                    if session.is_expired(self.session_timeout)
                ]
                
                for session_id in expired_ids:
                    await self.close_session(session_id)
                
                if expired_ids:
                    logger.info(f"Cleaned up {len(expired_ids)} expired sessions")
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
