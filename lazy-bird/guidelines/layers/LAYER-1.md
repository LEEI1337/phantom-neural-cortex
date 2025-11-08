# 📋 LAYER 1 - MCP Server Usage

**Gilt für:** AI CLIs die MCP Servers verwenden
**Erbt von:** LAYER-0 (Universal Standards)
**Zweck:** Standardisierte Nutzung der 18 MCP Servers

---

## 🎯 Verfügbare MCP Server

### Filesystem & Git
- **@modelcontextprotocol/server-filesystem** - File Operations
- **@modelcontextprotocol/server-git** - Git Operations
- **@vimtor/mcp-server-docker** - Docker Management

### Datenbanken
- **@modelcontextprotocol/server-postgres** - PostgreSQL
- **@modelcontextprotocol/server-sqlite** - SQLite

### AI & Search
- **@modelcontextprotocol/server-brave-search** - Web Search
- **@wong2/mcp-server-perplexity** - Perplexity AI
- **@mzxai/mcp-server-gemini-advisor** - Gemini CLI Integration

### Development Tools
- **@modelcontextprotocol/server-github** - GitHub API
- **@modelcontextprotocol/server-gitlab** - GitLab API
- **@modelcontextprotocol/server-memory** - Persistent Memory
- **@modelcontextprotocol/server-fetch** - HTTP Requests
- **@modelcontextprotocol/server-puppeteer** - Browser Automation
- **@kimtaeyoon83/mcp-server-youtube-transcript** - YouTube Transcripts
- **@blazickjp/mcp-server-arxiv** - ArXiv Papers

### Productivity
- **@angheljf/mcp-simple-timekeeper** - Time Tracking
- **@modelcontextprotocol/server-slack** - Slack Integration
- **@modelcontextprotocol/server-google-maps** - Maps API

---

## 🔧 Best Practices pro Server

### Filesystem Server

```python
# ✅ RICHTIG: Use Read/Write tools statt direkter File I/O
# Über MCP:
content = read_file("/path/to/file.txt")
write_file("/path/to/file.txt", "new content")

# ❌ FALSCH: Direkter File Access (MCP bypassed)
with open("/path/to/file.txt") as f:
    content = f.read()
```

**Warum MCP?**
- Consistent Error Handling
- Rate Limiting
- Logging & Monitoring
- Security Checks

### Git Server

```python
# ✅ RICHTIG: MCP Git Tools
git_status = call_mcp_tool("git", "status", {"repo": "."})
git_commit = call_mcp_tool("git", "commit", {
    "message": "feat: Add feature",
    "files": ["src/feature.py"]
})

# ❌ FALSCH: Direkte Git Commands (bypassed MCP)
import subprocess
subprocess.run(["git", "status"])
```

### Brave Search Server

```python
# ✅ RICHTIG: Rate Limit beachten
def search_web(query: str) -> List[Result]:
    # Max 60 requests/hour (Free Tier)
    if rate_limit_exceeded():
        raise RateLimitError("Wait before next search")

    return call_mcp_tool("brave-search", "search", {
        "query": query,
        "count": 10
    })

# ❌ FALSCH: Unlimitierte Requests
for query in 1000_queries:  # Rate Limit!
    search_web(query)
```

### GitHub Server

```python
# ✅ RICHTIG: Verwende MCP GitHub Tools
issues = call_mcp_tool("github", "list_issues", {
    "owner": "LEEI1337",
    "repo": "ai-dev-orchestrator",
    "state": "open"
})

# ❌ FALSCH: Direkte API Calls
response = requests.get(
    "https://api.github.com/repos/LEEI1337/ai-dev-orchestrator/issues"
)
```

---

## 📊 Rate Limits (WICHTIG!)

### Free Tier Limits

| MCP Server | Rate Limit | Hinweis |
|-----------|-----------|---------|
| Brave Search | 60/hour | Cached results nutzen |
| Gemini Advisor | 1000/day | Free tier |
| Perplexity | 10/month | SEHR limitiert! |
| GitHub | 5000/hour | Mit Token |
| ArXiv | Unlimitiert | Aber fair use |

### Rate Limit Handling

```python
# ✅ RICHTIG: Rate Limit Tracking
class MCPRateLimiter:
    def __init__(self):
        self.limits = {
            "brave-search": {"max": 60, "window": 3600},
            "perplexity": {"max": 10, "window": 2592000},
        }
        self.usage = {}

    def check_limit(self, server: str) -> bool:
        """Check if request allowed."""
        if server not in self.limits:
            return True  # No limit

        limit = self.limits[server]
        now = time.time()

        # Clean old requests
        self.usage[server] = [
            ts for ts in self.usage.get(server, [])
            if now - ts < limit["window"]
        ]

        # Check limit
        if len(self.usage[server]) >= limit["max"]:
            return False

        # Track request
        self.usage[server].append(now)
        return True
```

---

## 🔐 API Keys & Secrets

### Environment Variables (PFLICHT)

