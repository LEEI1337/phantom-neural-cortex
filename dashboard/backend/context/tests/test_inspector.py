"""
Unit tests for ContextInspector
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from context import ContextTracker, ContextInspector, ModelType


class TestContextInspector:
    """Test ContextInspector functionality"""
    
    def setup_method(self):
        """Setup test tracker"""
        self.tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        
        # Add sample content
        self.tracker.add_system_prompt("You are a helpful assistant.", pinned=True)
        self.tracker.add_user_message("Hello!")
        self.tracker.add_assistant_message("Hi there!")
        self.tracker.add_tool_call("grep 'test' src/", tool_name="grep")
        self.tracker.add_tool_result("src/test.py:1: test", tool_name="grep")
        
        self.inspector = ContextInspector(self.tracker)
    
    def test_initialization(self):
        """Test inspector initialization"""
        assert self.inspector.tracker == self.tracker
    
    def test_get_status_display(self):
        """Test status display formatting"""
        display = self.inspector.get_status_display()
        
        # Should contain key information
        assert "Context:" in display
        assert "tokens" in display
        assert "System:" in display
        assert "Messages:" in display
        assert "Tools:" in display
    
    def test_get_items_list(self):
        """Test items list formatting"""
        items_list = self.inspector.get_items_list()
        
        # Should contain all items
        assert "[System]" in items_list
        assert "[User]" in items_list
        assert "[Assistant]" in items_list
        assert "[Tool Call]" in items_list
        assert "[Tool Result]" in items_list
    
    def test_get_detailed_breakdown(self):
        """Test detailed breakdown formatting"""
        breakdown = self.inspector.get_detailed_breakdown()
        
        # Should contain detailed sections
        assert "Detailed Context Breakdown" in breakdown
        assert "System Prompt:" in breakdown
        assert "Conversation:" in breakdown
        assert "Tool Results:" in breakdown
        assert "tokens" in breakdown.lower()
    
    def test_get_inspection(self):
        """Test inspection data structure"""
        inspection = self.inspector.get_inspection()
        
        # Check structure
        assert hasattr(inspection, 'status')
        assert hasattr(inspection, 'items')
        assert hasattr(inspection, 'breakdown')
        
        # Check data
        assert inspection.status is not None
        assert len(inspection.items) > 0
        assert inspection.breakdown is not None
    
    def test_format_compact_command(self):
        """Test compact command formatting"""
        display = self.inspector.format_compact_result(
            tokens_before=1000,
            tokens_after=600,
            tokens_saved=400
        )
        
        # Should show before/after/saved
        assert "1000" in display or "1,000" in display
        assert "600" in display
        assert "400" in display
        assert "%" in display  # Percentage reduction


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
