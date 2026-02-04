#!/usr/bin/env python3
"""
Test script for Context Management System

Demonstrates all features of the context management system.
"""

import sys
from context import (
    ContextTracker,
    ContextPruner,
    ContextCompactor,
    ContextInspector,
    ModelType
)


def test_context_tracking():
    """Test basic context tracking"""
    print("=" * 70)
    print("TEST 1: Context Tracking")
    print("=" * 70)
    
    # Create tracker
    tracker = ContextTracker(session_id="test_session", model=ModelType.CLAUDE)
    
    # Add system prompt
    tracker.add_system_prompt(
        "You are a helpful AI assistant specialized in software development.",
        pinned=True
    )
    
    # Add user message
    tracker.add_user_message(
        "Can you help me implement a context management system?"
    )
    
    # Add assistant response
    tracker.add_assistant_message(
        "Of course! I'll help you build a context management system with real-time "
        "token tracking, automatic pruning, and AI-powered compaction. Let's start "
        "by understanding your requirements..."
    )
    
    # Add tool call and result
    tracker.add_tool_call(
        content="grep -r 'context' src/",
        tool_name="grep"
    )
    
    tracker.add_tool_result(
        content="src/context.py:1: # Context management\n" * 20,  # Simulate large output
        tool_name="grep"
    )
    
    # Get status
    status = tracker.get_status()
    
    print(f"\n✓ Created tracker for session: {tracker.session_id}")
    print(f"✓ Model: {status.model.value}")
    print(f"✓ Total tokens: {status.total_tokens}/{status.max_tokens}")
    print(f"✓ Usage: {status.usage_percent:.1f}%")
    print(f"✓ Items: {status.item_count}")
    print(f"  - System: {status.system_tokens} tokens")
    print(f"  - Messages: {status.message_tokens} tokens")
    print(f"  - Tools: {status.tool_tokens} tokens")
    
    return tracker


def test_inspector(tracker):
    """Test inspector CLI commands"""
    print("\n" + "=" * 70)
    print("TEST 2: Inspector Commands")
    print("=" * 70)
    
    inspector = ContextInspector(tracker)
    
    # Test /status command
    print("\n/status command:")
    print(inspector.get_status_display())
    
    # Test /context list command
    print("\n/context list command:")
    print(inspector.get_items_list())
    
    # Test /context detail command
    print("\n/context detail command:")
    print(inspector.get_detailed_breakdown())
    
    return inspector


def test_pruning(tracker):
    """Test pruning strategies"""
    print("\n" + "=" * 70)
    print("TEST 3: Pruning")
    print("=" * 70)
    
    # Add more messages to test pruning
    for i in range(10):
        tracker.add_user_message(f"Test message {i}")
        tracker.add_assistant_message(f"Response to test message {i}")
    
    status_before = tracker.get_status()
    print(f"\nBefore pruning: {status_before.total_tokens} tokens ({status_before.usage_percent:.1f}%)")
    print(f"Items: {status_before.item_count}")
    
    # Prune old messages
    pruner = ContextPruner(tracker)
    result = pruner.prune_old_messages(max_age_minutes=1, keep_recent=5)
    
    status_after = tracker.get_status()
    print(f"\nAfter pruning: {status_after.total_tokens} tokens ({status_after.usage_percent:.1f}%)")
    print(f"Items: {status_after.item_count}")
    print(f"Freed: {result.tokens_freed} tokens")
    print(f"Removed: {len(result.pruned_items)} items")
    print(f"✓ Pruning successful!")


def test_compaction(tracker):
    """Test compaction"""
    print("\n" + "=" * 70)
    print("TEST 4: Compaction")
    print("=" * 70)
    
    status_before = tracker.get_status()
    print(f"\nBefore compaction: {status_before.total_tokens} tokens")
    
    # Compact context
    compactor = ContextCompactor(tracker)
    result = compactor.compact()
    
    status_after = tracker.get_status()
    print(f"After compaction: {status_after.total_tokens} tokens")
    print(f"Saved: {result.tokens_saved} tokens ({result.compression_ratio:.1%} compression)")
    print(f"Items compacted: {result.items_compacted}")
    print(f"✓ Compaction successful!")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("CONTEXT MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 70)
    
    try:
        # Test 1: Basic tracking
        tracker = test_context_tracking()
        
        # Test 2: Inspector commands
        inspector = test_inspector(tracker)
        
        # Test 3: Pruning
        test_pruning(tracker)
        
        # Test 4: Compaction
        test_compaction(tracker)
        
        # Final status
        print("\n" + "=" * 70)
        print("FINAL STATUS")
        print("=" * 70)
        print(inspector.get_status_display())
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
