# Error Handling & Retry Strategy - Production Resilience

**Version:** 1.0.0
**Status:** REQUIRED for Production

Comprehensive error handling ensures **graceful degradation** - handle failures elegantly, retry intelligently, never crash unexpectedly.

---

## Why Error Handling Matters

### The Problem:

```python
# ❌ BAD: No error handling
async def execute_task(task: Task):
    response = await agent.execute(task.prompt)  # 💥 Network error crashes entire system
    return response
```

**Consequences:**
- User loses work
- System becomes unavailable
- No visibility into what went wrong
- Can't recover automatically
- Cascading failures

### The Solution:

```python
# ✅ GOOD: Comprehensive error handling
async def execute_task(task: Task):
    for attempt in range(1, 4):  # Retry up to 3 times
        try:
            response = await agent.execute(task.prompt)
            return response
        except NetworkError as e:
            if attempt < 3:
                logger.warning(f"Network error on attempt {attempt}, retrying...")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Task failed after 3 attempts: {e}")
                raise TaskExecutionError(f"Failed to execute task: {e}") from e
        except ValidationError as e:
            # Don't retry validation errors
            logger.error(f"Invalid task configuration: {e}")
            raise
```

**Benefits:**
- ✅ Graceful degradation
- ✅ Automatic recovery from transient errors
- ✅ Clear error messages
- ✅ System remains stable
- ✅ User experience preserved

---

## Error Classification

### 1. Transient Errors (Retriable)

**Definition:** Temporary failures that may succeed on retry

**Examples:**
- Network timeouts
- API rate limits (429)
- Temporary service unavailability (503)
- Database connection pool exhausted
- Redis connection timeout

**Strategy:** Retry with exponential backoff

```python
class TransientError(Exception):
    """Temporary error that may succeed on retry."""
    pass


TRANSIENT_HTTP_CODES = {408, 429, 500, 502, 503, 504}

def is_transient_error(e: Exception) -> bool:
    """Check if error is transient and retriable."""
    if isinstance(e, (TimeoutError, ConnectionError, TransientError)):
        return True

    if isinstance(e, HTTPException) and e.status_code in TRANSIENT_HTTP_CODES:
        return True

    return False
```

### 2. Permanent Errors (Non-Retriable)

**Definition:** Failures that won't succeed on retry

**Examples:**
- Invalid API key (401, 403)
- Invalid request format (400)
- Resource not found (404)
- Validation errors
- Business logic errors

**Strategy:** Fail fast, return clear error message

```python
class PermanentError(Exception):
    """Permanent error that won't succeed on retry."""
    pass


PERMANENT_HTTP_CODES = {400, 401, 403, 404, 405, 410}

def is_permanent_error(e: Exception) -> bool:
    """Check if error is permanent (don't retry)."""
    if isinstance(e, (ValidationError, ValueError, PermanentError)):
        return True

    if isinstance(e, HTTPException) and e.status_code in PERMANENT_HTTP_CODES:
        return True

    return False
```

### 3. Resource Exhaustion (Throttle)

**Definition:** System resources depleted

**Examples:**
- Database connection pool full
- Memory limit reached
- CPU overloaded
- Too many concurrent requests

**Strategy:** Throttle, queue, or reject new requests

```python
class ResourceExhaustedError(Exception):
    """System resources exhausted."""
    pass
```

---

## Retry Patterns

### Pattern 1: Exponential Backoff

**Use Case:** Transient network errors, API rate limits

```python
import asyncio
from typing import Callable, Any, Type
import logging

logger = logging.getLogger(__name__)


async def retry_with_exponential_backoff(
    func: Callable,
    *args,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    **kwargs
) -> Any:
    """
    Retry function with exponential backoff.

    Args:
        func: Async function to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential backoff (usually 2)
        exceptions: Tuple of exceptions to catch and retry

    Returns:
        Function result

    Raises:
        Last exception if all retries exhausted

    Example:
        >>> result = await retry_with_exponential_backoff(
        ...     agent.execute,
        ...     task,
        ...     max_retries=3,
        ...     exceptions=(NetworkError, TimeoutError)
        ... )
    """
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            last_exception = e

            if attempt == max_retries:
                logger.error(f"All {max_retries} retry attempts exhausted")
                raise

            # Calculate delay with exponential backoff
            delay = min(initial_delay * (exponential_base ** (attempt - 1)), max_delay)

            logger.warning(
                f"Attempt {attempt}/{max_retries} failed: {e}. "
                f"Retrying in {delay:.2f}s..."
            )

            await asyncio.sleep(delay)

    # Should never reach here, but just in case
    raise last_exception


# Usage
async def execute_with_retry(task: Task):
    """Execute task with automatic retry."""
    return await retry_with_exponential_backoff(
        agent.execute,
        task.prompt,
        max_retries=3,
        initial_delay=2.0,
        exceptions=(NetworkError, TimeoutError)
    )
```

