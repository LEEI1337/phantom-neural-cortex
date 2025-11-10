# LAYER 2: AI CLI Guidelines - GitHub Copilot Agent

**Layer:** 2 (AI CLI Specific)
**Agent:** GitHub Copilot
**Parent Layer:** [LAYER-2.md](LAYER-2.md) (AI CLI General)
**Inherits From:** [LAYER-0.md](LAYER-0.md), [LAYER-1.md](LAYER-1.md)

---

## 🎯 GitHub Copilot Agent Profile

**Primary Use Cases:**
- GitHub-specific workflows (Issues, PRs, Actions)
- Quick code fixes and completions
- Boilerplate generation
- Code suggestions in IDE

**Cost:** FREE (Individual) / $10/mo (Pro) / $19/user/mo (Business)
**Context Window:** Variable (IDE-dependent)
**Strengths:** GitHub integration, real-time IDE assistance, familiar developer UX
**Weaknesses:** Limited reasoning depth, smaller context, requires GitHub account

---

## 📋 When to Use GitHub Copilot

### Automatic Selection Triggers

Copilot is auto-selected for GitHub issues with these labels:
- `github-workflow` - GitHub Actions, CI/CD
- `pr-automation` - Pull request workflows
- `issue-triage` - Issue management
- `quick-fix` - Small, straightforward bugs
- `boilerplate` - Code generation (CRUD, templates)

### Manual Selection

Use Copilot explicitly when:
1. **GitHub operations** - Creating PRs, managing issues, workflows
2. **Quick iterations** - Small fixes that need fast turnaround
3. **IDE integration** - Real-time coding assistance
4. **Familiarity** - Developer prefers Copilot UX
5. **Cost optimization** - Free tier available

---

## 🚀 Copilot-Specific Strengths

### 1. Native GitHub Integration

**Leverage Copilot's GitHub superpowers:**

```bash
# ✅ CORRECT: Use Copilot for GitHub workflows
gh copilot suggest "Create a GitHub Action to run tests on PR"

# Output: Complete GitHub Actions YAML
# .github/workflows/test.yml generated with:
# - Proper triggers (pull_request)
# - Matrix builds (Python 3.11, 3.12)
# - Caching strategies
# - Status reporting
```

**GitHub-Specific Tasks:**
```bash
# Create PR with AI-generated description
gh pr create --fill-ai

# Review PR with Copilot suggestions
gh copilot review-pr 123

# Generate issue templates
gh copilot generate-issue-template --type bug

# Optimize GitHub Actions workflow
gh copilot optimize-workflow .github/workflows/ci.yml
```

### 2. Real-Time IDE Assistance

**Copilot shines in IDEs (VS Code, JetBrains, Neovim):**

```python
# ✅ CORRECT: Use Copilot for inline completions

# Type: "def calculate_fibonacci"
# Copilot suggests complete implementation:

def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number using memoization."""
    memo = {0: 0, 1: 1}

    def fib(num: int) -> int:
        if num in memo:
            return memo[num]
        memo[num] = fib(num - 1) + fib(num - 2)
        return memo[num]

    return fib(n)

# Type: "# test for calculate_fibonacci"
# Copilot suggests tests:

def test_calculate_fibonacci():
    assert calculate_fibonacci(0) == 0
    assert calculate_fibonacci(1) == 1
    assert calculate_fibonacci(10) == 55
    assert calculate_fibonacci(20) == 6765
```

### 3. Quick Boilerplate Generation

**Fast CRUD, routes, models:**

```typescript
// ✅ CORRECT: Use Copilot for repetitive code

// Type: "// Express route for user CRUD"
// Copilot generates:

import { Router } from 'express';
import { User } from './models/User';

const router = Router();

// GET all users
router.get('/users', async (req, res) => {
  try {
    const users = await User.findAll();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});

// GET user by ID
router.get('/users/:id', async (req, res) => {
  try {
    const user = await User.findByPk(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch user' });
  }
});

// POST create user
router.post('/users', async (req, res) => {
  try {
    const user = await User.create(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: 'Failed to create user' });
  }
});

// ... (PUT, DELETE routes)
```

---

## 🎯 Copilot-Optimized Tasks

### 1. GitHub Actions & CI/CD

**Best-in-class for workflow generation:**

```yaml
# ✅ CORRECT: Copilot-generated GitHub Actions workflow

# Type: "# GitHub Action for Python test, lint, type-check"
# Copilot generates:

name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Lint with ruff
      run: ruff check .

    - name: Type check with mypy
      run: mypy src/

    - name: Test with pytest
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
```

