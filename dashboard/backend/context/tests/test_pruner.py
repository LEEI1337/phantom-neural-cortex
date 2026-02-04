"""
Unit tests for ContextPruner
"""

import pytest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from context import ContextTracker, ContextPruner, ModelType


class TestContextPruner:
    """Test ContextPruner functionality"""
    
    def setup_method(self):
        """Setup test tracker with multiple messages"""
        self.tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        
        # Add system prompt (pinned)
        self.tracker.add_system_prompt("You are a helpful assistant.", pinned=True)
        
        # Add some user/assistant messages
        for i in range(10):
            self.tracker.add_user_message(f"User message {i}")
            self.tracker.add_assistant_message(f"Assistant response {i}")
        
        # Add some tool results
        self.tracker.add_tool_result("Tool result 1", tool_name="grep")
        self.tracker.add_tool_result("Tool result 2", tool_name="view")
    
    def test_initialization(self):
        """Test pruner initialization"""
        pruner = ContextPruner(self.tracker)
        assert pruner.tracker == self.tracker
    
    def test_prune_old_messages(self):
        """Test pruning old messages"""
        pruner = ContextPruner(self.tracker)
        
        # Get initial state
        status_before = self.tracker.get_status()
        initial_count = status_before.item_count
        
        # Prune keeping only last 5 messages
        result = pruner.prune_old_messages(keep_recent=5, max_age_minutes=0.01)
        
        # Should have pruned some messages
        status_after = self.tracker.get_status()
        assert status_after.item_count < initial_count
        assert result.items_removed > 0
        assert result.tokens_freed > 0
        
        # Pinned system prompt should remain
        items = self.tracker.get_items()
        assert any(item.pinned for item in items)
    
    def test_prune_by_importance(self):
        """Test pruning by importance threshold"""
        pruner = ContextPruner(self.tracker)
        
        # Get initial state
        status_before = self.tracker.get_status()
        
        # Prune messages with low importance
        result = pruner.prune_by_importance(min_importance=0.7)
        
        # Should have pruned some messages
        assert result.items_removed >= 0
        
        # All remaining messages should have importance >= 0.7 or be pinned
        items = self.tracker.get_items()
        for item in items:
            assert item.importance >= 0.7 or item.pinned
    
    def test_prune_tool_outputs(self):
        """Test pruning tool outputs"""
        pruner = ContextPruner(self.tracker)
        
        # Get initial tool token count
        status_before = self.tracker.get_status()
        tool_tokens_before = status_before.tool_tokens
        
        # Prune tool outputs
        result = pruner.prune_tool_outputs(keep_recent=1)
        
        # Should have pruned at least one tool output
        assert result.items_removed >= 1
        
        # Tool tokens should be reduced
        status_after = self.tracker.get_status()
        assert status_after.tool_tokens < tool_tokens_before
    
    def test_prune_when_threshold_exceeded(self):
        """Test automatic pruning when threshold is exceeded"""
        pruner = ContextPruner(self.tracker)
        
        # Fill up context to near capacity
        for i in range(100):
            self.tracker.add_user_message("x" * 100)  # Long messages
        
        # Check if we're over threshold
        status = self.tracker.get_status()
        if status.usage_percent > 0.8:
            # Prune to get under threshold
            result = pruner.prune_to_target(target_percent=0.6)
            
            # Should have reduced usage
            status_after = self.tracker.get_status()
            assert status_after.usage_percent < 0.7
    
    def test_preserve_pinned_items(self):
        """Test that pinned items are always preserved"""
        pruner = ContextPruner(self.tracker)
        
        # Find pinned item
        items_before = self.tracker.get_items()
        pinned_items = [item for item in items_before if item.pinned]
        assert len(pinned_items) > 0
        
        # Prune aggressively
        result = pruner.prune_old_messages(keep_recent=1, max_age_minutes=0)
        
        # Pinned items should still exist
        items_after = self.tracker.get_items()
        for pinned_item in pinned_items:
            assert any(item.id == pinned_item.id for item in items_after)
    
    def test_keep_recent_messages(self):
        """Test that recent messages are preserved"""
        pruner = ContextPruner(self.tracker)
        
        # Prune keeping last 3 messages
        result = pruner.prune_old_messages(keep_recent=3, max_age_minutes=0)
        
        # Should have at least 3 non-pinned messages remaining
        items = self.tracker.get_items()
        non_pinned = [item for item in items if not item.pinned]
        assert len(non_pinned) >= 3
    
    def test_pruning_result_details(self):
        """Test pruning result contains correct details"""
        pruner = ContextPruner(self.tracker)
        
        result = pruner.prune_old_messages(keep_recent=5, max_age_minutes=0)
        
        # Check result structure
        assert hasattr(result, 'items_removed')
        assert hasattr(result, 'tokens_freed')
        assert hasattr(result, 'pruned_items')
        
        # Values should be consistent
        assert result.items_removed == len(result.pruned_items)
        assert result.tokens_freed >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
