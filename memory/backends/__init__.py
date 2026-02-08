from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

class BaseMemoryBackend(ABC):
    """Abstract base class for memory backends (Phase 4)"""
    
    @abstractmethod
    async def save_session(self, session_id: str, data: Dict[str, Any]):
        """Save session state"""
        pass
        
    @abstractmethod
    async def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session state"""
        pass
        
    @abstractmethod
    async def add_item(self, session_id: str, item_id: str, data: Dict[str, Any]):
        """Add item to session history"""
        pass
        
    @abstractmethod
    async def get_items(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all items for a session"""
        pass
        
    @abstractmethod
    async def delete_session(self, session_id: str):
        """Delete session and its items"""
        pass

    @abstractmethod
    async def clear_items(self, session_id: str, keep_pinned: bool = True):
        """Clear session items"""
        pass