**Backoff Timing:**
```
Attempt 1: Immediate
Attempt 2: 2s delay
Attempt 3: 4s delay
Attempt 4: 8s delay
Attempt 5: 16s delay
```

### Pattern 2: Jittered Backoff

**Use Case:** Prevent thundering herd (many clients retrying simultaneously)

```python
import random


async def retry_with_jitter(
    func: Callable,
    *args,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    **kwargs
) -> Any:
    """
    Retry with jittered exponential backoff.

    Adds randomness to prevent synchronized retries from multiple clients.
    """
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e

            if attempt == max_retries:
                raise

            # Exponential backoff with jitter
            max_backoff = min(base_delay * (2 ** (attempt - 1)), max_delay)
            delay = random.uniform(0, max_backoff)

            logger.warning(f"Retry attempt {attempt} in {delay:.2f}s")
            await asyncio.sleep(delay)

    raise last_exception


# Usage
result = await retry_with_jitter(
    api_call,
    max_retries=5,
    base_delay=1.0,
    max_delay=30.0
)
```

### Pattern 3: Circuit Breaker (Already Implemented!)

**Use Case:** Prevent cascading failures from unavailable services

**Location:** `dashboard/backend/orchestration/circuit_breaker.py`

```python
from orchestration.circuit_breaker import CircuitBreaker, CircuitState

# Create circuit breaker per agent
claude_breaker = CircuitBreaker(
    failure_threshold=5,  # Open after 5 failures
    timeout_duration=60,  # Wait 60s before retry
    expected_exception=Exception
)


async def execute_with_circuit_breaker(task: Task):
    """Execute task with circuit breaker protection."""
    try:
        return await claude_breaker.call_async(
            agent.execute,
            task.prompt
        )
    except Exception as e:
        if claude_breaker.state == CircuitState.OPEN:
            logger.error("Circuit breaker OPEN - switching to backup agent")
            # Switch to Gemini or Copilot
            return await execute_with_backup_agent(task)
        raise
```

**Circuit Breaker States:**

```
CLOSED (Normal)
   ↓ (5 failures)
OPEN (Blocked)
   ↓ (60s timeout)
HALF_OPEN (Testing)
   ↓ (1 success)
CLOSED (Recovered)
```

### Pattern 4: Fallback Chain

**Use Case:** Try multiple agents in sequence until one succeeds

```python
from typing import List, Callable


async def execute_with_fallback_chain(
    task: Task,
    agents: List[Callable],
    agent_names: List[str]
) -> Any:
    """
    Try multiple agents in sequence until one succeeds.

    Args:
        task: Task to execute
        agents: List of agent execute functions
        agent_names: List of agent names for logging

    Returns:
        First successful response

    Raises:
        Exception: If all agents fail
    """
    errors = []

    for agent, agent_name in zip(agents, agent_names):
        try:
            logger.info(f"Trying agent: {agent_name}")
            response = await agent(task.prompt)
            logger.info(f"Agent {agent_name} succeeded")
            return response
        except Exception as e:
            logger.warning(f"Agent {agent_name} failed: {e}")
            errors.append((agent_name, e))
            continue

    # All agents failed
    error_summary = "\n".join([f"{name}: {err}" for name, err in errors])
    raise Exception(f"All agents failed:\n{error_summary}")


# Usage
response = await execute_with_fallback_chain(
    task,
    agents=[execute_claude, execute_gemini, execute_copilot],
    agent_names=["claude", "gemini", "copilot"]
)
```

### Pattern 5: Timeout Protection

**Use Case:** Prevent hanging requests

```python
async def execute_with_timeout(
    func: Callable,
    *args,
    timeout_seconds: float = 30.0,
    **kwargs
) -> Any:
    """
    Execute function with timeout.

    Args:
        func: Async function to execute
        timeout_seconds: Timeout in seconds

    Returns:
        Function result

    Raises:
        asyncio.TimeoutError: If function exceeds timeout
    """
    try:
        return await asyncio.wait_for(
            func(*args, **kwargs),
            timeout=timeout_seconds
        )
    except asyncio.TimeoutError:
        logger.error(f"Function timed out after {timeout_seconds}s")
        raise


# Usage with retry
async def execute_task_safely(task: Task):
    """Execute with timeout and retry."""
    return await retry_with_exponential_backoff(
        execute_with_timeout,
        agent.execute,
        task.prompt,
        timeout_seconds=30.0,
        max_retries=3,
        exceptions=(asyncio.TimeoutError, NetworkError)
    )
```