### 2. Pull Request Automation

**Copilot CLI for PR workflows:**

```bash
# ✅ CORRECT: Use gh copilot for PR tasks

# Create PR with AI-generated title & description
gh pr create \
  --title "$(gh copilot suggest-title)" \
  --body "$(gh copilot suggest-pr-body)"

# Review code with Copilot suggestions
gh copilot review-pr 42 --focus security,performance

# Generate PR checklist
gh copilot pr-checklist \
  --include tests,docs,changelog,breaking-changes
```

### 3. Issue Management

**Automate issue triage:**

```bash
# ✅ CORRECT: Copilot-assisted issue management

# Auto-label issue based on content
LABELS=$(gh copilot suggest-labels --issue 123)
gh issue edit 123 --add-label "$LABELS"

# Generate issue response
gh copilot reply-to-issue 123 \
  --context "Known bug, fix in PR #124"

# Create issue from error log
cat error.log | gh copilot create-issue \
  --title "Investigate production error" \
  --auto-assign
```

### 4. Code Completion & Refactoring

**Inline suggestions in IDE:**

```python
# ✅ CORRECT: Use Copilot Chat for refactoring

# Select code block, then in Copilot Chat:
# "/refactor Extract this into separate functions"

# Before (messy):
def process_data(data):
    # 100 lines of mixed logic
    pass

# After (Copilot refactor):
def process_data(data):
    validated_data = validate_input(data)
    transformed_data = transform_data(validated_data)
    result = save_to_database(transformed_data)
    send_notification(result)
    return result

def validate_input(data):
    # Validation logic
    pass

def transform_data(data):
    # Transformation logic
    pass

# ... (extracted functions)
```

---

## ⚠️ Copilot Limitations & Workarounds

### 1. Limited Context Window

**Issue:** Copilot has smaller context than Claude/Gemini

**Workaround:**
```python
# ✅ CORRECT: Provide context in comments

# Context: This function is part of the authentication system.
# It validates JWT tokens issued by auth_service.py
# Related files: auth_service.py, token_manager.py
# Dependencies: PyJWT, cryptography
# See: docs/authentication.md for flow diagram

def validate_token(token: str) -> bool:
    # Copilot now has context to generate better code
    pass
```

### 2. Security Awareness

**Issue:** Copilot may suggest insecure patterns

**Workaround:**
```python
# ❌ WRONG: Copilot might suggest this
password = request.form['password']
user = User.query.filter_by(password=password).first()  # Plain text!

# ✅ CORRECT: Guide Copilot with security comments
# SECURITY: Always hash passwords with bcrypt
# SECURITY: Never store plain text passwords
# SECURITY: Use constant-time comparison

import bcrypt
password = request.form['password']
user = User.query.filter_by(username=username).first()
if user and bcrypt.checkpw(password.encode(), user.hashed_password):
    # Authenticated
    pass
```

### 3. Complex Architecture

**Issue:** Copilot struggles with complex multi-file refactors

**Workaround:**
```bash
# ✅ CORRECT: Use Copilot for individual files, Claude for architecture

# Copilot: Quick file-level changes
copilot: "Add logging to all functions in this file"

# Claude: Multi-file architectural changes
claude: "Refactor authentication system across 10 files to use OAuth2"
```

---

## 🎯 Best Practices for Copilot

### 1. Comment-Driven Development

**Guide Copilot with clear comments:**

```python
# ✅ CORRECT: Descriptive comments = better suggestions

# Function to fetch user data from PostgreSQL database
# Input: user_id (integer, primary key)
# Output: User object with id, name, email, created_at
# Raises: UserNotFoundError if user doesn't exist
# Caches result in Redis for 5 minutes
def get_user_by_id(user_id: int) -> User:
    # Copilot generates implementation based on these hints
    pass
```

### 2. Leverage Copilot Chat

**Use `/` commands in Copilot Chat:**

```
/explain     - Explain selected code
/fix         - Suggest fixes for errors
/tests       - Generate unit tests
/doc         - Add documentation
/refactor    - Refactor code
/optimize    - Performance optimizations
/security    - Security review
```

### 3. Iterative Refinement

**Accept → Refine → Repeat:**

