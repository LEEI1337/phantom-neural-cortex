# Testing Strategy - Production Quality Assurance

**Version:** 1.0.0
**Status:** REQUIRED for Production

Comprehensive testing ensures **code reliability** - catch bugs early, deploy with confidence, maintain quality over time.

---

## Why Testing Matters

### The Problem Without Tests:

```python
# ❌ No tests - how do you know this works?
async def execute_task(task: Task):
    agent = select_agent(task)
    response = await agent.execute(task.prompt)
    return response

# Questions:
# - What if agent selection fails?
# - What if agent execution times out?
# - What if response is malformed?
# - Does it work with all agents?
# - Does circuit breaker work correctly?
```

**Consequences:**
- Bugs discovered in production
- Fear of refactoring
- Slow development (manual testing)
- Inconsistent behavior
- Cascading failures

### The Solution With Tests:

```python
# ✅ Comprehensive test coverage
@pytest.mark.asyncio
async def test_execute_task_success():
    """Test successful task execution with Claude."""
    task = Task(id="test_123", prompt="Test prompt")
    response = await orchestrator.execute_task(task, "session_1")

    assert response.agent == "claude"
    assert response.content is not None
    assert response.task_id == "test_123"


@pytest.mark.asyncio
async def test_execute_task_agent_failure_switches_to_fallback():
    """Test agent switching when primary agent fails."""
    # Mock Claude to fail
    with patch("orchestrator.execute_claude", side_effect=NetworkError()):
        response = await orchestrator.execute_task(task, "session_1")

    # Should switch to Gemini
    assert response.agent == "gemini"
```

**Benefits:**
- ✅ Catch bugs before production
- ✅ Safe refactoring
- ✅ Fast feedback loop
- ✅ Documentation through tests
- ✅ Confidence in deployments

---

## Test Structure

### Test Organization

```
dashboard/backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   │
│   ├── unit/                       # Unit tests (fast, isolated)
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_encryption.py
│   │   ├── test_circuit_breaker.py
│   │   └── orchestration/
│   │       ├── test_agent_selection.py
│   │       └── test_quality_assessment.py
│   │
│   ├── integration/                # Integration tests (slower, real dependencies)
│   │   ├── __init__.py
│   │   ├── test_database.py
│   │   ├── test_redis.py
│   │   ├── test_orchestrator_flow.py
│   │   └── test_api_endpoints.py
│   │
│   ├── e2e/                        # End-to-end tests (slowest, full system)
│   │   ├── __init__.py
│   │   ├── test_task_execution.py
│   │   └── test_websocket_events.py
│   │
│   └── fixtures/                   # Test data fixtures
│       ├── tasks.json
│       ├── projects.json
│       └── responses.json
```

### Test Configuration

```python
# tests/conftest.py

import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
import os

from database import Base, get_async_db
from main import app


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
async def test_db():
    """Create test database for each test."""
    # Use in-memory SQLite for tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # Cleanup
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_client(test_db):
    """Create test HTTP client with test database."""
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


# ============================================================================
# MOCK FIXTURES
# ============================================================================

@pytest.fixture
def mock_claude_response():
    """Mock Claude API response."""
    return {
        "content": "This is a test response from Claude",
        "tokens": 150,
        "cost": 0.0045,
        "model": "claude-sonnet-4-5"
    }


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response."""
    return {
        "content": "This is a test response from Gemini",
        "tokens": 120,
        "cost": 0.0,
        "model": "gemini-2.0-flash-thinking-exp"
    }


@pytest.fixture
def sample_task():
    """Sample task for testing."""
    from models import Task
    return Task(
        id="task_test_123",
        project_id="proj_test",
        prompt="Review code for security vulnerabilities",
        task_type="security",
        status="pending",
        assigned_agent="claude"
    )


@pytest.fixture
def sample_project():
    """Sample project for testing."""
    from models import Project
    return Project(
        id="proj_test",
        name="Test Project",
        description="A test project",
        status="active"
    )


# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ["TESTING"] = "true"
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    os.environ["REDIS_URL"] = "redis://localhost:6379/15"  # Test DB
    os.environ["FERNET_KEY"] = "test-key-for-testing-only-not-secure"
    yield
    # Cleanup
    del os.environ["TESTING"]
```

