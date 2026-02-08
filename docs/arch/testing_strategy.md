# Testing Strategy: Phantom Neural Cortex (Backend)

**Version:** 2.0 (Feb 2026)  
**Status:** IMPLEMENTED

## Overview

The Phantom Neural Cortex utilizes a "Shift-Left" testing strategy, prioritizing fast, isolated integration tests that verify API contracts and database interactions without external dependencies.

## 1. Environment & Architecture

### In-Memory Isolation

To ensure test speed and reliability (especially on Windows), all backend tests utilize an **In-Memory SQLite** database.

* **Driver**: `aiosqlite` (async) for application logic, `sqlite3` (sync) for test setup.
* **Connection Pooling**: `StaticPool` is used to maintain the in-memory state throughout a single test session/transaction.

### Transactional Integrity

Each test function is wrapped in a database transaction:

1. `db_session` fixture starts a transaction.
2. The test executes (including API calls via `TestClient`).
3. The transaction is rolled back at the end of the test.
*Benefit*: Tests are guaranteed a clean state without the overhead of recreating tables for every test.

## 2. API Contract Testing

Integration tests for routers (e.g., `test_api_projects.py`) must verify:

* **Schema Compliance**: Incoming requests must match Pydantic models.
* **Enum Enforcement**: Valid values for `ProjectType`, `ProjectStatus`, etc.
* **HTTP Semantics**: Correct use of `GET`, `POST`, `PUT`, `DELETE`.
* **Error States**: `400` (Business logic violations), `404` (Not found), `422` (Validation).

## 3. Toolchain

* **Framework**: `pytest`
* **Async Support**: `pytest-asyncio`
* **Client**: `fastapi.testclient.TestClient` (Synchronous bridge for testing async endpoints)
* **Execution**: Run via `python -m pytest` to ensure environment consistency.

## 4. Best Practices

1. **No Hardcoded IDs**: Always use IDs returned from previous `POST` requests in the same test.
2. **Mocking**: External APIs (GitHub, OpenAI, etc.) should be mocked at the service layer if possible, though currently integration tests focus on the DB/API boundary.
3. **Enterprise Documentation**: Major test resolutions must be documented in `docs/incident_reports/`.
4. **XFail usage**: Use `@pytest.mark.xfail` for features in active development or documented requirements not yet implemented in the core logic.

## 5. Continuous Improvement

* **Next Step**: Implement `TestClient` for WebSocket testing in `test_websocket.py`.
* **Next Step**: Add coverage reporting via `pytest-cov`.