---

## Comprehensive Error Handling in Orchestrator

### Enhanced Orchestrator with Error Handling

```python
# dashboard/backend/orchestration/orchestrator.py

import asyncio
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TaskExecutionError(Exception):
    """Task execution failed."""
    pass


class AgentUnavailableError(Exception):
    """Agent is unavailable."""
    pass


class CLIOrchestrator:
    """Multi-agent orchestrator with comprehensive error handling."""

    def __init__(self):
        self.circuit_breakers = {
            "claude": CircuitBreaker(failure_threshold=5, timeout_duration=60),
            "gemini": CircuitBreaker(failure_threshold=5, timeout_duration=60),
            "copilot": CircuitBreaker(failure_threshold=5, timeout_duration=60),
        }
        self.max_agent_switches = 3
        self.task_timeout = 300  # 5 minutes

    async def execute_task(
        self,
        task: Task,
        session_id: str
    ) -> TaskResponse:
        """
        Execute task with comprehensive error handling.

        Error Handling Strategy:
        1. Try primary agent with timeout and retry
        2. If circuit breaker opens, try fallback agents
        3. Track agent switches and quality
        4. Return detailed error if all attempts fail
        """
        start_time = datetime.utcnow()
        agent_attempts = []

        try:
            # Select initial agent
            selected_agent = await self._select_agent(task)

            # Execute with fallback chain
            for attempt in range(self.max_agent_switches + 1):
                agent_name = selected_agent.value
                agent_attempts.append(agent_name)

                logger.info(f"Attempt {attempt + 1}: Executing with {agent_name}")

                try:
                    # Check circuit breaker state
                    breaker = self.circuit_breakers[agent_name]
                    if breaker.state == CircuitState.OPEN:
                        raise AgentUnavailableError(f"{agent_name} circuit breaker is OPEN")

                    # Execute with timeout and retry
                    response = await self._execute_agent_with_retry(
                        agent_name,
                        task,
                        session_id
                    )

                    # Success!
                    logger.info(f"Task completed successfully with {agent_name}")
                    return response

                except AgentUnavailableError as e:
                    logger.warning(f"Agent {agent_name} unavailable: {e}")

                    if attempt < self.max_agent_switches:
                        # Try fallback agent
                        selected_agent = await self._select_fallback_agent(
                            task,
                            excluded_agents=agent_attempts
                        )
                        logger.info(f"Switching to fallback agent: {selected_agent.value}")
                        continue
                    else:
                        raise TaskExecutionError(
                            f"All agents exhausted after {attempt + 1} attempts"
                        )

                except ValidationError as e:
                    # Don't retry validation errors
                    logger.error(f"Validation error: {e}")
                    raise TaskExecutionError(f"Invalid task configuration: {e}") from e

                except asyncio.TimeoutError:
                    logger.error(f"Agent {agent_name} timed out")

                    # Mark as failure in circuit breaker
                    breaker._on_failure()

                    if attempt < self.max_agent_switches:
                        selected_agent = await self._select_fallback_agent(
                            task,
                            excluded_agents=agent_attempts
                        )
                        continue
                    else:
                        raise TaskExecutionError("Task execution timed out")

                except Exception as e:
                    logger.error(f"Unexpected error with {agent_name}: {e}")

                    # Mark as failure
                    breaker._on_failure()

                    if attempt < self.max_agent_switches:
                        selected_agent = await self._select_fallback_agent(
                            task,
                            excluded_agents=agent_attempts
                        )
                        continue
                    else:
                        raise

        except Exception as e:
            # Final catch-all
            duration = (datetime.utcnow() - start_time).total_seconds()

            logger.error(
                f"Task execution failed after {duration:.2f}s. "
                f"Attempted agents: {', '.join(agent_attempts)}"
            )

            # Track failure in database
            await self._track_task_failure(
                task_id=task.id,
                error=str(e),
                attempted_agents=agent_attempts,
                duration=duration
            )

            # Emit failure event
            await emit_task_failed(
                task_id=task.id,
                error=str(e),
                attempted_agents=agent_attempts
            )

            raise TaskExecutionError(
                f"Task execution failed: {e}. "
                f"Attempted agents: {', '.join(agent_attempts)}"
            ) from e

    async def _execute_agent_with_retry(
        self,
        agent_name: str,
        task: Task,
        session_id: str,
        max_retries: int = 3
    ) -> TaskResponse:
        """
        Execute agent with exponential backoff retry.

        Retries on:
        - Network errors
        - Timeouts
        - Transient API errors (429, 503)

        Does NOT retry on:
        - Invalid API key (401)
        - Validation errors (400)
        - Not found (404)
        """
        breaker = self.circuit_breakers[agent_name]

        return await retry_with_exponential_backoff(
            self._execute_agent,
            agent_name,
            task,
            session_id,
            max_retries=max_retries,
            initial_delay=2.0,
            max_delay=30.0,
            exceptions=(NetworkError, TimeoutError, TransientError)
        )

    async def _execute_agent(
        self,
        agent_name: str,
        task: Task,
        session_id: str
    ) -> TaskResponse:
        """Execute single agent with timeout and circuit breaker."""
        breaker = self.circuit_breakers[agent_name]

        # Execute with timeout
        response = await breaker.call_async(
            execute_with_timeout,
            self._execute_agent_subprocess,
            agent_name,
            task,
            session_id,
            timeout_seconds=self.task_timeout
        )

        return response

    async def _execute_agent_subprocess(
        self,
        agent_name: str,
        task: Task,
        session_id: str
    ) -> TaskResponse:
        """Execute agent subprocess (claude.cmd, gemini, copilot)."""
        # Fetch API key from database
        api_key = await self._get_api_key(agent_name)

        # Set up environment
        env = os.environ.copy()
        env[f"{agent_name.upper()}_API_KEY"] = api_key

        # Execute subprocess
        try:
            if agent_name == "claude":
                cmd = ["claude", "-p", task.prompt]
            elif agent_name == "gemini":
                cmd = ["gemini", "--prompt", task.prompt]
            elif agent_name == "copilot":
                cmd = ["copilot", task.prompt]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise TaskExecutionError(
                    f"Agent {agent_name} failed with code {process.returncode}: "
                    f"{stderr.decode()}"
                )

            # Parse response
            output = stdout.decode()

            return TaskResponse(
                task_id=task.id,
                agent=agent_name,
                content=output,
                session_id=session_id,
                timestamp=datetime.utcnow()
            )

        except FileNotFoundError:
            raise AgentUnavailableError(f"Agent CLI not found: {agent_name}")
        except Exception as e:
            raise TaskExecutionError(f"Agent execution failed: {e}") from e
        finally:
            # Clear API key from memory
            if f"{agent_name.upper()}_API_KEY" in env:
                del env[f"{agent_name.upper()}_API_KEY"]

    async def _track_task_failure(
        self,
        task_id: str,
        error: str,
        attempted_agents: List[str],
        duration: float
    ):
        """Track task failure in database for analytics."""
        async with AsyncSessionLocal() as db:
            failure_record = TaskFailure(
                id=str(uuid.uuid4()),
                task_id=task_id,
                error_message=error,
                attempted_agents=",".join(attempted_agents),
                duration=duration,
                timestamp=datetime.utcnow()
            )
            db.add(failure_record)
            await db.commit()
```