---

## Unit Tests

### Test 1: Circuit Breaker

```python
# tests/unit/test_circuit_breaker.py

import pytest
from orchestration.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_starts_closed():
    """Circuit breaker should start in CLOSED state."""
    breaker = CircuitBreaker(failure_threshold=5, timeout_duration=60)
    assert breaker.state == CircuitState.CLOSED
    assert breaker.failure_count == 0


def test_circuit_breaker_opens_after_threshold():
    """Circuit breaker should open after reaching failure threshold."""
    breaker = CircuitBreaker(failure_threshold=3, timeout_duration=60)

    # Simulate 3 failures
    for i in range(3):
        try:
            breaker.call(lambda: (_ for _ in ()).throw(Exception("Test error")))
        except Exception:
            pass

    # Should be OPEN now
    assert breaker.state == CircuitState.OPEN
    assert breaker.failure_count == 3


def test_circuit_breaker_blocks_requests_when_open():
    """Circuit breaker should block requests when OPEN."""
    breaker = CircuitBreaker(failure_threshold=2, timeout_duration=60)

    # Trigger 2 failures to open breaker
    for i in range(2):
        try:
            breaker.call(lambda: (_ for _ in ()).throw(Exception("Test")))
        except Exception:
            pass

    # Should block next request
    with pytest.raises(Exception, match="Circuit breaker is OPEN"):
        breaker.call(lambda: "success")


@pytest.mark.asyncio
async def test_circuit_breaker_resets_after_timeout():
    """Circuit breaker should reset to HALF_OPEN after timeout."""
    import asyncio
    from datetime import datetime, timedelta

    breaker = CircuitBreaker(failure_threshold=2, timeout_duration=1)

    # Open the breaker
    for i in range(2):
        try:
            await breaker.call_async(lambda: (_ for _ in ()).throw(Exception("Test")))
        except Exception:
            pass

    assert breaker.state == CircuitState.OPEN

    # Wait for timeout + a bit
    await asyncio.sleep(1.5)

    # Should transition to HALF_OPEN and allow test request
    result = await breaker.call_async(lambda: "success")
    assert result == "success"
    assert breaker.state == CircuitState.CLOSED


def test_circuit_breaker_resets_on_success():
    """Circuit breaker should reset failure count on success."""
    breaker = CircuitBreaker(failure_threshold=5, timeout_duration=60)

    # Simulate 2 failures
    for i in range(2):
        try:
            breaker.call(lambda: (_ for _ in ()).throw(Exception("Test")))
        except Exception:
            pass

    assert breaker.failure_count == 2

    # Success should reset
    breaker.call(lambda: "success")
    assert breaker.failure_count == 0
    assert breaker.state == CircuitState.CLOSED
```

### Test 2: Encryption

