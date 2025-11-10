# LAYER 2: AI CLI Guidelines - Gemini Agent

**Layer:** 2 (AI CLI Specific)
**Agent:** Gemini (Google AI)
**Parent Layer:** [LAYER-2.md](LAYER-2.md) (AI CLI General)
**Inherits From:** [LAYER-0.md](LAYER-0.md), [LAYER-1.md](LAYER-1.md)

---

## 🎯 Gemini Agent Profile

**Primary Use Cases:**
- Bulk documentation generation
- Large-scale code analysis and refactoring
- High-volume repetitive tasks
- Data processing and transformation

**Cost:** **FREE** (1000 requests/day, 2M token context)
**Context Window:** 2M tokens (industry-leading)
**Strengths:** Massive context, cost-free, fast processing, excellent at bulk operations
**Weaknesses:** Quality variance, less specialized for security/architecture

---

## 📋 When to Use Gemini

### Automatic Selection Triggers

Gemini is auto-selected for GitHub issues with these labels:
- `documentation` - Generating/updating documentation
- `bulk` - High-volume operations
- `analysis` - Code analysis, metrics collection
- `refactor-simple` - Straightforward refactoring without complexity
- `data-processing` - Data transformation tasks

### Manual Selection

Use Gemini explicitly when:
1. **Large codebases** need analysis (leverage 2M context)
2. **Cost is a concern** (1000 free requests/day)
3. **Bulk operations** like renaming, reformatting, documenting
4. **Data extraction** from logs, metrics, or files
5. **Non-critical refactoring** that doesn't require deep security analysis

---

## 🚀 Gemini-Specific Strengths

### 1. Massive Context Window (2M tokens)

**Leverage for whole-codebase analysis:**

```bash
# ✅ CORRECT: Feed entire codebase to Gemini
gemini analyze \
  --context "$(find src -name '*.py' -exec cat {} \;)" \
  --task "Generate dependency graph for all modules"

# Gemini can handle:
# - Entire monorepo in one request
# - Complete documentation set
# - Full conversation history
# - Large log files
```

**Use Cases for Large Context:**
- Generate system-wide architecture documentation
- Analyze dependencies across entire codebase
- Find patterns/anti-patterns in large codebases
- Migrate entire projects between frameworks
- Comprehensive test coverage analysis

### 2. Cost Optimization (FREE Tier)

**1000 requests/day = Perfect for automation:**

```python
# ✅ CORRECT: Use Gemini for bulk operations to save costs
from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-2.0-flash-exp')

# Example: Document 100 functions (would cost $$$ with Claude)
for function in codebase.get_all_functions():
    prompt = f"""
    Generate comprehensive documentation for this function:

    {function.source_code}

    Include:
    - Purpose and behavior
    - Parameters and return values
    - Example usage
    - Edge cases
    """

    # FREE (within 1000/day limit)
    documentation = model.generate_content(prompt)
    function.add_docstring(documentation.text)
```

**Cost Comparison:**
| Task | Claude Pro | Gemini Free | Savings |
|------|------------|-------------|---------|
| 100 function docs | ~$3-5 | $0 | 100% |
| Codebase analysis | ~$10-15 | $0 | 100% |
| Daily automation (500 tasks) | ~$50-100 | $0 | 100% |

### 3. Speed for Simple Tasks

**Gemini Flash is extremely fast:**

```python
# ✅ CORRECT: Use Gemini Flash for quick iterations
import google.generativeai as genai

# Fast model for simple tasks
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# ~1-2 seconds response time
response = model.generate_content("Explain this error: TypeError: 'int' object is not callable")
```

---

## 📚 Gemini-Optimized Tasks

### 1. Documentation Generation

**Bulk documentation is Gemini's strength:**

```python
# ✅ CORRECT: Mass documentation generation
def document_entire_module(module_path: str) -> None:
    """Generate documentation for all functions in a module using Gemini."""

    import ast
    import google.generativeai as genai

    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # Parse module
    with open(module_path, 'r') as f:
        tree = ast.parse(f.read())

    # Extract all function definitions
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    for func in functions:
        # Get function source
        source = ast.get_source_segment(open(module_path).read(), func)

        prompt = f"""
        Generate a comprehensive docstring for this Python function:

        {source}

        Format:
        - One-line summary
        - Detailed description
        - Args section with types
        - Returns section with type
        - Raises section if applicable
        - Example usage

        Use Google style docstring format.
        """

        # Generate documentation (FREE!)
        result = model.generate_content(prompt)
        print(f"Documented: {func.name}")
        print(result.text)
```

### 2. Code Analysis at Scale

**Analyze entire repositories:**