---

## Error Response Format

### Standard Error Response

```python
from pydantic import BaseModel
from typing import Optional, List


class ErrorDetail(BaseModel):
    """Detailed error information."""
    code: str  # "VALIDATION_ERROR", "NETWORK_ERROR", "AGENT_UNAVAILABLE"
    message: str  # Human-readable error message
    field: Optional[str] = None  # Field that caused error (for validation)
    details: Optional[dict] = None  # Additional context


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str  # Short error description
    error_code: str  # Machine-readable error code
    details: ErrorDetail  # Detailed error information
    timestamp: str  # ISO 8601 timestamp
    request_id: str  # Request ID for tracking
    retry_after: Optional[int] = None  # Seconds to wait before retry (for 429)


# Example error responses

# Validation Error (400)
{
    "error": "Invalid task configuration",
    "error_code": "VALIDATION_ERROR",
    "details": {
        "code": "INVALID_PROMPT",
        "message": "Prompt cannot be empty",
        "field": "prompt"
    },
    "timestamp": "2025-11-10T12:00:00Z",
    "request_id": "req_abc123"
}

# Rate Limit (429)
{
    "error": "Rate limit exceeded",
    "error_code": "RATE_LIMIT_EXCEEDED",
    "details": {
        "code": "TOO_MANY_REQUESTS",
        "message": "Maximum 100 requests per minute exceeded"
    },
    "timestamp": "2025-11-10T12:00:00Z",
    "request_id": "req_xyz789",
    "retry_after": 60
}

# Agent Unavailable (503)
{
    "error": "Service temporarily unavailable",
    "error_code": "AGENT_UNAVAILABLE",
    "details": {
        "code": "CIRCUIT_BREAKER_OPEN",
        "message": "Claude agent circuit breaker is open",
        "details": {
            "agent": "claude",
            "failure_count": 5,
            "retry_after": 45
        }
    },
    "timestamp": "2025-11-10T12:00:00Z",
    "request_id": "req_def456"
}
```

