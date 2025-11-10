# LAYER 2: AI CLI Guidelines - Claude Agent

**Layer:** 2 (AI CLI Specific)
**Agent:** Claude (Anthropic)
**Parent Layer:** [LAYER-2.md](LAYER-2.md) (AI CLI General)
**Inherits From:** [LAYER-0.md](LAYER-0.md), [LAYER-1.md](LAYER-1.md)

---

##  Claude Agent Profile

**Primary Use Cases:**
- Security-critical tasks and audits
- Architecture design and complex refactoring
- High-quality code generation
- Deep reasoning and problem-solving

**Cost:** $20/mo (Claude Pro)
**Context Window:** 200K tokens
**Strengths:** Code quality, security awareness, best practices, reasoning depth
**Weaknesses:** API rate limits, cost for high-volume tasks

---

##  When to Use Claude

### Automatic Selection Triggers

Claude is auto-selected for GitHub issues with these labels:
- `security` - Security audits, vulnerability fixes
- `architecture` - System design, architectural decisions
- `complex` - Multi-step problems requiring deep reasoning
- `refactor` - Large-scale refactoring with quality focus
- `critical` - Production-critical bugs or features

### Manual Selection

Use Claude explicitly when:
1. Security implications are unclear
2. Multiple architectural approaches need evaluation
3. Code quality is paramount (public APIs, core libraries)
4. Complex debugging requiring root cause analysis
5. Critical production issues

---

##  Claude-Specific Requirements

### 1. Security First Mindset

**ALWAYS apply security best practices:**

```python
#  CORRECT: Input Validation & Sanitization
from typing import Optional
import html
import re

def process_user_input(data: str, max_length: int = 1000) -> str:
    """Process user input with security validation."""
    # Type validation
    if not isinstance(data, str):
        raise TypeError(f"Expected string, got {type(data).__name__}")

    # Length validation
    if len(data) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length}")

    # Content validation (example: alphanumeric + spaces)
    if not re.match(r'^[a-zA-Z0-9\s]+$', data):
        raise ValueError("Input contains invalid characters")

    # HTML escape for XSS prevention
    return html.escape(data.strip())

#  WRONG: No validation
def process_user_input(data):
    return data  # XSS, injection, DoS vulnerabilities!
```

```typescript
//  CORRECT: SQL Injection Prevention with Parameterized Queries
import { Pool } from 'pg';

async function getUserById(pool: Pool, userId: number): Promise<User> {
  // Parameterized query prevents SQL injection
  const result = await pool.query(
    'SELECT id, name, email FROM users WHERE id = $1',
    [userId]
  );

  if (result.rows.length === 0) {
    throw new Error(`User ${userId} not found`);
  }

  return result.rows[0];
}

//  WRONG: String concatenation vulnerable to SQL injection
async function getUserById(pool: Pool, userId: number): Promise<User> {
  const result = await pool.query(
    `SELECT * FROM users WHERE id = ${userId}` // SQL injection!
  );
  return result.rows[0];
}
```

### 2. Comprehensive Error Handling

**Always handle errors explicitly and meaningfully:**

```python
#  CORRECT: Specific Exception Handling
import logging
from typing import Dict, Any
import requests
from requests.exceptions import Timeout, HTTPError, RequestException

logger = logging.getLogger(__name__)

def fetch_api_data(url: str, timeout: int = 10) -> Dict[str, Any]:
    """Fetch data from API with robust error handling."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()

    except Timeout:
        logger.error(f"Request to {url} timed out after {timeout}s")
        raise

    except HTTPError as e:
        logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
        raise

    except ValueError as e:
        logger.error(f"Invalid JSON response from {url}: {e}")
        raise

    except RequestException as e:
        logger.error(f"Network error fetching {url}: {e}")
        raise

    except Exception as e:
        logger.critical(f"Unexpected error fetching {url}: {e}", exc_info=True)
        raise

#  WRONG: Bare except with silent failure
def fetch_api_data(url):
    try:
        return requests.get(url).json()
    except:
        pass  # Silent failure - debugging nightmare!
```

### 3. Strong Type Safety

**Use strict typing in Python and TypeScript:**

```typescript
//  CORRECT: Strict TypeScript Types
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: Date;
  metadata?: Record<string, unknown>;
}

interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

async function getUser(id: number): Promise<ApiResponse<User>> {
  // Type-safe implementation
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();

  // Runtime validation
  if (!isValidUser(data)) {
    throw new TypeError('Invalid user data structure');
  }

  return {
    success: true,
    data: data as User
  };
}

function isValidUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null &&
         'id' in obj && typeof obj.id === 'number' &&
         'name' in obj && typeof obj.name === 'string' &&
         'email' in obj && typeof obj.email === 'string';
}

//  WRONG: Any types everywhere
async function getUser(id: any): Promise<any> {
  return fetch(`/api/users/${id}`).then((r: any) => r.json());
}
```