```python
# ✅ CORRECT: Repository-wide analysis with 2M context
import google.generativeai as genai
from pathlib import Path

model = genai.GenerativeModel('gemini-2.0-flash-exp')

def analyze_repository(repo_path: str) -> dict:
    """Analyze entire repository structure and patterns."""

    # Collect all Python files (Gemini can handle them all at once!)
    all_code = []
    for py_file in Path(repo_path).rglob('*.py'):
        with open(py_file, 'r', encoding='utf-8') as f:
            all_code.append(f"# File: {py_file}\n{f.read()}\n\n")

    full_codebase = "\n".join(all_code)

    prompt = f"""
    Analyze this entire Python codebase and provide:

    1. **Architecture Overview**: High-level structure and patterns
    2. **Dependency Graph**: Module dependencies
    3. **Code Quality Issues**: Anti-patterns, duplications
    4. **Security Concerns**: Potential vulnerabilities
    5. **Test Coverage Gaps**: Areas needing tests
    6. **Documentation Needs**: Missing or outdated docs
    7. **Refactoring Opportunities**: Suggested improvements

    CODEBASE:
    {full_codebase}

    Provide structured analysis with specific file:line references.
    """

    # Gemini handles 2M tokens - entire codebase in one go!
    response = model.generate_content(prompt)
    return response.text
```

### 3. Data Processing

**Process large datasets:**

```python
# ✅ CORRECT: Log analysis with Gemini
import google.generativeai as genai

model = genai.GenerativeModel('gemini-2.0-flash-exp')

def analyze_logs(log_file: str) -> dict:
    """Analyze application logs for patterns and issues."""

    # Read large log file (100K+ lines = OK for Gemini)
    with open(log_file, 'r') as f:
        logs = f.read()

    prompt = f"""
    Analyze these application logs and identify:

    1. **Error Patterns**: Common errors and their frequencies
    2. **Performance Issues**: Slow operations, timeouts
    3. **User Behavior**: Usage patterns and anomalies
    4. **Security Events**: Failed auth, suspicious activity
    5. **Root Causes**: Underlying issues causing errors

    LOGS:
    {logs}

    Provide summary with:
    - Top 10 errors (count, severity, suggested fix)
    - Performance bottlenecks (operation, avg time, recommendation)
    - Security incidents (timestamp, type, severity)
    - Action items prioritized by impact
    """

    response = model.generate_content(prompt)
    return parse_analysis(response.text)
```

### 4. Code Migration

**Migrate between languages/frameworks:**

```python
# ✅ CORRECT: Bulk code translation
def migrate_javascript_to_typescript(js_files: list[str]) -> None:
    """Convert JavaScript files to TypeScript using Gemini."""

    import google.generativeai as genai

    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    for js_file in js_files:
        with open(js_file, 'r') as f:
            js_code = f.read()

        prompt = f"""
        Convert this JavaScript code to TypeScript:

        {js_code}

        Requirements:
        - Add strict type annotations
        - Use interfaces for object shapes
        - Add JSDoc comments
        - Handle null/undefined explicitly
        - Use modern TS features (ES2022+)

        Output ONLY the TypeScript code, no explanations.
        """

        # Fast conversion (FREE!)
        result = model.generate_content(prompt)

        # Write TypeScript file
        ts_file = js_file.replace('.js', '.ts')
        with open(ts_file, 'w') as f:
            f.write(result.text)

        print(f"Migrated: {js_file} → {ts_file}")
```

---

## ⚠️ Gemini Limitations & Workarounds

### 1. Quality Variance

**Issue:** Gemini may produce less polished code than Claude for complex tasks

**Workaround:**
```python
# ✅ CORRECT: Use Gemini for initial draft, Claude for review
def create_feature_with_review(feature_spec: str):
    # Phase 1: Gemini generates initial implementation (fast + free)
    gemini_code = gemini.generate_code(feature_spec)

    # Phase 2: Claude reviews for security/quality (high quality)
    claude_review = claude.review_code(
        gemini_code,
        focus=['security', 'edge_cases', 'error_handling']
    )

    # Phase 3: Gemini applies Claude's feedback (free refinement)
    final_code = gemini.refine_code(gemini_code, claude_review)

    return final_code
```

### 2. Rate Limits (1000 req/day)

**Issue:** Free tier has daily limits

**Workaround:**
```python
# ✅ CORRECT: Track and optimize request usage
from datetime import datetime
import json

class GeminiRateLimiter:
    """Track Gemini API usage to stay within free tier."""

    def __init__(self, limit: int = 1000):
        self.limit = limit
        self.usage_file = '.gemini_usage.json'
        self.usage = self._load_usage()

    def can_make_request(self) -> bool:
        """Check if within daily limit."""
        today = datetime.now().date().isoformat()
        return self.usage.get(today, 0) < self.limit

    def record_request(self) -> None:
        """Record API request."""
        today = datetime.now().date().isoformat()
        self.usage[today] = self.usage.get(today, 0) + 1
        self._save_usage()

    def get_remaining(self) -> int:
        """Get remaining requests for today."""
        today = datetime.now().date().isoformat()
        used = self.usage.get(today, 0)
        return max(0, self.limit - used)

# Usage
rate_limiter = GeminiRateLimiter()

if rate_limiter.can_make_request():
    response = model.generate_content(prompt)
    rate_limiter.record_request()
else:
    # Fallback to Claude or queue for tomorrow
    print(f"Gemini limit reached. Switching to Claude.")
    response = claude.generate(prompt)
```