```python
# ✅ CORRECT: Iterative improvement with Copilot

# Iteration 1: Basic function
def calculate_total(items):
    return sum(items)

# Iteration 2: Add type hints (Copilot suggests)
def calculate_total(items: list[float]) -> float:
    return sum(items)

# Iteration 3: Add validation (guide Copilot)
# Add input validation: items must be non-empty, all positive numbers
def calculate_total(items: list[float]) -> float:
    if not items:
        raise ValueError("Items list cannot be empty")
    if any(item < 0 for item in items):
        raise ValueError("All items must be positive")
    return sum(items)
```

### 4. GitHub Context Injection

**Copilot uses GitHub data:**

```bash
# ✅ CORRECT: Reference issues/PRs in code comments

# TODO: Fix performance issue mentioned in #123
# Related PR: #124 (waiting for review)
# See discussion: https://github.com/org/repo/discussions/45

# Copilot will reference these when suggesting fixes
```

---

## 🔄 Integration with Smart Agent Switching

### Switch FROM Copilot to Claude when:
- Security-critical code detected
- Complex multi-file refactoring needed
- Deep architectural decisions required
- Quality issues in Copilot suggestions

### Switch FROM Copilot to Gemini when:
- Large codebase analysis needed (>50 files)
- Bulk documentation required
- Cost optimization critical (free Gemini tier)

### Switch TO Copilot from others when:
- GitHub workflow automation needed
- Real-time IDE assistance wanted
- Quick boilerplate generation
- Developer familiar with Copilot UX

---

## 📊 Copilot Performance Metrics

### Expected Quality
- **GitHub Workflows:** ⭐⭐⭐⭐⭐ (Best-in-class)
- **Boilerplate Code:** ⭐⭐⭐⭐⭐ (Excellent)
- **Quick Fixes:** ⭐⭐⭐⭐ (Very Good)
- **Security Analysis:** ⭐⭐⭐ (Adequate, needs review)
- **Complex Architecture:** ⭐⭐ (Use Claude instead)

### Speed Comparison
| Task | Copilot | Claude | Gemini |
|------|---------|--------|--------|
| Inline completion | ~100ms | N/A | N/A |
| GitHub Action | ~5s | ~15s | ~10s |
| PR description | ~3s | ~10s | ~8s |
| Boilerplate CRUD | ~2s | ~20s | ~15s |

---

## 🛡️ Security Considerations for Copilot

### Code Review Checklist

Always review Copilot suggestions for:
- [ ] **Hardcoded Secrets:** Check for API keys, passwords
- [ ] **SQL Injection:** Verify parameterized queries
- [ ] **XSS:** Ensure input sanitization
- [ ] **CSRF:** Check token validation
- [ ] **Auth Bypass:** Validate permission checks
- [ ] **Error Leakage:** No sensitive data in error messages

### Security-First Prompting

```python
# ✅ CORRECT: Security-focused comments

# SECURITY REQUIREMENTS:
# - Validate and sanitize all inputs
# - Use parameterized SQL queries
# - Hash passwords with bcrypt (cost=12)
# - Implement rate limiting (max 5 req/min)
# - Log all authentication attempts
# - Return generic errors (no user enumeration)

def create_user(username: str, password: str) -> User:
    # Copilot generates secure implementation
    pass
```

---

## 💡 Copilot Pro Tips

### 1. Use GitHub Copilot Labs

```bash
# Install Copilot Labs extension
# Features:
# - Explain code
# - Translate languages
# - Brushes (readable, fix bug, debug, clean)
# - Test generation
```

### 2. Keyboard Shortcuts

```
Tab          - Accept suggestion
Alt+]        - Next suggestion
Alt+[        - Previous suggestion
Ctrl+Enter   - Open Copilot panel
Alt+\        - Trigger inline suggestion
```

### 3. Fine-Tune with .copilotignore

```bash
# ✅ CORRECT: Exclude sensitive files from Copilot

# .copilotignore
.env
secrets/
*.key
*.pem
config/production.yaml
```

---

## 📚 References

### Inherits Guidelines From:
- [LAYER-0: Universal Standards](LAYER-0.md)
- [LAYER-1: MCP Server Usage](LAYER-1.md)
- [LAYER-2: AI CLI General](LAYER-2.md)

### Copilot-Specific Resources:
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Copilot CLI](https://githubnext.com/projects/copilot-cli/)
- [Copilot Labs](https://githubnext.com/projects/copilot-labs/)
- [gh CLI Reference](https://cli.github.com/manual/)

### Related ADRs:
- ADR-005: Smart Agent Switching
- GitHub Actions in LAYER-1.md

---

**Version:** 2.0.0
**Last Updated:** 2025-11-09
**Maintainer:** Phantom Neural Cortex Team