```python
# tests/unit/test_encryption.py

import pytest
from utils.encryption import EncryptionManager, encrypt_api_key, decrypt_api_key
from cryptography.fernet import InvalidToken


def test_encrypt_decrypt_round_trip():
    """Test encryption and decryption round trip."""
    encryption = EncryptionManager(key="test-key-for-testing-only-not-secure")

    plaintext = "sk-ant-api03-test-key-12345"
    encrypted = encryption.encrypt(plaintext)
    decrypted = encryption.decrypt(encrypted)

    assert decrypted == plaintext
    assert encrypted != plaintext  # Should be different


def test_encrypt_returns_different_ciphertext():
    """Test that encrypting same plaintext twice produces different ciphertext."""
    encryption = EncryptionManager()

    plaintext = "test-api-key"
    encrypted1 = encryption.encrypt(plaintext)
    encrypted2 = encryption.encrypt(plaintext)

    # Different ciphertexts due to random IV
    assert encrypted1 != encrypted2

    # But both decrypt to same plaintext
    assert encryption.decrypt(encrypted1) == plaintext
    assert encryption.decrypt(encrypted2) == plaintext


def test_decrypt_invalid_token_raises_error():
    """Test that decrypting invalid token raises ValueError."""
    encryption = EncryptionManager()

    with pytest.raises(ValueError, match="Invalid encrypted data"):
        encryption.decrypt("invalid-ciphertext")


def test_decrypt_with_wrong_key_raises_error():
    """Test that decrypting with wrong key raises error."""
    encryption1 = EncryptionManager(key="key1")
    encryption2 = EncryptionManager(key="key2")

    plaintext = "test-data"
    encrypted = encryption1.encrypt(plaintext)

    with pytest.raises(ValueError):
        encryption2.decrypt(encrypted)


def test_encrypt_empty_string():
    """Test encrypting empty string."""
    encryption = EncryptionManager()

    encrypted = encryption.encrypt("")
    decrypted = encryption.decrypt(encrypted)

    assert decrypted == ""


def test_encrypt_unicode_characters():
    """Test encrypting unicode characters."""
    encryption = EncryptionManager()

    plaintext = "测试🔐émojis"
    encrypted = encryption.encrypt(plaintext)
    decrypted = encryption.decrypt(encrypted)

    assert decrypted == plaintext
```

### Test 3: Agent Selection

```python
# tests/unit/orchestration/test_agent_selection.py

import pytest
from orchestration.orchestrator import CLIOrchestrator
from models import Task


@pytest.mark.asyncio
async def test_select_agent_for_security_task():
    """Test that security tasks are assigned to Claude."""
    orchestrator = CLIOrchestrator()

    task = Task(
        id="task_1",
        project_id="proj_1",
        prompt="Review code for SQL injection vulnerabilities",
        task_type="security",
        status="pending"
    )

    agent = await orchestrator._select_agent(task)
    assert agent.value == "claude"


@pytest.mark.asyncio
async def test_select_agent_for_simple_task():
    """Test that simple tasks are assigned to Gemini (free tier)."""
    orchestrator = CLIOrchestrator()

    task = Task(
        id="task_2",
        project_id="proj_1",
        prompt="Format this JSON",
        task_type="simple",
        status="pending"
    )

    agent = await orchestrator._select_agent(task)
    assert agent.value == "gemini"


@pytest.mark.asyncio
async def test_select_fallback_agent_excludes_failed_agents():
    """Test that fallback agent selection excludes already-failed agents."""
    orchestrator = CLIOrchestrator()

    task = Task(
        id="task_3",
        project_id="proj_1",
        prompt="Test task",
        task_type="general",
        status="pending"
    )

    fallback_agent = await orchestrator._select_fallback_agent(
        task,
        excluded_agents=["claude", "gemini"]
    )

    assert fallback_agent.value == "copilot"
```

---

## Integration Tests

### Test 1: Database Operations

```python
# tests/integration/test_database.py

import pytest
from models import Project, Task
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_project(test_db):
    """Test creating a project in database."""
    project = Project(
        id="proj_test_1",
        name="Test Project",
        description="A test project",
        status="active"
    )

    test_db.add(project)
    await test_db.commit()

    # Verify
    result = await test_db.execute(
        select(Project).filter(Project.id == "proj_test_1")
    )
    saved_project = result.scalar_one()

    assert saved_project.name == "Test Project"
    assert saved_project.status == "active"


@pytest.mark.asyncio
async def test_create_task_with_foreign_key(test_db):
    """Test creating task with foreign key to project."""
    # Create project first
    project = Project(
        id="proj_test_2",
        name="Test Project 2",
        status="active"
    )
    test_db.add(project)
    await test_db.commit()

    # Create task
    task = Task(
        id="task_test_1",
        project_id="proj_test_2",
        prompt="Test prompt",
        task_type="general",
        status="pending",
        assigned_agent="claude"
    )
    test_db.add(task)
    await test_db.commit()

    # Verify
    result = await test_db.execute(
        select(Task).filter(Task.id == "task_test_1")
    )
    saved_task = result.scalar_one()

    assert saved_task.project_id == "proj_test_2"
    assert saved_task.assigned_agent == "claude"


@pytest.mark.asyncio
async def test_cascade_delete_tasks_when_project_deleted(test_db):
    """Test that tasks are deleted when project is deleted (CASCADE)."""
    # Create project with task
    project = Project(id="proj_test_3", name="Test", status="active")
    task = Task(
        id="task_test_2",
        project_id="proj_test_3",
        prompt="Test",
        task_type="general",
        status="pending",
        assigned_agent="claude"
    )

    test_db.add(project)
    test_db.add(task)
    await test_db.commit()

    # Delete project
    await test_db.delete(project)
    await test_db.commit()

    # Task should be deleted too
    result = await test_db.execute(
        select(Task).filter(Task.id == "task_test_2")
    )
    deleted_task = result.scalar_one_or_none()

    assert deleted_task is None
```

