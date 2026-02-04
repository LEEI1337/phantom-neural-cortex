"""
Unit tests for ContextCompactor
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from context import ContextTracker, ContextCompactor, ModelType


class TestContextCompactor:
    """Test ContextCompactor functionality"""
    
    def setup_method(self):
        """Setup test tracker with content to compact"""
        self.tracker = ContextTracker(session_id="test", model=ModelType.CLAUDE)
        
        # Add system prompt
        self.tracker.add_system_prompt("You are a helpful assistant.", pinned=True)
        
        # Add a long conversation
        for i in range(10):
            self.tracker.add_user_message(
                f"This is user message number {i} with some additional context "
                f"that makes it longer and more suitable for compaction testing."
            )
            self.tracker.add_assistant_message(
                f"This is assistant response number {i} with detailed information "
                f"that could be summarized to save tokens in the context window."
            )
        
        # Add long tool outputs
        self.tracker.add_tool_result(
            "Line 1: Some output\n" * 20,
            tool_name="grep"
        )
    
    def test_initialization(self):
        """Test compactor initialization"""
        compactor = ContextCompactor(self.tracker)
        assert compactor.tracker == self.tracker
    
    def test_basic_compaction(self):
        """Test basic compaction reduces tokens"""
        compactor = ContextCompactor(self.tracker)
        
        # Get initial state
        status_before = self.tracker.get_status()
        tokens_before = status_before.total_tokens
        
        # Compact
        result = compactor.compact()
        
        # Should have saved tokens
        status_after = self.tracker.get_status()
        tokens_after = status_after.total_tokens
        
        assert result.tokens_saved > 0
        assert tokens_after < tokens_before
        assert result.items_compacted > 0
    
    def test_compression_ratio(self):
        """Test compression ratio calculation"""
        compactor = ContextCompactor(self.tracker)
        
        result = compactor.compact()
        
        # Compression ratio should be between 0 and 1
        assert 0 <= result.compression_ratio <= 1.0
        
        # If tokens were saved, ratio should be > 0
        if result.tokens_saved > 0:
            assert result.compression_ratio > 0
    
    def test_compact_preserves_important_info(self):
        """Test that compaction preserves important information"""
        compactor = ContextCompactor(self.tracker)
        
        # Get initial items
        items_before = self.tracker.get_items()
        
        # Compact
        result = compactor.compact()
        
        # Pinned items should remain
        items_after = self.tracker.get_items()
        pinned_before = [item for item in items_before if item.pinned]
        pinned_after = [item for item in items_after if item.pinned]
        
        assert len(pinned_after) >= len(pinned_before)
    
    def test_compact_tool_outputs(self):
        """Test compacting tool outputs specifically"""
        compactor = ContextCompactor(self.tracker)
        
        # Get initial tool tokens
        status_before = self.tracker.get_status()
        tool_tokens_before = status_before.tool_tokens
        
        # Compact
        result = compactor.compact()
        
        # Tool tokens should be reduced (or at least not increased)
        status_after = self.tracker.get_status()
        assert status_after.tool_tokens <= tool_tokens_before
    
    def test_compaction_idempotent(self):
        """Test that compacting twice doesn't break things"""
        compactor = ContextCompactor(self.tracker)
        
        # First compaction
        result1 = compactor.compact()
        status1 = self.tracker.get_status()
        
        # Second compaction
        result2 = compactor.compact()
        status2 = self.tracker.get_status()
        
        # Second compaction should save fewer tokens (already compressed)
        assert result2.tokens_saved <= result1.tokens_saved
    
    def test_compaction_result_structure(self):
        """Test compaction result has correct structure"""
        compactor = ContextCompactor(self.tracker)
        
        result = compactor.compact()
        
        # Check result attributes
        assert hasattr(result, 'tokens_saved')
        assert hasattr(result, 'compression_ratio')
        assert hasattr(result, 'items_compacted')
        assert hasattr(result, 'summary')
        
        # Values should be valid
        assert result.tokens_saved >= 0
        assert 0 <= result.compression_ratio <= 1.0
        assert result.items_compacted >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
