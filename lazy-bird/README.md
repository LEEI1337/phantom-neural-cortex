# 🤖 Lazy Bird - Layer 4 Automation

> **Autonomous GitHub Issue → Implementation → PR workflow**  
> Orchestration layer above Rover for fully automated development

---

## 📋 What is This?

Lazy Bird is the **automation layer (Layer 4)** that sits above Rover, enabling autonomous software development workflows. It watches GitHub issues and automatically:

1. ✅ Detects issues with specific labels (e.g., "lazy-bird")
2. ✅ Selects optimal AI agent (Claude/Gemini/Copilot) based on cost optimization
3. ✅ Triggers Rover to create isolated workspace + Docker container
4. ✅ Monitors AI agent implementation
5. ✅ Validates with tests before PR creation
6. ✅ Creates PR automatically when ready

**Result:** Save 20-100 hours/month on repetitive tasks while maintaining cost efficiency ($20-30/month).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  LAYER 4: LAZY BIRD (This Directory)    │
│  ┌──────────┐  ┌──────────┐            │
│  │  Issue   │→ │  Agent   │            │
│  │ Watcher  │  │ Selector │            │
│  └──────────┘  └──────────┘            │
│        ↓              ↓                 │
│  ┌──────────┐  ┌──────────┐            │
│  │  Rover   │  │ Project  │            │
│  │ Adapter  │  │ Manager  │            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
              ↓
    Layer 3: ROVER
    Layer 2: AI AGENTS
    Layer 1: MCP SERVERS
```

---

## 📁 Directory Structure

```
lazy-bird/
├── scripts/
│   ├── issue-watcher.py      # GitHub issue polling
│   ├── agent-selector.py     # AI agent routing (cost-optimized)
│   ├── rover-adapter.py      # Rover CLI integration
│   └── project-manager.py    # Multi-project configuration
├── configs/
│   ├── projects.json         # Project definitions
│   └── rover-mapping.json    # Agent selection rules
├── systemd/
│   └── lazy-bird-watcher.service  # Systemd service file
└── README.md                 # This file
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip3 install requests

# Set GitHub token
export GITHUB_TOKEN=ghp_your_token_here
```

### 2. Configure Projects

Edit `configs/projects.json`:

```json
{
  "projects": [
    {
      "id": "my-project",
      "repo": "https://github.com/user/my-project",
      "rover_enabled": true,
      "settings": {
        "test_command": "pytest tests/ -v",
        "default_agent": "gemini"
      },
      "labels": {
        "watch": "lazy-bird"
      }
    }
  ]
}
```

### 3. Run Issue Watcher

```bash
cd scripts
python3 issue-watcher.py
```

### 4. Create Automated Issues

```bash
# Create issue with "lazy-bird" label
gh issue create \
  --title "Add login feature" \
  --body "Implement OAuth..." \
  --label "lazy-bird,security"

# Lazy Bird will:
# 1. Detect issue within 60s
# 2. Select Claude (security label)
# 3. Create Rover task
# 4. Implement & test
# 5. Create PR
```

---

## 🤖 AI Agent Selection

Lazy Bird intelligently routes tasks to the optimal AI agent based on:

### Label-Based Rules

| Labels | Agent | Cost | Use For |
|--------|-------|------|---------|
| `security`, `architecture`, `complex` | **Claude** | $20/mo | Expert tasks |
| `documentation`, `bulk-refactor` | **Gemini** | FREE | Large-scale |
| `github-workflow`, `quick-fix` | **Copilot** | $0-10 | GitHub ops |
| *No specific label* | **Gemini** | FREE | Default |

### Cost Optimization

**Target Distribution:**
- 🟢 Gemini: 60-70% (FREE tier, 1000/day)
- 🔵 Copilot: 20-30% (FREE/$10)
- 🔴 Claude: 10-20% ($20/mo)

**Monthly Cost: $20-30**

---

## 📝 Components

### Issue Watcher (`issue-watcher.py`)

**Purpose:** Monitor GitHub for labeled issues

**Features:**
- Polls GitHub API every 60 seconds
- Filters by configurable labels
- Tracks processed issues (no duplicates)
- Comments on issues with status
- Multi-project support

**Usage:**
```bash
export GITHUB_TOKEN=ghp_xxxxx
python3 issue-watcher.py
```

### Agent Selector (`agent-selector.py`)

**Purpose:** Cost-optimized AI routing

**Features:**
- Label-based agent selection
- Project-specific defaults
- Usage tracking & statistics
- Cost optimization suggestions
- Budget alerts

**Usage:**
```python
from agent_selector import AgentSelector

