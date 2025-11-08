# 🚀 Rover - Multi-Agent Orchestration Guide

**Version:** 2.0 - Optimized Edition
**Status:** ✅ Initialized with Intelligent Agent Selection
**Detected Agents:** Claude (Expert), Gemini (Worker), Copilot (GitHub Specialist)

---

## Was ist Rover?

**Rover** von Endor ist ein **Multi-Agent Manager** der mehrere AI-Coding-Agents **parallel** orchestriert:

### Key Features:
- 🔄 **Parallel Task Execution** - Mehrere Agents gleichzeitig
- 🔒 **Isolated Workspaces** - Git Worktrees für jede Task
- 🐳 **Docker Containers** - Sichere Isolation
- 🤖 **Multi-Agent Support** - Claude, Gemini, Copilot (optimiert!)
- 📊 **Task Management** - Create, inspect, merge, iterate
- 💰 **Cost Optimization** - Intelligente Agent-Auswahl (<$10/month!)

### ⚡ NEU: Intelligente Agent-Rollen

| Agent | Rolle | Kosten | Optimal für |
|-------|-------|--------|-------------|
| **Claude** | Senior Architect | $$$ (TEUER) | Security, Architecture, Debugging |
| **Gemini** | Bulk Worker | $0 (1500/day) | Docs, Analysis, Refactoring |
| **Copilot** | GitHub Specialist | $0 (in Sub) | PR, Issues, Quick Fixes |

**Siehe:** [ROVER-AI-SELECTOR.md](ROVER-AI-SELECTOR.md) für detaillierte Auswahl-Strategie
**Siehe:** [AI-CAPABILITY-MATRIX.md](AI-CAPABILITY-MATRIX.md) für vollständige Analyse

---

## Quick Start

### Installation
```bash
# Global installation
npm install -g @endorhq/rover@latest

# Verify
rover --version  # Should show 1.4.1+
```

### Initialization (✅ Already Done!)
```bash
# In your repository
rover init .

# Rover detects:
# ✓ Git repository
# ✓ Docker installed
# ✓ Claude installed
# ✓ Gemini installed
```

---

## Core Commands

### 1. Create Task
```bash
# Basic task
rover task "Fix login button on mobile"

# With specific agent
rover task "Analyze performance" --agent gemini

# With description file
rover task @task-description.md
```

### 2. List Tasks
```bash
# All tasks
rover ls

# With details (watch mode)
rover ls -w

# Filter by status
rover ls --status running
rover ls --status completed
```

### 3. Inspect Task
```bash
# View task details
rover inspect <task-id>

# Example
rover inspect 1
```

### 4. Diff Changes
```bash
# See what changed
rover diff <task-id>

# Example
rover diff 1
```

### 5. Merge Task
```bash
# Merge completed task to main branch
rover merge <task-id>

# Example
rover merge 1
```

### 6. Iterate on Task
```bash
# Additional passes with agent
rover iterate <task-id> "Add more tests"

# Example
rover iterate 1 "Improve error handling"
```

### 7. Shell into Task
```bash
# Jump into task workspace
rover shell <task-id>

# Manual edits possible
# Exit with: exit
```

### 8. Cancel Task
```bash
# Stop running task
rover cancel <task-id>

# Example
rover cancel 1
```

### 9. Clean Up
```bash
# Remove completed tasks
rover cleanup

# Remove specific task
rover cleanup <task-id>
```

---

## Parallel Execution - The Right Way!

### ❌ Old Way (Manual Terminals):
```bash
# Terminal 1
claude "task 1"

# Terminal 2
gemini "task 2"

# Terminal 3
copilot "task 3"

# Problem: No isolation, conflicts possible, hard to manage
```

### ✅ Rover Way (Orchestrated):
```bash
# Single terminal, all parallel!
rover task "Fix authentication bug" --agent claude
rover task "Optimize database queries" --agent gemini
rover task "Update documentation" --agent claude

# Rover manages:
# - Isolated git worktrees
# - Separate Docker containers
# - No conflicts
# - Easy to track progress
```

### Watch All Tasks:
```bash
# Monitor all parallel tasks
rover ls -w

# Output:
# ID  Status    Agent    Task
# 1   running   claude   Fix authentication bug
# 2   running   gemini   Optimize database queries
# 3   pending   claude   Update documentation
```

---

## Workflows

### Workflow 1: Feature Development
```bash
# 1. Create parallel tasks
rover task "Implement user profile UI" --agent claude
rover task "Create user profile API" --agent gemini
rover task "Write E2E tests" --agent claude

# 2. Monitor progress
rover ls -w

# 3. Inspect completed tasks
rover inspect 1
rover inspect 2

# 4. Review changes
rover diff 1
rover diff 2

# 5. Merge when ready
rover merge 1
rover merge 2
rover merge 3
```

