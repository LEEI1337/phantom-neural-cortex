"""
Enterprise Grade Test Configuration for Backend API Tests

Provides:
- In-memory SQLite database for fast, isolated tests
- Proper session management with transaction rollback
- FastAPI TestClient with dependency injection override
"""

import os
import sys
from pathlib import Path

# Add project root to python path FIRST
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Force in-memory test database URL BEFORE importing app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Import app modules after setting env var
from dashboard.backend.database import get_db
from dashboard.backend.models import Base

# Create dedicated sync engine for tests (in-memory, shared connection)
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Reuse single connection for in-memory DB
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test database schema once per session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Get a fresh DB session for each test function with rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Test client with overridden DB dependency.
    
    Each test gets an isolated database state via transaction rollback.
    """
    # Import app lazily to avoid circular imports
    from dashboard.backend.main import app
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
