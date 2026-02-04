"""
Context Compactor

AI-powered context compaction through summarization.
"""

import logging
from typing import List, Optional

from .models import (
    ContextItem,
    MessageType,
    CompactResult
)
from .tracker import ContextTracker
from .utils import count_tokens

logger = logging.getLogger(__name__)


class ContextCompactor:
    """
    Compacts context using AI-powered summarization.
    
    Features:
    - Summarize conversation threads
    - Compress tool outputs
    - Preserve essential information
    """
    
    def __init__(self, tracker: ContextTracker):
        """
        Initialize compactor with a context tracker.
        
        Args:
            tracker: ContextTracker instance to compact
        """
        self.tracker = tracker
        self.logger = logger
    
    def _generate_summary(self, items: List[ContextItem]) -> str:
        """
        Generate summary of context items.
        
        For now, this is a simple extraction. In production,
        this would use an AI model (Claude/Gemini) for intelligent summarization.
        
        Args:
            items: Items to summarize
            
        Returns:
            Summary text
        """
        # Simple summarization for now
        # TODO: Integrate with Claude/Gemini API for intelligent summarization
        
        summary_parts = []
        
        for item in items[:5]:  # Summarize first 5 items as example
            content_preview = item.content[:100]
            if len(item.content) > 100:
                content_preview += "..."
            summary_parts.append(f"- {item.type.value}: {content_preview}")
        
        if len(items) > 5:
            summary_parts.append(f"... and {len(items) - 5} more items")
        
        return "\n".join(summary_parts)
    
    def compact_old_messages(
        self,
        max_age_minutes: int = 60,
        keep_recent: int = 10
    ) -> CompactResult:
        """
        Compact old messages into a summary.
        
        Args:
            max_age_minutes: Messages older than this will be compacted
            keep_recent: Keep this many recent messages uncompacted
            
        Returns:
            CompactResult with details
        """
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.now() - timedelta(minutes=max_age_minutes)
        items = self.tracker.get_items()
        
        # Sort by timestamp (oldest first for compaction)
        sorted_items = sorted(items, key=lambda x: x.timestamp)
        
        # Find items to compact
        to_compact = []
        for i, item in enumerate(sorted_items):
            # Skip pinned and system messages
            if item.pinned or item.type == MessageType.SYSTEM:
                continue
            
            # Skip recent messages
            if len(sorted_items) - i <= keep_recent:
                break
            
            # Check age
            if item.timestamp < cutoff_time:
                to_compact.append(item)
        
        if not to_compact:
            self.logger.info("No items to compact")
            return CompactResult(
                original_tokens=0,
                compacted_tokens=0,
                tokens_saved=0,
                compression_ratio=0.0,
                summary="No items to compact",
                items_compacted=0
            )
        
        # Calculate original tokens
        original_tokens = sum(item.tokens for item in to_compact)
        
        # Generate summary
        summary = self._generate_summary(to_compact)
        summary_tokens = count_tokens(summary, self.tracker.model)
        
        # Remove old items
        for item in to_compact:
            self.tracker.remove_item(item.id)
        
        # Add summary as new message
        self.tracker.add_assistant_message(
            content=f"[Summary of {len(to_compact)} previous messages]\n{summary}",
            importance=0.7,
            metadata={"is_summary": True, "items_compacted": len(to_compact)}
        )
        
        tokens_saved = original_tokens - summary_tokens
        compression_ratio = summary_tokens / original_tokens if original_tokens > 0 else 0
        
        self.logger.info(
            f"Compacted {len(to_compact)} items: "
            f"{original_tokens} -> {summary_tokens} tokens "
            f"(saved {tokens_saved}, ratio {compression_ratio:.2f})"
        )
        
        return CompactResult(
            original_tokens=original_tokens,
            compacted_tokens=summary_tokens,
            tokens_saved=tokens_saved,
            compression_ratio=compression_ratio,
            summary=summary,
            items_compacted=len(to_compact)
        )
    
    def compact_tool_outputs(self) -> CompactResult:
        """
        Compact large tool outputs by extracting key information.
        
        Returns:
            CompactResult with details
        """
        items = self.tracker.get_items()
        
        # Find large tool results
        large_tool_results = [
            item for item in items
            if item.type == MessageType.TOOL_RESULT
            and item.tokens > 500  # Compact if > 500 tokens
            and not item.pinned
        ]
        
        if not large_tool_results:
            self.logger.info("No large tool results to compact")
            return CompactResult(
                original_tokens=0,
                compacted_tokens=0,
                tokens_saved=0,
                compression_ratio=0.0,
                summary="No large tool results found",
                items_compacted=0
            )
        
        original_tokens = sum(item.tokens for item in large_tool_results)
        compacted_tokens = 0
        
        for item in large_tool_results:
            # Extract first and last parts
            content = item.content
            if len(content) > 1000:
                # Keep first 300 and last 200 characters
                compacted = (
                    content[:300] + 
                    "\n\n[... content truncated ...]\n\n" + 
                    content[-200:]
                )
            else:
                # Keep first 500 characters
                compacted = content[:500] + "\n\n[... truncated ...]"
            
            tokens = count_tokens(compacted, self.tracker.model)
            compacted_tokens += tokens
            
            # Remove old item and add compacted version
            tool_name = item.metadata.get('tool_name', 'unknown')
            self.tracker.remove_item(item.id)
            self.tracker.add_tool_result(
                content=compacted,
                tool_name=tool_name,
                importance=item.importance,
                metadata={**item.metadata, "compacted": True}
            )
        
        tokens_saved = original_tokens - compacted_tokens
        compression_ratio = compacted_tokens / original_tokens if original_tokens > 0 else 0
        
        self.logger.info(
            f"Compacted {len(large_tool_results)} tool results: "
            f"{original_tokens} -> {compacted_tokens} tokens "
            f"(saved {tokens_saved}, ratio {compression_ratio:.2f})"
        )
        
        return CompactResult(
            original_tokens=original_tokens,
            compacted_tokens=compacted_tokens,
            tokens_saved=tokens_saved,
            compression_ratio=compression_ratio,
            summary=f"Compacted {len(large_tool_results)} tool outputs",
            items_compacted=len(large_tool_results)
        )
    
    def compact(self) -> CompactResult:
        """
        Run full compaction: messages and tool outputs.
        
        Returns:
            Combined CompactResult
        """
        # Compact messages
        msg_result = self.compact_old_messages()
        
        # Compact tool outputs
        tool_result = self.compact_tool_outputs()
        
        # Combine results
        return CompactResult(
            original_tokens=msg_result.original_tokens + tool_result.original_tokens,
            compacted_tokens=msg_result.compacted_tokens + tool_result.compacted_tokens,
            tokens_saved=msg_result.tokens_saved + tool_result.tokens_saved,
            compression_ratio=(
                (msg_result.compacted_tokens + tool_result.compacted_tokens) /
                (msg_result.original_tokens + tool_result.original_tokens)
                if (msg_result.original_tokens + tool_result.original_tokens) > 0
                else 0
            ),
            summary=f"Messages: {msg_result.summary}\nTools: {tool_result.summary}",
            items_compacted=msg_result.items_compacted + tool_result.items_compacted
        )
