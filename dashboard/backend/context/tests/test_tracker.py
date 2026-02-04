"""
Unit tests for ContextTracker
"""

import pytest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from context import ContextTracker, ModelType, MessageType


class TestContextTracker:
    """Test ContextTracker functionality"""
    
    def test_initialization(self):
        """Test tracker initialization"""
        tracker = ContextTracker(session_id="test_session", model=ModelType.CLAUDE)
        
        assert tracker.session_id == "test_session"
        assert tracker.model == ModelType.CLAUDE
        status = tracker.get_status()
        assert status.total_tokens == 0
        assert status.usage_percent == 0.0
    
    def test_add_system_prompt(self):
        """Test adding system prompt"""
        tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        tracker.add_system_prompt("You are a helpful assistant.", pinned=True)
        
        status = tracker.get_status()
        assert status.system_tokens > 0
        assert status.item_count == 1
        
        # System prompt should be pinned
        items = tracker.get_items()
        assert len(items) == 1
        assert items[0].pinned is True
        assert items[0].type == MessageType.SYSTEM
    
    def test_add_user_message(self):
        """Test adding user message"""
        tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        tracker.add_user_message("Hello, how are you?")
        
        status = tracker.get_status()
        assert status.message_tokens > 0
        assert status.item_count == 1
        
        items = tracker.get_items()
        assert items[0].type == MessageType.USER
    
    def test_multiple_message_types(self):
        """Test tracking multiple message types"""
        tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        
        tracker.add_system_prompt("System prompt", pinned=True)
        tracker.add_user_message("User message")
        tracker.add_assistant_message("Assistant response")
        tracker.add_tool_call("tool call", tool_name="test")
        tracker.add_tool_result("tool result", tool_name="test")
        
        status = tracker.get_status()
        assert status.item_count == 5
        assert status.system_tokens > 0
        assert status.message_tokens > 0
        assert status.tool_tokens > 0
        assert status.total_tokens == (
            status.system_tokens + status.message_tokens + status.tool_tokens
        )
    
    def test_token_counting_accuracy(self):
        """Test token counting is reasonably accurate"""
        tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        
        # Simple message with known approximate token count
        message = "This is a test message with about ten words in it."
        tracker.add_user_message(message)
        
        status = tracker.get_status()
        # Should be between 10-20 tokens (rough estimate)
        assert 8 <= status.total_tokens <= 25
    
    def test_usage_percentage_calculation(self):
        """Test usage percentage calculation"""
        tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        
        # Add some content
        tracker.add_user_message("Short message")
        status = tracker.get_status()
        
        # Should be very small percentage
        assert 0 < status.usage_percent < 1.0
        
        # Max tokens should be model default
        assert status.max_tokens > 0
    
    def test_remove_item(self):
        """Test removing an item"""
        tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        
        tracker.add_user_message("Message 1")
        tracker.add_user_message("Message 2")
        
        items = tracker.get_items()
        assert len(items) == 2
        
        # Remove first item
        removed = tracker.remove_item(items[0].id)
        assert removed is True
        
        # Should have 1 item left
        items_after = tracker.get_items()
        assert len(items_after) == 1
        assert "Message 2" in items_after[0].content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