```python
# ✅ RICHTIG: Von .env laden
import os

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

if not BRAVE_API_KEY:
    raise ValueError("BRAVE_API_KEY not set in .env")

# ❌ FALSCH: Hardcoded
BRAVE_API_KEY = "BSA..."  # NIEMALS!
```

### .env Template

```bash
# .env.example (committed)
BRAVE_API_KEY=
GITHUB_TOKEN=
PERPLEXITY_API_KEY=
GEMINI_API_KEY=

# .env (NOT committed!)
BRAVE_API_KEY=BSA...
GITHUB_TOKEN=ghp_...
PERPLEXITY_API_KEY=DK2...
GEMINI_API_KEY=AIza...
```

---

## 💾 Caching Best Practices

### Brave Search Caching

```python
# ✅ RICHTIG: Cache Results
import hashlib
from datetime import datetime, timedelta

class SearchCache:
    def __init__(self, ttl_hours: int = 24):
        self.cache = {}
        self.ttl = timedelta(hours=ttl_hours)

    def get(self, query: str):
        key = hashlib.md5(query.encode()).hexdigest()

        if key in self.cache:
            result, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return result  # Cache hit!

        # Cache miss - fetch from API
        result = call_mcp_tool("brave-search", "search", {"query": query})
        self.cache[key] = (result, datetime.now())
        return result
```

---

## 🛠️ Tool Selection Guide

### Wann welchen MCP Server?

**File Operations:**
```
Lesen/Schreiben → @modelcontextprotocol/server-filesystem
Git Operations → @modelcontextprotocol/server-git
```

**Web & API:**
```
Allgemeine Suche → @modelcontextprotocol/server-brave-search
AI-gestützte Suche → @wong2/mcp-server-perplexity (LIMIT!)
HTTP Requests → @modelcontextprotocol/server-fetch
```

**Development:**
```
GitHub Issues/PRs → @modelcontextprotocol/server-github
Docker Management → @vimtor/mcp-server-docker
Browser Testing → @modelcontextprotocol/server-puppeteer
```

**Research:**
```
Papers → @blazickjp/mcp-server-arxiv
YouTube → @kimtaeyoon83/mcp-server-youtube-transcript
```

---

## ⚡ Performance Optimization

### 1. Batch Operations

```python
# ✅ RICHTIG: Batch File Reads
files = ["file1.txt", "file2.txt", "file3.txt"]
contents = [read_file(f) for f in files]  # Batch MCP calls

# ❌ FALSCH: Individual Calls mit Delays
for file in files:
    content = read_file(file)
    time.sleep(1)  # Unnecessary delay!
```

### 2. Parallel Requests (wenn erlaubt)

```python
# ✅ RICHTIG: Parallel MCP Calls
from concurrent.futures import ThreadPoolExecutor

def fetch_multiple_repos(repos: List[str]):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(
                call_mcp_tool, "github", "get_repo", {"repo": repo}
            )
            for repo in repos
        ]
        return [f.result() for f in futures]

# ❌ FALSCH: Sequential
results = []
for repo in repos:
    results.append(call_mcp_tool("github", "get_repo", {"repo": repo}))
```

---

## 🚨 Error Handling

### MCP Tool Failures

```python
# ✅ RICHTIG: Proper Error Handling
def safe_mcp_call(server: str, tool: str, params: dict):
    try:
        return call_mcp_tool(server, tool, params)
    except RateLimitError as e:
        logger.warning(f"Rate limit for {server}: {e}")
        # Wait and retry
        time.sleep(60)
        return call_mcp_tool(server, tool, params)
    except AuthenticationError as e:
        logger.error(f"Auth failed for {server}: {e}")
        raise
    except Exception as e:
        logger.error(f"MCP call failed: {e}")
        # Fallback or re-raise
        raise

# ❌ FALSCH: Bare except
try:
    result = call_mcp_tool("github", "get_repo", params)
except:
    pass  # Silent failure!
```

---

## 📊 Logging & Monitoring

### MCP Call Logging

```python
# ✅ RICHTIG: Log all MCP calls
import logging

logger = logging.getLogger(__name__)

def call_mcp_tool_logged(server: str, tool: str, params: dict):
    logger.info(f"MCP Call: {server}.{tool} with {params}")

    start = time.time()
    try:
        result = call_mcp_tool(server, tool, params)
        duration = time.time() - start

        logger.info(f"MCP Success: {server}.{tool} in {duration:.2f}s")
        return result

    except Exception as e:
        duration = time.time() - start
        logger.error(f"MCP Failed: {server}.{tool} after {duration:.2f}s: {e}")
        raise
```

---

## ✅ Layer 1 Checkliste

- [ ] Verwende MCP Tools statt direkter API Calls
- [ ] Rate Limits beachten und tracken
- [ ] API Keys in Environment Variables
- [ ] Caching für teure Calls (Brave Search, Perplexity)
- [ ] Proper Error Handling mit Retries
- [ ] Logging aller MCP Calls
- [ ] Batch Operations wo möglich
- [ ] Parallel Requests nutzen (wo erlaubt)

---

**Nächster Layer:** [LAYER-2.md](LAYER-2.md) - AI CLI Usage
