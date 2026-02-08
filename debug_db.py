import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import sys

async def test_connection():
    try:
        print(f"Python: {sys.version}")
        import aiosqlite
        print(f"aiosqlite: {aiosqlite.__version__}")
        import sqlalchemy
        print(f"SQLAlchemy: {sqlalchemy.__version__}")
        
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
        async with engine.connect() as conn:
            result = await conn.execute(sqlalchemy.text("SELECT 1"))
            print(f"Result: {result.scalar()}")
        print("✅ Connection successful")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
