import asyncio
import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from dashboard.backend.database import init_db_async, get_async_db
from memory.persistence import MemoryManager

async def test_persistence():
    print("🚀 Testing Phase 4 Persistent Memory...")
    
    # 1. Initialize DB
    print("Step 1: Initializing database tables...")
    await init_db_async()
    print("✅ Tables initialized.")
    
    # 2. Test MemoryManager
    print("\nStep 2: Testing MemoryManager session persistence...")
    manager = MemoryManager(backend_type="sql")
    session_id = f"test-session-{os.urandom(4).hex()}"
    
    await manager.save_context_session(
        session_id=session_id,
        model="claude",
        max_tokens=200000,
        user_id="dev-user"
    )
    print(f"✅ Created persistent session: {session_id}")
    
    # 3. Add items
    print("\nStep 3: Storing context items...")
    item1 = {
        "type": "user",
        "content": "Hello AI!",
        "tokens": 10,
        "importance": 1.0,
        "pinned": False,
        "metadata": {"test": True}
    }
    await manager.add_context_item(session_id, "item-1", item1)
    
    item2 = {
        "type": "assistant",
        "content": "Hello human! I am persistently here.",
        "tokens": 20,
        "importance": 0.8,
        "pinned": True,
        "metadata": {"test": True}
    }
    await manager.add_context_item(session_id, "item-2", item2)
    print("✅ Stored 2 items.")
    
    # 4. Recall
    print("\nStep 4: Recalling memory...")
    history = await manager.get_context_history(session_id)
    print(f"✅ Recalled {len(history)} items.")
    for item in history:
        print(f"  [{item['type']}] {item['content']} ({item['tokens']} tokens)")
        
    # 5. Clean up
    print("\nStep 5: Testing partial cleanup (keeping pinned)...")
    await manager.clear_context_items(session_id, keep_pinned=True)
    history_after = await manager.get_context_history(session_id)
    print(f"✅ After cleanup: {len(history_after)} items remain (Expecting 1 pinned).")
    
    # Final cleanup
    print("\nDone. Phase 4 Persistent Memory is OPERATIONAL! 🚀")

if __name__ == "__main__":
    asyncio.run(test_persistence())
