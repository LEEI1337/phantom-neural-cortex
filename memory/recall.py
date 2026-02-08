import logging
import os
from typing import List, Dict, Any, Optional
from .persistence import MemoryManager
from dashboard.backend.context.utils import count_tokens

logger = logging.getLogger(__name__)

class MemoryRecall:
    """
    Intelligent memory recall system (Phase 4).
    Provides semantic search and context retrieval capabilities.
    """
    
    def __init__(self, manager: MemoryManager = None):
        self.manager = manager or MemoryManager()
        
    async def get_relevant_history(
        self, 
        session_id: str, 
        query: Optional[str] = None, 
        limit: int = 10,
        min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant items from history.
        
        Args:
            session_id: Session ID
            query: Optional search query (for future semantic search)
            limit: Max items to return
            min_importance: Minimum importance threshold
            
        Returns:
            List of relevant context items
        """
        # 1. Get all history
        full_history = await self.manager.get_context_history(session_id)
        
        if not full_history:
            return []
            
        # 2. Filter by importance
        filtered = [item for item in full_history if item.get('importance', 1.0) >= min_importance]
        
        # 3. Simple fuzzy/keyword search (Fallback if no vector DB yet)
        if query:
            query = query.lower()
            scored_items = []
            for item in filtered:
                content = item.get('content', '').lower()
                score = 0
                if query in content:
                    score += 10
                # Could add more complex scoring here
                if score > 0:
                    scored_items.append((score, item))
            
            # Sort by score then timestamp
            scored_items.sort(key=lambda x: (x[0], x[1].get('timestamp')), reverse=True)
            results = [item for score, item in scored_items[:limit]]
        else:
            # Just take recent ones if no query
            results = filtered[-limit:]
            
        return results

    async def get_summary_context(self, session_id: str, max_tokens: int = 1000) -> str:
        """
        Generate a summarized view of past context for quick injection.
        
        Args:
            session_id: Session ID
            max_tokens: Max tokens for summary
            
        Returns:
            Summary string
        """
        # Load high-importance items
        items = await self.get_relevant_history(session_id, min_importance=0.7, limit=20)
        
        if not items:
            return "No previous context found."
            
        summary_parts = ["Summary of relevant past context:"]
        current_tokens = count_tokens(summary_parts[0], "claude")
        
        for item in items:
            part = f"[{item['type']}] {item['content'][:200]}..."
            tokens = count_tokens(part, "claude")
            if current_tokens + tokens > max_tokens:
                break
            summary_parts.append(part)
            current_tokens += tokens
            
        return "\n".join(summary_parts)