### Test 2: API Endpoints

```python
# tests/integration/test_api_endpoints.py

import pytest


@pytest.mark.asyncio
async def test_health_endpoint(test_client):
    """Test /api/health endpoint."""
    response = await test_client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "redis" in data


@pytest.mark.asyncio
async def test_create_project_endpoint(test_client):
    """Test POST /api/projects endpoint."""
    payload = {
        "name": "Test API Project",
        "description": "Created via API",
        "status": "active"
    }

    response = await test_client.post("/api/projects", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test API Project"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_projects_endpoint(test_client, sample_project, test_db):
    """Test GET /api/projects endpoint."""
    # Create project in database
    test_db.add(sample_project)
    await test_db.commit()

    # Fetch via API
    response = await test_client.get("/api/projects")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["id"] == sample_project.id


@pytest.mark.asyncio
async def test_execute_task_validation_error(test_client):
    """Test task execution with invalid payload."""
    payload = {
        # Missing required fields
        "prompt": ""  # Empty prompt
    }

    response = await test_client.post("/api/orchestration/execute", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error_code"] == "VALIDATION_ERROR"
```

### Test 3: Orchestrator Flow

```python
# tests/integration/test_orchestrator_flow.py

import pytest
from unittest.mock import patch, AsyncMock
from orchestration.orchestrator import CLIOrchestrator
from models import Task


@pytest.mark.asyncio
async def test_orchestrator_executes_task_successfully(sample_task, mock_claude_response):
    """Test full orchestrator flow with successful execution."""
    orchestrator = CLIOrchestrator()

    # Mock the agent execution
    with patch.object(
        orchestrator,
        "_execute_agent_subprocess",
        return_value=AsyncMock(
            task_id=sample_task.id,
            agent="claude",
            content=mock_claude_response["content"],
            tokens=mock_claude_response["tokens"],
            cost=mock_claude_response["cost"]
        )
    ):
        response = await orchestrator.execute_task(sample_task, "session_123")

    assert response.agent == "claude"
    assert response.content == mock_claude_response["content"]
    assert response.tokens == mock_claude_response["tokens"]


@pytest.mark.asyncio
async def test_orchestrator_switches_agent_on_failure(sample_task, mock_gemini_response):
    """Test that orchestrator switches to fallback agent on failure."""
    orchestrator = CLIOrchestrator()

    # Mock Claude to fail, Gemini to succeed
    async def mock_execute(agent_name, task, session_id):
        if agent_name == "claude":
            raise Exception("Claude unavailable")
        elif agent_name == "gemini":
            return AsyncMock(
                task_id=task.id,
                agent="gemini",
                content=mock_gemini_response["content"]
            )

    with patch.object(orchestrator, "_execute_agent_subprocess", side_effect=mock_execute):
        response = await orchestrator.execute_task(sample_task, "session_123")

    # Should have switched to Gemini
    assert response.agent == "gemini"


@pytest.mark.asyncio
async def test_orchestrator_respects_circuit_breaker():
    """Test that orchestrator respects circuit breaker state."""
    orchestrator = CLIOrchestrator()

    # Open Claude's circuit breaker
    orchestrator.circuit_breakers["claude"].state = CircuitState.OPEN

    task = Task(
        id="task_cb_test",
        project_id="proj_test",
        prompt="Test",
        task_type="security",  # Would normally use Claude
        status="pending"
    )

    with patch.object(orchestrator, "_execute_agent_subprocess", return_value=AsyncMock()):
        response = await orchestrator.execute_task(task, "session_123")

    # Should NOT use Claude (circuit breaker open)
    assert response.agent != "claude"
```