```python
#  CORRECT: Python Type Hints with Runtime Validation
from typing import Literal, TypedDict, Optional
from dataclasses import dataclass
from datetime import datetime

Role = Literal['admin', 'user', 'guest']

@dataclass
class User:
    id: int
    name: str
    email: str
    role: Role
    created_at: datetime
    metadata: Optional[dict] = None

    def __post_init__(self):
        """Runtime validation."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"Invalid user ID: {self.id}")
        if not self.email or '@' not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
        if self.role not in ['admin', 'user', 'guest']:
            raise ValueError(f"Invalid role: {self.role}")

#  WRONG: No types
def get_user(id):
    return {'id': id, 'name': 'John'}
```

### 4. Architectural Thinking

**Consider system-wide implications:**

```python
#  CORRECT: Design Pattern with Clear Separation of Concerns
from abc import ABC, abstractmethod
from typing import Protocol

class MetricsCollector(Protocol):
    """Protocol for metrics collection (dependency inversion)."""
    def record_event(self, event: str, value: float) -> None: ...

class FeatureService:
    """Service with dependency injection and single responsibility."""

    def __init__(
        self,
        repository: 'FeatureRepository',
        metrics: MetricsCollector,
        cache: 'CacheService'
    ):
        self._repository = repository
        self._metrics = metrics
        self._cache = cache

    async def create_feature(self, feature_data: dict) -> Feature:
        """Create feature with proper layering."""
        # 1. Validation layer
        validated_data = self._validate_feature_data(feature_data)

        # 2. Business logic layer
        feature = await self._repository.create(validated_data)

        # 3. Side effects (metrics, cache)
        self._metrics.record_event('feature.created', 1.0)
        await self._cache.invalidate(f'features:{feature.id}')

        return feature

    def _validate_feature_data(self, data: dict) -> dict:
        """Separate validation logic."""
        # Validation implementation
        return data

#  WRONG: God class with mixed concerns
class FeatureManager:
    def create_feature(self, data):
        # Database, validation, caching, metrics all mixed together
        feature = self.db.create(data)
        self.cache.set(feature.id, feature)
        self.metrics.increment('features')
        return feature
```

### 5. Documentation Excellence

**Write comprehensive documentation:**

```python
#  CORRECT: Comprehensive Docstrings
from typing import List, Optional
from datetime import datetime

def analyze_quality_metrics(
    iterations: List[int],
    quality_scores: List[float],
    threshold: float = 0.8,
    min_iterations: int = 3
) -> dict:
    """
    Analyze quality progression across iterations to detect stagnation.

    This function implements the quality stagnation detection algorithm
    as described in ADR-004 (Deep Supervision Checkpoints). It calculates
    variance and trend to determine if the refinement loop should terminate.

    Args:
        iterations: List of iteration numbers (must be sequential)
        quality_scores: Corresponding quality scores (0.0-1.0 range)
        threshold: Minimum acceptable quality score (default: 0.8)
        min_iterations: Minimum iterations before stagnation check (default: 3)

    Returns:
        Dictionary containing:
        - is_stagnant (bool): True if quality has stagnated
        - variance (float): Variance of recent quality scores
        - trend (float): Linear trend coefficient
        - recommendation (str): Action recommendation

    Raises:
        ValueError: If iterations and quality_scores have different lengths
        ValueError: If quality_scores contain values outside [0.0, 1.0]
        ValueError: If iterations are not sequential

    Example:
        >>> iterations = [1, 2, 3, 4, 5]
        >>> scores = [0.65, 0.72, 0.73, 0.74, 0.74]
        >>> result = analyze_quality_metrics(iterations, scores)
        >>> result['is_stagnant']
        True
        >>> result['recommendation']
        'Quality stagnated at 74% - consider stopping refinement'

    See Also:
        - ADR-004: Deep Supervision Checkpoints
        - docs/feedback-loop/OPTIMIZATION-SUMMARY.md
    """
    # Implementation
    pass

#  WRONG: Minimal or no documentation
def analyze_metrics(data):
    """Analyze metrics."""
    return calculate_stuff(data)
```

---

##  Claude's Reasoning Strengths

