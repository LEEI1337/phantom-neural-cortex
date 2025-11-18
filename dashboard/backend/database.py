"""
Database Configuration and Session Management

Async SQLAlchemy 2.0 with asyncpg driver for 2.5x performance improvement.
Supports both PostgreSQL (production) and SQLite (development).
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from typing import AsyncGenerator, Generator
import os
import logging

logger = logging.getLogger(__name__)

# Database URL Configuration
# PostgreSQL: postgresql+asyncpg://user:password@host:port/dbname
# SQLite: sqlite+aiosqlite:///./lazy_bird.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lazy_bird.db")

# Convert sync PostgreSQL URL to async if needed
if DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
elif DATABASE_URL.startswith("sqlite://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

logger.info(f"Database configured: {ASYNC_DATABASE_URL.split('@')[-1] if '@' in ASYNC_DATABASE_URL else 'SQLite'}")

# ============================================================================
# ASYNC ENGINE & SESSIONS (Primary - Production Use)
# ============================================================================

# Async Engine with optimized connection pool
# Different configurations for PostgreSQL vs SQLite
if "postgresql" in ASYNC_DATABASE_URL:
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=False,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={
            "server_settings": {"application_name": "lazy-bird-dashboard"}
        }
    )
else:
    # SQLite doesn't support pool_size/max_overflow
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )

# Async SessionLocal for dependency injection
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy-loading issues
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async dependency function for getting database sessions.

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()

    Yields:
        AsyncSession: Database session for async operations

    Raises:
        SQLAlchemyError: If database connection or transaction fails
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database transaction error: {e}")
            raise
        finally:
            await session.close()


# ============================================================================
# SYNC ENGINE & SESSIONS (Backward Compatibility - Migration Phase)
# ============================================================================

# Sync engine for backward compatibility during migration
sync_engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
    pool_size=10,  # Smaller pool for sync operations
    max_overflow=5,
)

# Sync SessionLocal for legacy endpoints
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Alias for backward compatibility (seed_data.py imports 'engine')
engine = sync_engine


def get_db() -> Generator[Session, None, None]:
    """
    Sync dependency function for getting database sessions (DEPRECATED).

    WARNING: This is deprecated. Use get_async_db() for new endpoints.
    Only kept for backward compatibility during migration phase.

    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    Yields:
        Session: Database session for sync operations
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Sync database transaction error: {e}")
        raise
    finally:
        db.close()


# ============================================================================
# DATABASE INITIALIZATION & UTILITIES
# ============================================================================

async def init_db_async():
    """
    Initialize database tables and seed initial data (async version).

    This should be called on application startup.

    Raises:
        Exception: If initialization or seeding fails
    """
    from models import Base

    # Create all tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created successfully")

    # Seed initial data
    try:
        from seed_data import seed_all_async
        async with AsyncSessionLocal() as session:
            await seed_all_async(session)
            await session.commit()
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.warning(f"Seeding failed (may already be seeded): {e}")


def init_db():
    """
    Initialize database tables and seed initial data (sync version - DEPRECATED).

    WARNING: Use init_db_async() instead for better performance.
    Only kept for backward compatibility.
    """
    from models import Base
    Base.metadata.create_all(bind=sync_engine)
    logger.info("Database initialized successfully (sync)")

    # Seed initial data
    try:
        from seed_data import seed_all
        db = SessionLocal()
        seed_all(db)
        db.close()
        logger.info("Database seeded successfully (sync)")
    except Exception as e:
        logger.warning(f"Seeding failed (may already be seeded): {e}")


async def reset_db_async():
    """
    Reset database - drop all tables and recreate (async version).

    WARNING: This deletes all data! Use only in development.

    Raises:
        Exception: If reset fails
    """
    from models import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    logger.warning("Database reset successfully (async) - ALL DATA DELETED")


def reset_db():
    """
    Reset database - drop all tables and recreate (sync version - DEPRECATED).

    WARNING: This deletes all data! Use only in development.
    Use reset_db_async() instead for better performance.
    """
    from models import Base
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)
    logger.warning("Database reset successfully (sync) - ALL DATA DELETED")


# ============================================================================
# HEALTH CHECK & MONITORING
# ============================================================================

async def check_db_health() -> dict:
    """
    Check database connection health.

    Returns:
        dict: Health status with connection pool info

    Example:
        >>> health = await check_db_health()
        >>> print(health['status'])
        'healthy'
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")

        pool = async_engine.pool

        return {
            "status": "healthy",
            "pool_size": pool.size(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "checked_in": pool.checkedin()
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# ============================================================================
# TRANSACTION UTILITIES
# ============================================================================

async def get_db_session() -> AsyncSession:
    """
    Get a new async database session (not for FastAPI dependencies).

    Usage for background tasks or manual session management:
        async with get_db_session() as session:
            result = await session.execute(select(Item))
            items = result.scalars().all()

    Returns:
        AsyncSession: New database session
    """
    return AsyncSessionLocal()


# ============================================================================
# MIGRATION HELPER
# ============================================================================

def get_engine_info() -> dict:
    """
    Get information about configured engines.

    Returns:
        dict: Engine configuration details
    """
    return {
        "async_url": ASYNC_DATABASE_URL.split('@')[-1] if '@' in ASYNC_DATABASE_URL else ASYNC_DATABASE_URL,
        "sync_url": DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL,
        "async_pool_size": async_engine.pool.size(),
        "sync_pool_size": sync_engine.pool.size(),
        "driver": "asyncpg" if "asyncpg" in ASYNC_DATABASE_URL else "aiosqlite",
    }
