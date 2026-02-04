"""
Context Pruner

Automatic pruning strategies for context window management.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional

from .models import (
    ContextItem,
    MessageType,
    PruneResult
)
from .tracker import ContextTracker

logger = logging.getLogger(__name__)


class ContextPruner:
    """
    Prunes context items using various strategies.
    
    Strategies:
    - Time-based: Remove old messages
    - Importance-based: Remove low-importance items
    - Token-based: Remove until under threshold
    - Smart: Combination of strategies
    """
    
    def __init__(self, tracker: ContextTracker):
        """
        Initialize pruner with a context tracker.
        
        Args:
            tracker: ContextTracker instance to prune
        """
        self.tracker = tracker
        self.logger = logger
    
    def prune_old_messages(
        self,
        max_age_minutes: int = 60,
        keep_recent: int = 5
    ) -> PruneResult:
        """
        Prune messages older than specified age.
        
        Args:
            max_age_minutes: Maximum age of messages to keep
            keep_recent: Always keep this many recent messages
            
        Returns:
            PruneResult with details of pruned items
        """
        cutoff_time = datetime.now() - timedelta(minutes=max_age_minutes)
        items = self.tracker.get_items()
        
        # Sort by timestamp (newest first)
        sorted_items = sorted(items, key=lambda x: x.timestamp, reverse=True)
        
        pruned_items = []
        tokens_freed = 0
        
        for i, item in enumerate(sorted_items):
            # Skip if pinned
            if item.pinned:
                continue
            
            # Skip if system message
            if item.type == MessageType.SYSTEM:
                continue
            
            # Keep recent N messages
            if i < keep_recent:
                continue
            
            # Check age
            if item.timestamp < cutoff_time:
                if self.tracker.remove_item(item.id):
                    pruned_items.append(item)
                    tokens_freed += item.tokens
        
        status = self.tracker.get_status()
        
        self.logger.info(
            f"Time-based pruning: removed {len(pruned_items)} items, "
            f"freed {tokens_freed} tokens"
        )
        
        return PruneResult(
            pruned_items=pruned_items,
            items_removed=len(pruned_items),
            tokens_freed=tokens_freed,
            new_total=status.total_tokens,
            new_usage_percent=status.usage_percent,
            strategy_used="time_based"
        )
    
    def prune_by_importance(
        self,
        min_importance: float = 0.3,
        keep_recent: int = 5
    ) -> PruneResult:
        """
        Prune low-importance items.
        
        Args:
            min_importance: Minimum importance score to keep (0-1)
            keep_recent: Always keep this many recent messages
            
        Returns:
            PruneResult with details of pruned items
        """
        items = self.tracker.get_items()
        
        # Sort by timestamp (newest first)
        sorted_items = sorted(items, key=lambda x: x.timestamp, reverse=True)
        
        pruned_items = []
        tokens_freed = 0
        
        for i, item in enumerate(sorted_items):
            # Skip if pinned
            if item.pinned:
                continue
            
            # Skip if system message
            if item.type == MessageType.SYSTEM:
                continue
            
            # Keep recent N messages
            if i < keep_recent:
                continue
            
            # Check importance
            if item.importance < min_importance:
                if self.tracker.remove_item(item.id):
                    pruned_items.append(item)
                    tokens_freed += item.tokens
        
        status = self.tracker.get_status()
        
        self.logger.info(
            f"Importance-based pruning: removed {len(pruned_items)} items, "
            f"freed {tokens_freed} tokens"
        )
        
        return PruneResult(
            pruned_items=pruned_items,
            items_removed=len(pruned_items),
            tokens_freed=tokens_freed,
            new_total=status.total_tokens,
            new_usage_percent=status.usage_percent,
            strategy_used="importance_based"
        )
    
    def prune_tool_results(
        self,
        keep_recent: int = 3
    ) -> PruneResult:
        """
        Prune old tool results (which are often large).
        
        Args:
            keep_recent: Keep this many recent tool results
            
        Returns:
            PruneResult with details of pruned items
        """
        items = self.tracker.get_items()
        
        # Get tool results sorted by timestamp (newest first)
        tool_results = [
            item for item in items 
            if item.type == MessageType.TOOL_RESULT and not item.pinned
        ]
        tool_results.sort(key=lambda x: x.timestamp, reverse=True)
        
        pruned_items = []
        tokens_freed = 0
        
        # Remove old tool results
        for i, item in enumerate(tool_results):
            if i >= keep_recent:
                if self.tracker.remove_item(item.id):
                    pruned_items.append(item)
                    tokens_freed += item.tokens
        
        status = self.tracker.get_status()
        
        self.logger.info(
            f"Tool result pruning: removed {len(pruned_items)} items, "
            f"freed {tokens_freed} tokens"
        )
        
        return PruneResult(
            pruned_items=pruned_items,
            items_removed=len(pruned_items),
            tokens_freed=tokens_freed,
            new_total=status.total_tokens,
            new_usage_percent=status.usage_percent,
            strategy_used="tool_result_pruning"
        )
    
    def prune_to_threshold(
        self,
        target_percent: float = 70.0,
        keep_recent: int = 5
    ) -> PruneResult:
        """
        Prune items until context usage is below target threshold.
        
        Uses smart strategy: removes tool results first, then old messages,
        then low-importance items.
        
        Args:
            target_percent: Target usage percentage (0-100)
            keep_recent: Always keep this many recent messages
            
        Returns:
            PruneResult with details of pruned items
        """
        status = self.tracker.get_status()
        
        if status.usage_percent <= target_percent:
            self.logger.info(
                f"No pruning needed: usage {status.usage_percent:.1f}% "
                f"<= target {target_percent}%"
            )
            return PruneResult(
                pruned_items=[],
                items_removed=0,
                tokens_freed=0,
                new_total=status.total_tokens,
                new_usage_percent=status.usage_percent,
                strategy_used="smart_threshold"
            )
        
        all_pruned = []
        total_freed = 0
        
        # Strategy 1: Remove old tool results
        if self.tracker.get_status().usage_percent > target_percent:
            result = self.prune_tool_results(keep_recent=3)
            all_pruned.extend(result.pruned_items)
            total_freed += result.tokens_freed
        
        # Strategy 2: Remove old messages
        if self.tracker.get_status().usage_percent > target_percent:
            result = self.prune_old_messages(max_age_minutes=30, keep_recent=keep_recent)
            all_pruned.extend(result.pruned_items)
            total_freed += result.tokens_freed
        
        # Strategy 3: Remove low-importance items
        if self.tracker.get_status().usage_percent > target_percent:
            result = self.prune_by_importance(min_importance=0.5, keep_recent=keep_recent)
            all_pruned.extend(result.pruned_items)
            total_freed += result.tokens_freed
        
        status = self.tracker.get_status()
        
        self.logger.info(
            f"Smart threshold pruning: removed {len(all_pruned)} items total, "
            f"freed {total_freed} tokens, usage now {status.usage_percent:.1f}%"
        )
        
        return PruneResult(
            pruned_items=all_pruned,
            items_removed=len(all_pruned),
            tokens_freed=total_freed,
            new_total=status.total_tokens,
            new_usage_percent=status.usage_percent,
            strategy_used="smart_threshold"
        )
    
    def auto_prune(self, threshold: float = 80.0) -> Optional[PruneResult]:
        """
        Automatically prune if context exceeds threshold.
        
        Args:
            threshold: Usage threshold to trigger pruning (0-100)
            
        Returns:
            PruneResult if pruning occurred, None otherwise
        """
        status = self.tracker.get_status()
        
        if status.usage_percent < threshold:
            return None
        
        self.logger.warning(
            f"Auto-pruning triggered: usage {status.usage_percent:.1f}% "
            f">= threshold {threshold}%"
        )
        
        # Target 70% after pruning to give some headroom
        return self.prune_to_threshold(target_percent=70.0)