selector = AgentSelector()
agent = selector.select_agent(["security"], "my-project")
print(agent)  # "claude"
```

### Rover Adapter (`rover-adapter.py`)

**Purpose:** Bridge to Rover CLI

**Features:**
- Translates issues to Rover tasks
- Monitors task execution
- Extracts test results
- Implements merge/retry logic
- Agent escalation on failure

**Usage:**
```python
from rover_adapter import RoverAdapter

adapter = RoverAdapter()
task_id = adapter.create_task(issue_data, project_config, "gemini")
status = adapter.monitor_task(task_id)
```

### Project Manager (`project-manager.py`)

**Purpose:** Multi-project configuration

**Features:**
- Load/validate project configs
- Project-specific settings
- Default agent management
- CRUD operations

**Usage:**
```python
from project_manager import ProjectManager

manager = ProjectManager()
project = manager.get_project("my-project")
```

---

## ⚙️ Configuration

### Project Configuration (`configs/projects.json`)

```json
{
  "projects": [
    {
      "id": "unique-id",
      "name": "Project Name",
      "type": "python|javascript|go",
      "path": "/absolute/path/to/project",
      "repo": "https://github.com/owner/repo",
      "branch": "main",
      "rover_enabled": true,
      "settings": {
        "test_command": "pytest tests/ -v",
        "build_command": "python -m build",
        "lint_command": "ruff check .",
        "default_agent": "gemini",
        "max_retries": 3,
        "timeout_minutes": 30
      },
      "labels": {
        "watch": "lazy-bird",
        "ready": "ready-for-implementation"
      }
    }
  ]
}
```

### Agent Mapping (`configs/rover-mapping.json`)

```json
{
  "label_rules": [
    {
      "labels": ["security", "architecture"],
      "agent": "claude",
      "cost_level": "high"
    }
  ],
  "project_defaults": {
    "my-project": "gemini"
  },
  "fallback_agent": "gemini"
}
```

---

## 🔧 Production Deployment

### Systemd Service

```bash
# 1. Copy service file
sudo cp systemd/lazy-bird-watcher.service /etc/systemd/system/

# 2. Edit with your credentials
sudo nano /etc/systemd/system/lazy-bird-watcher.service

# 3. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable lazy-bird-watcher
sudo systemctl start lazy-bird-watcher

# 4. Check status
sudo systemctl status lazy-bird-watcher

# 5. View logs
sudo journalctl -u lazy-bird-watcher -f
```

---

## 📖 Documentation

- **Setup Guide (EN):** [../docs/LAZY-BIRD-SETUP-EN.md](../docs/LAZY-BIRD-SETUP-EN.md)
- **Setup Guide (DE):** [../docs/LAZY-BIRD-SETUP-DE.md](../docs/LAZY-BIRD-SETUP-DE.md)
- **Architecture:** [../docs/LAZY-BIRD-ARCHITECTURE.md](../docs/LAZY-BIRD-ARCHITECTURE.md)
- **Main README:** [../README.md](../README.md)

---

## 🎯 Use Cases

### Example 1: Documentation Sprint (100% FREE)

```bash
# Create issues
gh issue create --title "Generate API docs" --label "lazy-bird,documentation"
gh issue create --title "Create user guide" --label "lazy-bird,documentation"
gh issue create --title "Add code examples" --label "lazy-bird,documentation"

# Result: All routed to Gemini (FREE), run in parallel
# Cost: $0
```

### Example 2: Security Audit ($1 from $20 subscription)

```bash
# Create issue
gh issue create --title "Security review" --label "lazy-bird,security"

# Result: Routed to Claude (expert), thorough analysis
# Cost: ~$0.50 from Claude Pro subscription
```

### Example 3: GitHub Workflow Update (FREE)

```bash
# Create issue
gh issue create --title "Update CI pipeline" --label "lazy-bird,github-workflow"

# Result: Routed to Copilot (GitHub specialist)
# Cost: $0 (free tier)
```

---

## 🧪 Testing

```bash
# Test project manager
python3 project-manager.py

# Test agent selector
python3 agent-selector.py

# Test with mock data (no Rover required)
python3 rover-adapter.py
```

---

## 🤝 Contributing

This is Phase 1 (Foundation) implementation. Future phases:

- **Phase 2:** Complete Rover integration + test coordinator
- **Phase 3:** Multi-AI optimization + parallel processing
- **Phase 4:** Production monitoring + web UI

Contributions welcome! See [../CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 📜 License

MIT License - see [../LICENSE](../LICENSE)

---

## 🙏 Acknowledgments

- **Lazy Bird:** https://github.com/yusufkaraaslan/lazy-bird - Original concept
- **Rover:** https://github.com/endorhq/rover - Multi-agent orchestration
- **Anthropic Claude:** https://www.anthropic.com/
- **Google Gemini:** https://ai.google.dev/
- **GitHub Copilot:** https://github.com/features/copilot

---

**Made with ❤️ for autonomous development in Austria 🇦🇹**