---

## End-to-End Tests

### Test 1: Full Task Execution

```python
# tests/e2e/test_task_execution.py

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_task_execution_flow(test_client, test_db):
    """Test complete task execution flow from API to completion."""
    # 1. Create project
    project_payload = {
        "name": "E2E Test Project",
        "description": "End-to-end test",
        "status": "active"
    }
    project_response = await test_client.post("/api/projects", json=project_payload)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    # 2. Execute task
    task_payload = {
        "prompt": "Write a hello world function",
        "task_type": "coding",
        "project_id": project_id
    }

    # Mock agent execution for E2E test
    with patch("orchestration.orchestrator.CLIOrchestrator._execute_agent_subprocess"):
        task_response = await test_client.post(
            "/api/orchestration/execute",
            json=task_payload
        )

    assert task_response.status_code == 200
    task_data = task_response.json()
    assert "task_id" in task_data
    assert "content" in task_data

    # 3. Verify task in database
    task_id = task_data["task_id"]
    task_get_response = await test_client.get(f"/api/tasks/{task_id}")
    assert task_get_response.status_code == 200

    # 4. Check project tasks
    project_tasks_response = await test_client.get(
        f"/api/projects/{project_id}/tasks"
    )
    assert project_tasks_response.status_code == 200
    tasks = project_tasks_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
```

### Test 2: WebSocket Events

```python
# tests/e2e/test_websocket_events.py

import pytest
from fastapi.testclient import TestClient
import json


@pytest.mark.asyncio
async def test_websocket_task_updates():
    """Test WebSocket receives task status updates."""
    from main import app

    client = TestClient(app)

    with client.websocket_connect("/ws?channel=global") as websocket:
        # Trigger task execution in background
        # (In real test, would use async task)

        # Simulate receiving event
        data = websocket.receive_json()

        assert "event" in data
        assert data["event"] in ["task_started", "task_completed", "task_failed"]
        assert "task_id" in data
```

---

## Test Coverage

### Measuring Coverage

```bash
# Install pytest-cov
pip install pytest-cov

# Run tests with coverage
pytest --cov=dashboard/backend --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

**Coverage Goals:**
- Overall: 80% minimum
- Critical paths (orchestrator, circuit breaker): 95% minimum
- Models, schemas: 70% minimum

### Coverage Report Example

```
Name                                      Stmts   Miss  Cover
-------------------------------------------------------------
dashboard/backend/database.py                45      3    93%
dashboard/backend/models.py                  89      8    91%
dashboard/backend/orchestration/
  orchestrator.py                           234     23    90%
  circuit_breaker.py                         45      2    96%
  langfuse_integration.py                    56     12    79%
dashboard/backend/routers/
  orchestration.py                           67      8    88%
  projects.py                                34      4    88%
  tasks.py                                   28      3    89%
dashboard/backend/utils/
  encryption.py                              42      2    95%
-------------------------------------------------------------
TOTAL                                       640     65    90%
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml

name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      # PostgreSQL for integration tests
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: lazy_bird_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      # Redis for integration tests
      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd dashboard/backend
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio

      - name: Run unit tests
        run: |
          cd dashboard/backend
          pytest tests/unit/ -v --cov=. --cov-report=xml

      - name: Run integration tests
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:test@localhost:5432/lazy_bird_test
          REDIS_URL: redis://localhost:6379/15
        run: |
          cd dashboard/backend
          pytest tests/integration/ -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./dashboard/backend/coverage.xml
          fail_ci_if_error: true

      - name: Check coverage threshold
        run: |
          cd dashboard/backend
          pytest --cov=. --cov-fail-under=80