### 3. Security Analysis Depth

**Issue:** Gemini is less specialized for security than Claude

**Workaround:**
```python
# ✅ CORRECT: Use Gemini for bulk, Claude for security
def refactor_codebase(files: list[str]):
    # Gemini: Non-security refactoring (free, fast)
    for file in files:
        if is_security_critical(file):
            # Claude: Security-critical files
            refactored = claude.refactor(file, focus='security')
        else:
            # Gemini: Standard refactoring
            refactored = gemini.refactor(file)

        save_file(file, refactored)

def is_security_critical(filepath: str) -> bool:
    """Identify security-critical files."""
    critical_patterns = [
        'auth', 'password', 'token', 'crypto',
        'security', 'permission', 'session'
    ]
    return any(pattern in filepath.lower() for pattern in critical_patterns)
```

---

## 🎯 Best Practices for Gemini

### 1. Batch Operations

**Maximize efficiency with batching:**

```python
# ✅ CORRECT: Batch multiple tasks in one request
prompt = """
Process these 10 functions and for each provide:
1. Docstring (Google style)
2. Type hints
3. Unit test

FUNCTIONS:
{function_1}
---
{function_2}
---
... (up to 10)

Output in JSON format:
[
  {
    "function_name": "...",
    "docstring": "...",
    "type_hints": "...",
    "unit_test": "..."
  },
  ...
]
"""

# 1 request instead of 10 = better rate limit management
```

### 2. Structured Output

**Request JSON for parsing:**

```python
# ✅ CORRECT: Use JSON for structured output
prompt = """
Analyze this code and return JSON:

{
  "complexity": <int>,
  "issues": [
    {"type": "...", "severity": "...", "line": <int>, "description": "..."}
  ],
  "suggestions": [
    {"priority": "...", "description": "...", "estimated_effort": "..."}
  ]
}

CODE:
{code}
"""

response = model.generate_content(prompt)
data = json.loads(response.text)  # Easy to parse
```

### 3. Leverage Multimodal Capabilities

**Gemini supports images, PDFs, videos:**

```python
# ✅ CORRECT: Analyze diagrams, screenshots
import google.generativeai as genai

model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Upload architecture diagram
image = genai.upload_file('architecture-diagram.png')

prompt = """
Analyze this architecture diagram and:
1. Describe all components
2. Identify data flows
3. Spot potential bottlenecks
4. Suggest improvements
"""

response = model.generate_content([prompt, image])
```

---

## 🔄 Integration with Smart Agent Switching

### Switch FROM Gemini to Claude when:
- Security vulnerability discovered
- Complex architectural decision needed
- Quality issues in generated code
- Deep debugging required

### Switch TO Gemini from Claude when:
- Cost optimization needed
- Bulk operations queued
- Large context required (>200K tokens)
- Speed is priority over perfect quality

---

## 📊 Gemini Performance Metrics

### Expected Quality (vs Claude)
- **Code Quality:** 85% of Claude quality
- **Security Analysis:** 70% of Claude depth
- **Documentation:** 90% of Claude quality
- **Speed:** 2-3x faster than Claude
- **Cost:** $0 vs Claude's ~$0.03-0.10 per request

### Optimal Use Cases
| Task | Gemini Score | When to Use |
|------|--------------|-------------|
| Documentation | ⭐⭐⭐⭐⭐ | Always (free + fast) |
| Bulk refactoring | ⭐⭐⭐⭐⭐ | Always (2M context) |
| Data analysis | ⭐⭐⭐⭐⭐ | Always (massive context) |
| Security audit | ⭐⭐⭐ | Only if Claude unavailable |
| Architecture design | ⭐⭐⭐ | Initial draft, Claude review |
| Complex debugging | ⭐⭐ | Use Claude instead |

---

## 🛡️ Quality Assurance for Gemini Output

### Post-Processing Checklist
- [ ] **Syntax Validation:** Code compiles/runs
- [ ] **Security Scan:** Run Bandit/Semgrep on generated code
- [ ] **Test Coverage:** Verify tests actually test the code
- [ ] **Type Checking:** mypy/pyright validation
- [ ] **Linting:** black/ruff formatting
- [ ] **Manual Review:** Spot-check critical sections

---

## 📚 References

### Inherits Guidelines From:
- [LAYER-0: Universal Standards](LAYER-0.md)
- [LAYER-1: MCP Server Usage](LAYER-1.md)
- [LAYER-2: AI CLI General](LAYER-2.md)

### Gemini-Specific Resources:
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Gemini Models](https://ai.google.dev/models/gemini)
- [Gemini Rate Limits](https://ai.google.dev/pricing)

### Related ADRs:
- ADR-005: Smart Agent Switching (cost optimization)
- ADR-001: Latent Reasoning (context compression)

---

**Version:** 2.0.0
**Last Updated:** 2025-11-09
**Maintainer:** Phantom Neural Cortex Team