### Workflow 2: Bug Fixing
```bash
# 1. Create task from GitHub issue
rover task "$(gh issue view 123 --json body -q .body)"

# 2. Let agent work in background
# (You continue with other work)

# 3. Agent finishes
rover inspect 1

# 4. Looks good? Merge!
rover merge 1
```

### Workflow 3: Large Refactoring
```bash
# 1. Use Gemini for large-scale analysis
rover task "Analyze codebase for performance issues" --agent gemini

# 2. Wait for analysis
rover ls -w

# 3. Create specific fix tasks
rover task "Optimize component rendering" --agent claude
rover task "Reduce bundle size" --agent claude
rover task "Database query optimization" --agent gemini

# 4. All work in parallel!
# 5. Merge incrementally
```

### Workflow 4: Documentation Sprint
```bash
# Parallel doc generation
rover task "Generate API docs for auth module" --agent gemini
rover task "Generate API docs for user module" --agent gemini
rover task "Generate API docs for payment module" --agent gemini
rover task "Create README examples" --agent claude

# Gemini's 2M token context perfect for docs!
```

---

## 💰 Agent Selection Guide (KOSTEN-OPTIMIERT!)

### 🔐 Claude = Expensive Expert (10-20% usage, ~$15-20/month)
**NUR für kritische Tasks!**

✅ **USE Claude for:**
- Security audits & vulnerability analysis
- Architecture design & system patterns
- Complex debugging & root cause analysis
- Cryptography & payment flow reviews
- Critical code path reviews

❌ **DON'T use Claude for:**
- Simple bug fixes (→ Copilot)
- Bulk operations (→ Gemini)
- Documentation (→ Gemini)
- GitHub operations (→ Copilot)

**Example:**
```bash
rover task "Security audit of authentication system" --agent claude
rover task "Debug race condition in payment handler" --agent claude
rover task "Design microservices architecture" --agent claude
```

---

### 📚 Gemini = Free Workhorse (60-70% usage, $0/month!)
**MAXIMIZE usage! 1500 free/day!**

✅ **USE Gemini for:**
- Large-scale documentation (2M token context!)
- Repository-wide analysis & refactoring
- Bulk code generation (>10 files)
- Dependency mapping & analysis
- Performance analysis across codebase
- Data processing & test generation

❌ **DON'T use Gemini for:**
- Security-critical code (→ Claude)
- GitHub-specific operations (→ Copilot)

**Example:**
```bash
rover task "Generate docs for all 200 API endpoints" --agent gemini
rover task "Analyze all 500 files for performance" --agent gemini
rover task "Refactor 50 components to new pattern" --agent gemini
```

---

### 🐙 Copilot = GitHub Specialist (20-30% usage, $0/month!)
**Already paid! Use freely!**

✅ **USE Copilot for:**
- GitHub PR, Issues, Workflows operations
- Quick bug fixes & single-file edits
- Linting, formatting, config updates
- E2E test execution
- Terminal commands & scripts

❌ **DON'T use Copilot for:**
- Large multi-file analysis (→ Gemini)
- Security audits (→ Claude)
- Complex debugging (→ Claude)

**Example:**
```bash
rover task "Create PR for bug fix" --agent copilot
rover task "Fix typo in README" --agent copilot
rover task "Update GitHub Actions workflow" --agent copilot
```

---

### 🎯 Quick Decision Tree

```
Task Type?
├─ GitHub PR/Issue/Workflow? → **Copilot** ($0)
├─ Security/Architecture/Debug? → **Claude** ($$$)
├─ Large/Bulk/Docs? → **Gemini** ($0)
├─ Quick Fix? → **Copilot** ($0)
└─ Default → **Gemini** ($0, most free tier!)
```

**📖 Detailed Guide:** See [ROVER-AI-SELECTOR.md](ROVER-AI-SELECTOR.md)

---

## Configuration

### Rover Config (`.rover/`)
Rover creates a `.rover` directory with:
- Task metadata
- Workspace configurations
- Agent preferences

### Environment Variables
```bash
# In .env
ANTHROPIC_API_KEY=sk-ant-...  # For Claude
GOOGLE_API_KEY=AIza...         # For Gemini

# Rover container settings
ROVER_CONTAINER_RUNTIME=docker
ROVER_MAX_PARALLEL_TASKS=2
ROVER_AUTO_CLEANUP=true
ROVER_CONTAINER_MEMORY=2g
ROVER_CONTAINER_CPU=1.5
```

### Optimize for Desktop
```bash
# .env settings
ROVER_MAX_PARALLEL_TASKS=2      # Max 2 parallel (desktop optimized)
ROVER_CONTAINER_MEMORY=2g       # 2GB per container
ROVER_CONTAINER_CPU=1.5         # 1.5 CPU cores
ROVER_AUTO_CLEANUP=true         # Auto-remove completed tasks
```

---

