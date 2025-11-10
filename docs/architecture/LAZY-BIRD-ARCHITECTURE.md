# 🏗️ Lazy Bird Architecture - Technical Design

> **4-Layer Autonomous Development System**  
> Comprehensive technical architecture for Layer 4 automation above Rover

---

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Architecture Layers](#architecture-layers)
- [Component Design](#component-design)
- [Data Flow](#data-flow)
- [Integration Points](#integration-points)
- [Cost Optimization Strategy](#cost-optimization-strategy)
- [Scalability & Performance](#scalability--performance)
- [Security Considerations](#security-considerations)

---

## System Overview

Lazy Bird adds **Layer 4 (Automation)** above the existing 3-layer AI development orchestrator, creating an autonomous GitHub issue → implementation → PR workflow.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: LAZY BIRD (Automation & Orchestration)            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Issue       │  │ Agent        │  │ Rover        │       │
│  │ Watcher     │→ │ Selector     │→ │ Adapter      │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
│          ↓                  ↓                  ↓            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Project     │  │ Test         │  │ Cost         │       │
│  │ Manager     │  │ Coordinator  │  │ Tracker      │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: ROVER (Task Orchestration)                        │
│  • Git worktree isolation                                   │
│  • Docker container management                              │
│  • AI agent execution                                       │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: AI CLI TOOLS (Isolated Agents)                    │
│  ┌───────────┬───────────┬───────────┐                      │
│  │  Claude   │  Gemini   │ Copilot   │                      │
│  │  Expert   │  Worker   │ Specialist│                      │
│  └───────────┴───────────┴───────────┘                      │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: MCP SERVERS (Shared Tools)                        │
│  18 servers: filesystem, github, docs, sqlite, ...          │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Layers

### Layer 4: Lazy Bird (NEW - Automation)

**Purpose:** Autonomous workflow orchestration

**Components:**
- **Issue Watcher** - GitHub issue polling and detection
- **Agent Selector** - Intelligent AI routing based on cost optimization
- **Rover Adapter** - Translation layer to Rover CLI
- **Project Manager** - Multi-project configuration
- **Test Coordinator** - Test validation and retry logic
- **Cost Tracker** - Usage monitoring and budget alerts

**Key Features:**
- Polls GitHub every 60 seconds for labeled issues
- Selects optimal AI agent (Claude/Gemini/Copilot) based on labels
- Triggers Rover tasks automatically
- Manages test validation before PR creation
- Implements retry logic with agent escalation
- Tracks costs and suggests optimizations

### Layer 3: Rover (Existing - Orchestration)

**Purpose:** Task isolation and execution

**Responsibilities:**
- Creates isolated git worktrees for each task
- Manages Docker containers for clean environments
- Executes AI CLI tools (Claude Code, Gemini CLI, Copilot CLI)
- Provides task status and logging
- Handles merge operations

**Integration with Layer 4:**
- Receives task requests via CLI from Rover Adapter
- Reports status back through file system and stdout
- Provides workspace paths for test execution
- Merges PRs on success

### Layer 2: AI CLI Tools (Existing - Agents)

**Purpose:** Code generation and implementation

**Agents:**
1. **Claude Code** ($20/mo)
   - Expert-level reasoning
   - Security audits
   - Architecture design
   - Complex debugging

2. **Gemini CLI** (FREE)
   - Large-scale analysis (2M token context)
   - Documentation generation
   - Bulk refactoring
   - 1000 free requests/day

3. **Copilot CLI** (FREE/$10)
   - GitHub-native operations
   - Workflow updates
   - Quick fixes
   - 2000 free/month

### Layer 1: MCP Servers (Existing - Tools)

**Purpose:** Shared tools and data access

**18 Servers:**
- filesystem, memory, github, brave-search
- sequential-thinking, gemini-cli, perplexity
- playwright, docs, postmancer, time, sqlite, etc.

---

## Component Design

### 1. Issue Watcher

**File:** `issue-watcher.py`

**Responsibilities:**
- Poll GitHub API every 60 seconds
- Filter issues by configured labels (e.g., "lazy-bird")
- Track processed issues to avoid duplicates
- Comment on issues with automation status
- Handle multiple projects concurrently

**Configuration:**
```python
{
  "poll_interval": 60,  # seconds
  "watch_labels": ["lazy-bird", "ready-for-implementation"],
  "github_token": "ghp_xxxxx"
}
```

**Key Functions:**
- `_poll_all_projects()` - Main polling loop
- `_fetch_issues(owner, repo, label)` - GitHub API call
- `_process_issue(issue, project)` - Trigger workflow
- `_comment_on_issue(issue, task_id)` - Update issue

### 2. Agent Selector

**File:** `agent-selector.py`

**Responsibilities:**
- Intelligent AI agent routing
- Cost optimization based on label patterns
- Usage tracking and statistics
- Budget alerts and suggestions

**Selection Strategy:**
```python
def select_agent(labels, project_id):
    # 1. Check label-based rules (highest priority)
    if "security" in labels or "architecture" in labels:
        return "claude"  # Expert tasks
    
    if "documentation" in labels or "bulk-refactor" in labels:
        return "gemini"  # Free tier
    
    if "github-workflow" in labels or "quick-fix" in labels:
        return "copilot"  # GitHub specialist
    
    # 2. Check project defaults
    if project_id in project_defaults:
        return project_defaults[project_id]
    
    # 3. Fallback to cost-optimized default
    return "gemini"  # Free tier default
```

**Cost Optimization:**
- Targets 60-70% Gemini, 20-30% Copilot, 10-20% Claude
- Tracks usage percentages
- Suggests agent switching when costs are high
- Alerts at 80% of monthly budget

### 3. Rover Adapter

**File:** `rover-adapter.py`

**Responsibilities:**
- Translate Lazy Bird tasks to Rover CLI commands
- Monitor Rover task execution
- Extract test results from Rover workspaces
- Implement merge/retry decision logic

**Core API:**
```python
class RoverAdapter:
    def create_task(issue_data, project_config, agent) -> task_id
    def monitor_task(task_id) -> status_dict
    def get_test_results(task_id) -> results_dict
    def merge_or_retry(task_id, test_status) -> action
```

**Rover CLI Integration:**
```bash
# Create task
rover task "Issue: Add login\n\nDescription..." \
  --agent gemini \
  --project /workspace/my-app \
  --issue 42

# Monitor status
rover status task-abc123 --json

# Get workspace path
rover workspace task-abc123

# Merge on success
rover merge task-abc123
```

### 4. Project Manager

**File:** `project-manager.py`

**Responsibilities:**
- Load and validate project configurations
- Manage multi-project settings
- Provide project-specific defaults
- Handle project CRUD operations

**Configuration Schema:**
```json
{
  "id": "string",
  "name": "string",
  "type": "python|javascript|go|...",
  "path": "/absolute/path",
  "repo": "https://github.com/owner/repo",
  "branch": "main|master",
  "rover_enabled": true,
  "settings": {
    "test_command": "pytest tests/ -v",
    "build_command": "python -m build",
    "lint_command": "ruff check .",
    "default_agent": "gemini|claude|copilot",
    "max_retries": 3,
    "timeout_minutes": 30
  },
  "labels": {
    "watch": "lazy-bird",
    "ready": "ready-for-implementation"
  }
}
```

### 5. Test Coordinator

**Status:** Future implementation (Phase 2)

**Responsibilities:**
- Execute tests in Rover workspaces
- Parse test results (pytest, jest, junit)
- Validate code quality before PR
- Trigger retries on failures

**Integration:**
```python
def validate_task(rover_task_id, project_config):
    # 1. Get Rover workspace path
    workspace = rover_adapter.get_workspace_path(task_id)
    
    # 2. Run tests in Docker container
    test_cmd = project_config["settings"]["test_command"]
    results = run_in_container(workspace, test_cmd)
    
    # 3. Parse results
    passed = parse_test_results(results)
    
    # 4. Decision
    if passed:
        return "merge"
    elif should_retry(task_id):
        return "retry"
    else:
        return "fail"
```

---

## Data Flow

### End-to-End Workflow

```
1. USER: Create GitHub Issue
   └─> Title: "Add OAuth login"
   └─> Labels: ["lazy-bird", "security"]

2. ISSUE WATCHER: Detect issue (60s poll)
   └─> Fetch from GitHub API
   └─> Check if already processed
   └─> Pass to Agent Selector

3. AGENT SELECTOR: Choose AI
   └─> Analyze labels: ["security"]
   └─> Rule match: security → Claude
   └─> Return: "claude"

4. ROVER ADAPTER: Create Rover task
   └─> Build CLI command:
       rover task "Add OAuth login..." --agent claude
   └─> Execute subprocess
   └─> Extract task ID: "task-abc123"
   └─> Comment on GitHub issue

5. ROVER: Execute task
   └─> Create git worktree
   └─> Start Docker container
   └─> Run Claude Code with MCP servers
   └─> Implement OAuth feature
   └─> Commit changes

6. TEST COORDINATOR: Validate
   └─> Get workspace path
   └─> Run: pytest tests/ -v
   └─> Parse results: 10/10 passed
   └─> Decision: merge

7. ROVER ADAPTER: Merge
   └─> rover merge task-abc123
   └─> Create GitHub PR
   └─> Comment on issue with PR link

8. USER: Review & merge PR
```

### State Machine

```
[NEW ISSUE] 
    ↓
[DETECTED] → (Issue Watcher polls)
    ↓
[AGENT SELECTED] → (Label-based routing)
    ↓
[TASK CREATED] → (Rover CLI invoked)
    ↓
[RUNNING] → (AI implements in container)
    ↓
[TESTING] → (Automated validation)
    ↓
    ├─> [TESTS PASSED] → [MERGED] → [PR CREATED]
    └─> [TESTS FAILED] → [RETRY or FAILED]
```

---

## Integration Points

### GitHub API Integration

**Endpoints Used:**
- `GET /repos/{owner}/{repo}/issues?labels={label}` - Fetch issues
- `POST /repos/{owner}/{repo}/issues/{number}/comments` - Add comments
- `GET /repos/{owner}/{repo}/pulls` - Check PR status

**Authentication:**
- Personal Access Token (PAT)
- Required scopes: `repo`, `workflow`, `write:discussion`

**Rate Limits:**
- 5000 requests/hour (authenticated)
- Lazy Bird uses ~1 request/minute/project = 60/hour

### Rover CLI Integration

**Commands:**
```bash
# Task management
rover task <description> [options]
rover status <task_id> [--json]
rover ls [-w|--watch]
rover workspace <task_id>
rover merge <task_id>

# Configuration
rover init <project_path>
rover config set <key> <value>
```

**Expected Rover Enhancements:**
- `--issue` flag to link GitHub issue
- `--json` output for programmatic parsing
- Task ID in predictable format
- Workspace path API

### AI CLI Integration

**Claude Code:**
```bash
claude-code task "description" --context "files"
```

**Gemini CLI:**
```bash
gemini-cli generate --prompt "description"
```

**Copilot CLI:**
```bash
gh copilot suggest -t shell "description"
```

---

## Cost Optimization Strategy

### Target Distribution

| Agent | Free Tier | Cost | Target % | Monthly Tasks | Monthly Cost |
|-------|-----------|------|----------|---------------|--------------|
| Gemini | 1000/day | $0 | 60-70% | 300-350 | $0 |
| Copilot | 2000/mo | $0-10 | 20-30% | 100-150 | $0-10 |
| Claude | None | $20 | 10-20% | 50-100 | $20 |
| **Total** | - | - | **100%** | **~500** | **$20-30** |

### Label-Based Routing Rules

```json
{
  "high_cost": {
    "labels": ["security", "architecture", "complex"],
    "agent": "claude",
    "justification": "Expert reasoning required"
  },
  "free_tier": {
    "labels": ["documentation", "bulk", "analysis"],
    "agent": "gemini",
    "justification": "Large-scale work, use free tier"
  },
  "github_specialist": {
    "labels": ["github-workflow", "ci-cd", "pr"],
    "agent": "copilot",
    "justification": "GitHub-native operations"
  }
}
```

### Cost Tracking

```python
class CostTracker:
    def track_usage(agent, task_id):
        # Increment usage counter
        # Calculate costs based on agent pricing
        # Check against monthly budget
        # Alert if approaching limit
        pass
    
    def get_monthly_cost():
        gemini_cost = 0  # Free tier
        copilot_cost = 10 if copilot_tasks > 2000 else 0
        claude_cost = 20  # Pro subscription
        return gemini_cost + copilot_cost + claude_cost
    
    def suggest_optimization():
        # Analyze usage patterns
        # Suggest label changes
        # Recommend agent switching
        pass
```

---

## Scalability & Performance

### Concurrent Projects

**Current Capacity:**
- 1-5 projects: Single Issue Watcher instance
- 5-20 projects: Multiple watcher instances (1 per 5 projects)
- 20+ projects: Distributed architecture with message queue

**Bottlenecks:**
- GitHub API rate limits (5000/hour)
- Rover container startup time (~10-30s)
- Docker resource limits (CPU/memory)

**Optimization Strategies:**
1. **Parallel Processing** - Multiple Rover tasks simultaneously
2. **Container Reuse** - Keep warm containers for common stacks
3. **Smart Polling** - Adjust interval based on project activity
4. **Webhook Migration** - Replace polling with GitHub webhooks

### Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Issue Detection Latency | <60s | 60s (polling) |
| Task Creation Time | <5s | ~2s |
| Rover Startup Time | <30s | 10-30s |
| Test Execution Time | <10min | Varies |
| End-to-End Time | <30min | ~15-20min |
| Throughput | 50+ tasks/week | TBD |

---

## Security Considerations

### Secrets Management

**Sensitive Data:**
- GitHub personal access tokens
- API keys (Claude, Gemini)
- Docker registry credentials

**Best Practices:**
1. **Environment Variables** - Never commit secrets to git
2. **Systemd Secrets** - Use systemd EnvironmentFile for services
3. **Key Rotation** - Rotate tokens every 90 days
4. **Least Privilege** - Minimal scopes on GitHub tokens

### Container Security

**Isolation:**
- Each Rover task in separate Docker container
- No shared volumes between tasks
- Network isolation by default

**Hardening:**
- Run containers as non-root user
- Resource limits (CPU, memory)
- Read-only file systems where possible
- Security scanning of container images

### GitHub API Security

**Token Permissions:**
- `repo` - Repository access (required)
- `workflow` - GitHub Actions (required)
- `write:discussion` - Issue comments (required)

**IP Restrictions:**
- Optionally restrict token to specific IPs
- Use GitHub's IP allow list

### Code Execution Security

**Risks:**
- AI-generated code may contain vulnerabilities
- Malicious issue descriptions could exploit prompts

**Mitigations:**
- CodeQL security scanning before merge
- Test validation required
- Human review before production merge
- Rate limiting on issue processing

---

## Future Enhancements

### Phase 2-4 Features

**Phase 2: Core Integration**
- Complete Rover CLI integration
- Test coordinator implementation
- End-to-end workflow validation

**Phase 3: Multi-AI & Multi-Project**
- Advanced agent selection (ML-based)
- Parallel project processing
- Cost prediction before task execution

**Phase 4: Production Optimization**
- Performance optimization (container reuse)
- Monitoring dashboards (Prometheus + Grafana)
- Web UI for task management
- A/B testing different agents on same task

---

## References

- **Lazy Bird:** https://github.com/yusufkaraaslan/lazy-bird
- **Rover:** https://github.com/endorhq/rover
- **Claude API:** https://docs.anthropic.com/
- **Gemini API:** https://ai.google.dev/
- **GitHub API:** https://docs.github.com/en/rest

---

**Last Updated:** 2025-01-08  
**Status:** Phase 1 - Foundation & Documentation  
**Version:** 1.0.0
