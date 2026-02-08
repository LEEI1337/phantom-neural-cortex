import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "dashboard", "backend")))

from database import init_db_async

async def main():
    print("🚀 Initializing database with new Phase 4 Context models...")
    try:
        await init_db_async()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")

if __name__ == "__main__":
    asyncio.run(main())
