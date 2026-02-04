"""
Context Inspector

CLI commands and inspection utilities for context window management.
"""

import logging
from typing import Dict, Any

from .models import (
    ContextStatus,
    ContextInspection,
    MessageType
)
from .tracker import ContextTracker
from .pruner import ContextPruner
from .compactor import ContextCompactor
from .utils import format_token_count, calculate_usage_color

logger = logging.getLogger(__name__)


class ContextInspector:
    """
    Provides inspection and CLI command functionality for context management.
    
    Commands:
    - status: Show context usage summary
    - list: List all context items
    - detail: Show detailed breakdown
    - compact: Trigger compaction
    """
    
    def __init__(self, tracker: ContextTracker):
        """
        Initialize inspector with a context tracker.
        
        Args:
            tracker: ContextTracker instance to inspect
        """
        self.tracker = tracker
        self.pruner = ContextPruner(tracker)
        self.compactor = ContextCompactor(tracker)
        self.logger = logger
    
    def get_status_display(self) -> str:
        """
        Get formatted status display (/status command).
        
        Returns:
            Formatted status string
        """
        status = self.tracker.get_status()
        color = calculate_usage_color(status.usage_percent)
        
        # Build status display
        lines = [
            "=" * 50,
            "CONTEXT WINDOW STATUS",
            "=" * 50,
            f"Session:  {status.session_id}",
            f"Model:    {status.model.value}",
            f"",
            f"Usage:    {format_token_count(status.total_tokens)}/{format_token_count(status.max_tokens)} "
            f"({status.usage_percent:.1f}%) [{color.upper()}]",
            f"Available: {format_token_count(status.available_tokens)} tokens",
            f"",
            f"Breakdown:",
            f"├─ System:   {format_token_count(status.system_tokens)} tokens",
            f"├─ Messages: {format_token_count(status.message_tokens)} tokens",
            f"└─ Tools:    {format_token_count(status.tool_tokens)} tokens",
            f"",
            f"Items:    {status.item_count} total",
            f"Warning:  {'⚠️  Near full! Consider pruning.' if status.is_near_full else '✓ Healthy'}",
            "=" * 50
        ]
        
        return "\n".join(lines)
    
    def get_items_list(self) -> str:
        """
        Get formatted list of context items (/context list command).
        
        Returns:
            Formatted items list
        """
        items = self.tracker.get_items()
        
        if not items:
            return "No items in context."
        
        lines = [
            "=" * 70,
            f"CONTEXT ITEMS ({len(items)} total)",
            "=" * 70
        ]
        
        for i, item in enumerate(items, 1):
            # Truncate content for display
            content_preview = item.content[:60]
            if len(item.content) > 60:
                content_preview += "..."
            
            pinned_marker = "📌 " if item.pinned else "   "
            
            lines.append(
                f"{i:3d}. {pinned_marker}[{item.type.value:12s}] "
                f"{format_token_count(item.tokens):>6s} | {content_preview}"
            )
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def get_detailed_breakdown(self) -> str:
        """
        Get detailed token breakdown (/context detail command).
        
        Returns:
            Formatted detailed breakdown
        """
        status = self.tracker.get_status()
        items = self.tracker.get_items()
        
        # Calculate breakdown by type
        breakdown = {
            "system": 0,
            "user": 0,
            "assistant": 0,
            "tool_call": 0,
            "tool_result": 0
        }
        
        for item in items:
            breakdown[item.type.value] += item.tokens
        
        lines = [
            "=" * 70,
            "DETAILED CONTEXT BREAKDOWN",
            "=" * 70,
            f"Session: {status.session_id}",
            f"Model:   {status.model.value} (max: {format_token_count(status.max_tokens)})",
            f"",
            f"TOTAL USAGE: {format_token_count(status.total_tokens)} "
            f"({status.usage_percent:.1f}%)",
            f"",
            "Token Breakdown by Type:",
            f"├─ System Prompts:    {format_token_count(breakdown['system']):>8s} "
            f"({breakdown['system']/status.total_tokens*100:.1f}%)" if status.total_tokens > 0 else "├─ System Prompts:         0",
            f"├─ User Messages:     {format_token_count(breakdown['user']):>8s} "
            f"({breakdown['user']/status.total_tokens*100:.1f}%)" if status.total_tokens > 0 else "├─ User Messages:          0",
            f"├─ Assistant Messages:{format_token_count(breakdown['assistant']):>8s} "
            f"({breakdown['assistant']/status.total_tokens*100:.1f}%)" if status.total_tokens > 0 else "├─ Assistant Messages:     0",
            f"├─ Tool Calls:        {format_token_count(breakdown['tool_call']):>8s} "
            f"({breakdown['tool_call']/status.total_tokens*100:.1f}%)" if status.total_tokens > 0 else "├─ Tool Calls:             0",
            f"└─ Tool Results:      {format_token_count(breakdown['tool_result']):>8s} "
            f"({breakdown['tool_result']/status.total_tokens*100:.1f}%)" if status.total_tokens > 0 else "└─ Tool Results:           0",
            f"",
            f"Item Statistics:",
            f"├─ Total Items:  {len(items)}",
            f"├─ Pinned Items: {sum(1 for item in items if item.pinned)}",
            f"├─ Oldest Item:  {min(items, key=lambda x: x.timestamp).timestamp.strftime('%Y-%m-%d %H:%M:%S')}" if items else "├─ Oldest Item:  N/A",
            f"└─ Newest Item:  {max(items, key=lambda x: x.timestamp).timestamp.strftime('%Y-%m-%d %H:%M:%S')}" if items else "└─ Newest Item:  N/A",
            "=" * 70
        ]
        
        return "\n".join(lines)
    
    def trigger_compaction(self) -> str:
        """
        Trigger manual compaction (/compact command).
        
        Returns:
            Formatted compaction result
        """
        status_before = self.tracker.get_status()
        
        # Run compaction
        result = self.compactor.compact()
        
        status_after = self.tracker.get_status()
        
        lines = [
            "=" * 50,
            "CONTEXT COMPACTION",
            "=" * 50,
            f"Before: {format_token_count(status_before.total_tokens)} "
            f"({status_before.usage_percent:.1f}%)",
            f"After:  {format_token_count(status_after.total_tokens)} "
            f"({status_after.usage_percent:.1f}%)",
            f"",
            f"Saved:  {format_token_count(result.tokens_saved)} tokens "
            f"({result.compression_ratio:.1%} compression)",
            f"Items:  {result.items_compacted} compacted",
            f"",
            f"Summary:",
            result.summary,
            "=" * 50
        ]
        
        return "\n".join(lines)
    
    def trigger_pruning(self, target_percent: float = 70.0) -> str:
        """
        Trigger manual pruning.
        
        Args:
            target_percent: Target usage percentage
            
        Returns:
            Formatted pruning result
        """
        status_before = self.tracker.get_status()
        
        # Run pruning
        result = self.pruner.prune_to_threshold(target_percent=target_percent)
        
        status_after = self.tracker.get_status()
        
        lines = [
            "=" * 50,
            "CONTEXT PRUNING",
            "=" * 50,
            f"Strategy: {result.strategy_used}",
            f"",
            f"Before: {format_token_count(status_before.total_tokens)} "
            f"({status_before.usage_percent:.1f}%)",
            f"After:  {format_token_count(status_after.total_tokens)} "
            f"({status_after.usage_percent:.1f}%)",
            f"",
            f"Freed:  {format_token_count(result.tokens_freed)} tokens",
            f"Items:  {len(result.pruned_items)} removed",
            "=" * 50
        ]
        
        return "\n".join(lines)
    
    def get_inspection_data(self) -> ContextInspection:
        """
        Get complete inspection data for API.
        
        Returns:
            ContextInspection model
        """
        status = self.tracker.get_status()
        items = self.tracker.get_items()
        
        # Calculate breakdown
        breakdown = {
            "system_prompt": status.system_tokens,
            "user_messages": sum(
                item.tokens for item in items 
                if item.type == MessageType.USER
            ),
            "assistant_messages": sum(
                item.tokens for item in items 
                if item.type == MessageType.ASSISTANT
            ),
            "tool_calls": sum(
                item.tokens for item in items 
                if item.type == MessageType.TOOL_CALL
            ),
            "tool_results": sum(
                item.tokens for item in items 
                if item.type == MessageType.TOOL_RESULT
            )
        }
        
        return ContextInspection(
            session_id=self.tracker.session_id,
            status=status,
            items=items,
            breakdown=breakdown
        )