## Integration with Other Tools

### OpenHands + Rover
```bash
# Use Rover for task management
rover task "Implement feature X" --agent claude

# OpenHands for E2E test generation
openhands "Generate E2E tests for feature X"

# Both work in parallel!
```

### GitHub Actions + Rover
```yaml
# .github/workflows/rover-tasks.yml
name: Rover Auto-Tasks

on:
  issues:
    types: [labeled]

jobs:
  rover-task:
    if: contains(github.event.issue.labels.*.name, 'rover')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Rover
        run: |
          rover task "${{ github.event.issue.body }}"
```

---

## Best Practices

### 1. Task Granularity
**Good:**
```bash
rover task "Add OAuth2 login support"
rover task "Write unit tests for auth service"
rover task "Update auth documentation"
```

**Bad:**
```bash
rover task "Build entire authentication system"
# Too broad, better to split
```

### 2. Review Before Merge
```bash
# Always inspect
rover inspect <task-id>

# Always diff
rover diff <task-id>

# Then merge
rover merge <task-id>
```

### 3. Use Appropriate Agent
```bash
# Large analysis → Gemini
rover task "Analyze 1000+ files" --agent gemini

# Complex logic → Claude
rover task "Debug race condition" --agent claude
```

### 4. Parallel Efficiency
```bash
# Independent tasks? Parallel!
rover task "Feature A" --agent claude
rover task "Feature B" --agent claude
rover task "Feature C" --agent gemini

# Dependent tasks? Sequential!
rover task "Create API endpoint"
# Wait for completion, then:
rover task "Create E2E tests for endpoint"
```

---

## Troubleshooting

### Rover init fails
```bash
# Ensure git repository
git init
git add .
git commit -m "initial"

# Then retry
rover init .
```

### Docker not found
```bash
# Install Docker Desktop (Windows)
# Or Docker Engine (Linux)

# Verify
docker --version
```

### Task stuck
```bash
# Check task status
rover inspect <task-id>

# Cancel if needed
rover cancel <task-id>

# Check Docker containers
docker ps
```

### Agent not detected
```bash
# Claude
claude --version

# Gemini
gemini --version

# Ensure in PATH
```

---

## Advanced Features

### Custom Workflows
Create `.rover/workflows/` directory:
```yaml
# .rover/workflows/feature-flow.yml
name: Feature Development
steps:
  - task: "Design architecture"
    agent: claude
  - task: "Implement feature"
    agent: claude
  - task: "Generate tests"
    agent: gemini
  - task: "Write docs"
    agent: gemini
```

### Task Templates
```bash
# .rover/templates/bugfix.md
## Bug Description
${description}

## Steps to Reproduce
1. ...

## Expected Behavior
...

## Actual Behavior
...

# Use template
rover task @.rover/templates/bugfix.md
```

---

## Monitoring & Metrics

### Task Statistics
```bash
# View all task history
rover ls --all

# Performance metrics
rover stats

# Example output:
# Total Tasks: 45
# Completed: 40
# Failed: 2
# Running: 3
# Avg Duration: 12.5 min
```

### Resource Usage
```bash
# Docker stats
docker stats

# Show Rover containers
docker ps | grep rover
```

---

## VS Code Extension

### Install
```bash
# VS Code Extension available
# Search: "Rover"
# Or: code --install-extension endor.rover
```

### Features:
- ✅ Task creation from editor
- ✅ Inline task status
- ✅ One-click merge
- ✅ Diff viewer
- ✅ Agent selection

---

## Cost Optimization with Rover

### Free Tier Usage:
- **Gemini:** 1500 req/day FREE → Use for large tasks
- **Claude:** Rate limited → Use for complex tasks
- **Rover:** Free software

### Strategy:
```bash
# Large scale → Gemini (free)
rover task "Analyze 500 files" --agent gemini

# Complex reasoning → Claude
rover task "Security review" --agent claude

# Parallel both:
rover task "Gemini task 1" --agent gemini
rover task "Gemini task 2" --agent gemini  # Still free!
rover task "Claude task" --agent claude
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `rover task "description"` | Create new task |
| `rover ls` | List all tasks |
| `rover ls -w` | Watch tasks (live updates) |
| `rover inspect <id>` | View task details |
| `rover diff <id>` | Show changes |
| `rover merge <id>` | Merge to main branch |
| `rover iterate <id> "msg"` | Additional agent pass |
| `rover shell <id>` | Jump into workspace |
| `rover cancel <id>` | Stop task |
| `rover cleanup` | Remove completed tasks |

---

**Rover macht Multi-Agent Orchestrierung einfach und sicher!** 🚀

**Next Steps:**
1. Try: `rover task "Your first task" --agent claude`
2. Monitor: `rover ls -w`
3. Review: `rover inspect 1`
4. Merge: `rover merge 1`

**Happy parallel coding! 🎯**
