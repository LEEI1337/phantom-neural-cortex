
import os
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import sys

async def test():
    print(f"Python executable: {sys.executable}")
    url = "sqlite+aiosqlite:///./test_repro.db"
    try:
        engine = create_async_engine(url)
        print("Engine created.")
        async with engine.connect() as conn:
            print("Connected successfully!")
    except Exception as e:
        print(f"Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