```

---

## Best Practices

### 1. Test Naming Convention

```python
# ✅ Good: Descriptive test names
def test_circuit_breaker_opens_after_five_failures()
def test_encryption_fails_with_invalid_key()
def test_orchestrator_switches_to_gemini_when_claude_unavailable()

# ❌ Bad: Vague test names
def test_circuit_breaker()
def test_encryption()
def test_orchestrator()
```

### 2. Arrange-Act-Assert Pattern

```python
@pytest.mark.asyncio
async def test_execute_task_with_quality_check():
    # Arrange
    task = Task(id="test_1", prompt="Test", task_type="general")
    orchestrator = CLIOrchestrator()
    expected_quality = 0.85

    # Act
    response = await orchestrator.execute_task(task, "session_1")

    # Assert
    assert response.quality >= expected_quality
    assert response.task_id == task.id
```

### 3. Use Fixtures for Common Setup

```python
@pytest.fixture
def orchestrator_with_open_breaker():
    """Orchestrator with Claude's circuit breaker open."""
    orchestrator = CLIOrchestrator()
    orchestrator.circuit_breakers["claude"].state = CircuitState.OPEN
    return orchestrator


def test_fallback_with_open_breaker(orchestrator_with_open_breaker):
    """Test fallback agent selection with open circuit breaker."""
    # Use pre-configured orchestrator
    ...
```

### 4. Mock External Dependencies

```python
@pytest.mark.asyncio
async def test_execute_task_with_mocked_agent():
    """Test orchestrator without calling real agents."""
    with patch("subprocess.run") as mock_subprocess:
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = b"Test response"

        response = await orchestrator.execute_task(task, "session_1")

        assert response.content == "Test response"
```

### 5. Test Error Scenarios

```python
@pytest.mark.asyncio
async def test_execute_task_handles_network_error():
    """Test that network errors are handled gracefully."""
    with patch("httpx.post", side_effect=NetworkError()):
        with pytest.raises(TaskExecutionError):
            await orchestrator.execute_task(task, "session_1")


@pytest.mark.asyncio
async def test_execute_task_retries_on_timeout():
    """Test that timeouts trigger retry logic."""
    call_count = 0

    async def mock_execute(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise TimeoutError()
        return "success"

    with patch("orchestrator._execute_agent", side_effect=mock_execute):
        response = await orchestrator.execute_task(task, "session_1")

    assert call_count == 3  # Retried twice, succeeded on third
```

---

## Performance Testing

### Load Testing with Locust

```python
# tests/performance/locustfile.py

from locust import HttpUser, task, between
import json


class PhantomNeuralCortexUser(HttpUser):
    """Simulate user load on the API."""
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    @task(3)
    def execute_task(self):
        """Execute a task (most common operation)."""
        payload = {
            "prompt": "Test prompt",
            "task_type": "general",
            "project_id": "proj_test"
        }
        self.client.post("/api/orchestration/execute", json=payload)

    @task(2)
    def list_projects(self):
        """List projects."""
        self.client.get("/api/projects")

    @task(1)
    def get_metrics(self):
        """Get metrics."""
        self.client.get("/api/metrics/summary")


# Run with:
# locust -f tests/performance/locustfile.py --host=http://localhost:1336
```

---

## Next Steps

1. ✅ Set up test structure
2. ✅ Write unit tests for critical components
3. ✅ Write integration tests for database and API
4. ✅ Write E2E tests for complete flows
5. ✅ Set up CI/CD pipeline with GitHub Actions
6. ✅ Configure coverage reporting
7. ✅ Add performance testing with Locust

---

**Documentation:**
- Pytest: https://docs.pytest.org/
- Pytest-asyncio: https://pytest-asyncio.readthedocs.io/
- Locust: https://docs.locust.io/
- Coverage.py: https://coverage.readthedocs.io/