### FastAPI Exception Handlers

```python
# dashboard/backend/main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uuid
from datetime import datetime


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors (400)."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "details": {
                "code": "INVALID_REQUEST",
                "message": "Request validation failed",
                "details": exc.errors()
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    )


@app.exception_handler(TaskExecutionError)
async def task_execution_error_handler(request: Request, exc: TaskExecutionError):
    """Handle task execution errors (500)."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Task execution failed",
            "error_code": "TASK_EXECUTION_ERROR",
            "details": {
                "code": "EXECUTION_FAILED",
                "message": str(exc)
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    )


@app.exception_handler(AgentUnavailableError)
async def agent_unavailable_error_handler(request: Request, exc: AgentUnavailableError):
    """Handle agent unavailable errors (503)."""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Service temporarily unavailable",
            "error_code": "AGENT_UNAVAILABLE",
            "details": {
                "code": "CIRCUIT_BREAKER_OPEN",
                "message": str(exc)
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4()),
            "retry_after": 60
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected errors (500)."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "details": {
                "code": "UNEXPECTED_ERROR",
                "message": "An unexpected error occurred"
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    )
```

---

## Monitoring & Alerting

### Error Metrics

Track error rates and types:

```python
from prometheus_client import Counter, Histogram

# Error counters
error_counter = Counter(
    "errors_total",
    "Total number of errors",
    ["error_type", "agent", "severity"]
)

# Retry counters
retry_counter = Counter(
    "retries_total",
    "Total number of retry attempts",
    ["agent", "reason"]
)

# Circuit breaker state
circuit_breaker_state = Gauge(
    "circuit_breaker_state",
    "Circuit breaker state (0=closed, 1=half_open, 2=open)",
    ["agent"]
)


# Track errors
def track_error(error_type: str, agent: str, severity: str):
    """Track error in Prometheus."""
    error_counter.labels(
        error_type=error_type,
        agent=agent,
        severity=severity
    ).inc()


# Track retries
def track_retry(agent: str, reason: str):
    """Track retry attempt."""
    retry_counter.labels(agent=agent, reason=reason).inc()
```

### Alerting Rules (Prometheus)

```yaml
# monitoring/prometheus/alerts.yml

groups:
  - name: error_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(errors_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"

      # Circuit breaker open
      - alert: CircuitBreakerOpen
        expr: circuit_breaker_state{agent="claude"} == 2
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Circuit breaker open for {{ $labels.agent }}"
          description: "Agent {{ $labels.agent }} is unavailable"

      # Too many retries
      - alert: HighRetryRate
        expr: rate(retries_total[5m]) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High retry rate detected"
          description: "Retry rate is {{ $value }} retries/sec"
```

---

## Best Practices Checklist

- [ ] Classify errors (transient vs permanent)
- [ ] Implement exponential backoff for retries
- [ ] Use circuit breakers for external services
- [ ] Set appropriate timeouts for all operations
- [ ] Return structured error responses
- [ ] Log errors with sufficient context
- [ ] Track error metrics (Prometheus)
- [ ] Set up alerting for critical errors
- [ ] Implement fallback agents
- [ ] Never expose internal error details to users
- [ ] Test error scenarios in integration tests

---

## Next Steps

1. ✅ Implement error classification
2. ✅ Add retry utilities with exponential backoff
3. ✅ Enhance orchestrator with comprehensive error handling
4. ✅ Set up structured error responses
5. ✅ Add error tracking and monitoring
6. ✅ Configure alerting rules
7. ✅ Test error scenarios

---

**Documentation:**
- Circuit Breaker Pattern: https://martinfowler.com/bliki/CircuitBreaker.html
- Retry Patterns: https://docs.aws.amazon.com/general/latest/gr/api-retries.html
- Error Handling Best Practices: https://12factor.net/logs