### Leverage Extended Thinking

Claude excels at multi-step reasoning. Structure complex tasks:

```python
#  CORRECT: Break down complex problems for Claude
"""
Task: Refactor authentication system for better security

Claude's approach:
1. ANALYZE current implementation
   - Identify security vulnerabilities
   - Map data flows
   - Review error handling

2. DESIGN new architecture
   - Apply security best practices (OWASP)
   - Consider edge cases
   - Plan migration strategy

3. IMPLEMENT incrementally
   - Phase 1: Add new secure methods
   - Phase 2: Migrate users
   - Phase 3: Deprecate old methods

4. VALIDATE
   - Security audit
   - Performance testing
   - Rollback plan
"""
```

### Root Cause Analysis

Claude is excellent at debugging. Provide context:

```
#  CORRECT: Structured debugging request
"""
BUG: User authentication fails intermittently

CONTEXT:
- Happens ~5% of requests
- Only in production (not staging)
- Started after deploy on 2025-11-05
- Logs show: "Token validation failed"

ATTEMPTED FIXES:
- Increased token expiry → No change
- Restarted services → Temporary improvement
- Checked database → No issues

REQUEST:
Use root-cause tracing to identify the issue.
Consider: rate limiting, clock skew, caching, load balancing
"""
```

---

##  Quality Metrics for Claude Tasks

### Code Quality Targets

When Claude generates code, expect:
- **Type Coverage:** ≥90%
- **Test Coverage:** ≥80%
- **Cyclomatic Complexity:** ≤10 per function
- **Security Score:** Bandit/Semgrep passing with no high/critical issues
- **Documentation:** All public APIs documented

### Review Checklist

Before accepting Claude's output:
- [ ] Security vulnerabilities addressed (OWASP Top 10)
- [ ] Error handling comprehensive and specific
- [ ] Types defined and validated
- [ ] Edge cases considered
- [ ] Performance implications analyzed
- [ ] Documentation complete
- [ ] Tests included (unit + integration)
- [ ] Backward compatibility maintained
- [ ] Migration path documented (if breaking change)

---

##  Integration with Other Agents

### When to Switch FROM Claude

Switch to another agent when:
- **Gemini:** Bulk documentation, simple refactoring, high-volume tasks
- **Copilot:** GitHub-specific workflows, quick fixes, boilerplate
- **Cursor:** Real-time coding assistance, IDE integration

### When to Switch TO Claude

Switch to Claude when:
- Security review needed
- Architecture decision required
- Complex bug needs root cause analysis
- Quality bar must be raised

---

##  Claude-Specific Best Practices

### 1. Leverage Sequential Thinking MCP

Claude has access to sequential-thinking MCP server. Use for:
- Multi-step architectural planning
- Complex algorithm design
- Security analysis with attack tree modeling

### 2. Use Memory MCP for Context

Store architectural decisions and patterns:
```bash
# Store important context
memory.store("auth_architecture", {
  "pattern": "JWT with refresh tokens",
  "rationale": "Stateless, scalable, secure",
  "decision_date": "2025-11-09"
})
```

### 3. Request Detailed Explanations

Claude excels at explaining. Ask for:
- Design rationale
- Security trade-offs
- Alternative approaches considered
- Future maintenance implications

---

##  Security Checklist (Claude Priority)

Every Claude task should verify:
- [ ] **Input Validation:** All user inputs validated and sanitized
- [ ] **SQL Injection:** Parameterized queries used
- [ ] **XSS Prevention:** Output escaped/encoded
- [ ] **CSRF Protection:** Tokens implemented for state-changing operations
- [ ] **Authentication:** Secure credential storage (bcrypt/Argon2)
- [ ] **Authorization:** Principle of least privilege
- [ ] **Secrets Management:** No hardcoded secrets, use environment variables
- [ ] **Error Messages:** No sensitive information leaked in errors
- [ ] **Rate Limiting:** API endpoints protected
- [ ] **Logging:** Security events logged (but not sensitive data)

---

##  References

### Inherits Guidelines From:
- [LAYER-0: Universal Standards](LAYER-0.md)
- [LAYER-1: MCP Server Usage](LAYER-1.md)
- [LAYER-2: AI CLI General](LAYER-2.md)

### Claude-Specific Resources:
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)

### Related ADRs:
- ADR-005: Smart Agent Switching (when to use Claude)
- ADR-011: RL Refinement Chain (quality optimization)

---

**Version:** 2.0.0
**Last Updated:** 2025-11-09
**Maintainer:** Phantom Neural Cortex Team
