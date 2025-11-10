# 🤖 Lazy Bird Integration - Setup Guide (English)

> **Autonomous GitHub Issue → Implementation → PR workflow**  
> Add Layer 4 (Automation) above Rover for fully automated development

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)

---

## Overview

**Lazy Bird** is an autonomous orchestration layer that sits **above Rover**, creating a 4-layer AI development system:

```
┌─────────────────────────────────────────┐
│  LAYER 4: LAZY BIRD (Automation)        │
│  • Watches GitHub/GitLab issues         │
│  • Triggers Rover tasks automatically   │
│  • Manages multi-project workflows      │
│  • Handles test validation & retries    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  LAYER 3: ROVER (Task Orchestration)    │
│  • Creates isolated git worktrees       │
│  • Manages Docker containers            │
│  • Executes AI agent tasks              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  LAYER 2: AI CLIs (Isolated)            │
│  ┌──────┬──────┬──────┐                 │
│  │Claude│Gemini│Copilot                 │
│  └──────┴──────┴──────┘                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  LAYER 1: MCP SERVERS (Shared)          │
│  18 servers with tools & data           │
└─────────────────────────────────────────┘
```

### Key Benefits

- ✅ **Save 20-100 hours/month** on repetitive development tasks
- ✅ **Work autonomously** while you're away (morning issue → evening merge)
- ✅ **Leverage existing Rover** isolation & multi-AI orchestration
- ✅ **Test-driven validation** before PR creation
- ✅ **Automatic retries** on test failures
- ✅ **Cost-optimized** - 60-70% of tasks run FREE

---

## Architecture

### Component Interactions

```
GitHub Issue (label: "lazy-bird")
    ↓
Issue Watcher (polls every 60s)
    ↓
Agent Selector (chooses Claude/Gemini/Copilot)
    ↓
Rover Adapter (translates to Rover CLI)
    ↓
Rover creates worktree + container
    ↓
AI agent implements task
    ↓
Test Coordinator validates
    ↓
Rover merges or retries
    ↓
GitHub PR created automatically
```

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| **Issue Watcher** | `issue-watcher.py` | Polls GitHub for labeled issues |
| **Agent Selector** | `agent-selector.py` | Chooses optimal AI agent (cost-optimized) |
| **Rover Adapter** | `rover-adapter.py` | Translates tasks to Rover CLI commands |
| **Project Manager** | `project-manager.py` | Multi-project configuration |

---

## Prerequisites

### System Requirements

- **OS:** Linux (Ubuntu 20.04+) or WSL2
- **RAM:** 16GB minimum (for multi-project)
- **Docker:** Desktop or Podman
- **Node.js:** 22+
- **Python:** 3.10+

### Required Software

```bash
# 1. Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. Install Docker
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 3. Install Python dependencies
sudo apt-get install -y python3 python3-pip

# 4. Install Rover CLI
npm install -g @endorhq/rover

# 5. Install AI CLIs
npm install -g @anthropic-ai/claude-code    # Claude (optional)
npm install -g @github/copilot-cli          # Copilot
npm install -g @google/generative-ai-cli    # Gemini
```

### Required API Keys

1. **GitHub Personal Access Token** (required)
   - Go to: https://github.com/settings/tokens
   - Create token with `repo`, `workflow`, `write:discussion` scopes
   - Export: `export GITHUB_TOKEN=ghp_xxxxx`

2. **Google Gemini API Key** (free tier)
   - Get from: https://ai.google.dev/
   - 1000 free requests/day
   - Export: `export GOOGLE_API_KEY=xxxxx`

3. **Anthropic Claude API** (optional, $20/mo)
   - Only needed for expert-level tasks
   - Get from: https://console.anthropic.com/

4. **GitHub Copilot** (free tier or $10/mo)
   - Free tier: 2000 completions/month
   - Pro: Unlimited

---

## Installation

### Step 1: Clone Repository

```bash
cd /workspace
git clone https://github.com/LEEI1337/ai-dev-orchestrator.git
cd ai-dev-orchestrator
```

### Step 2: Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

Add the following to `.env`:

```bash
# GitHub (Required)
GITHUB_TOKEN=ghp_your_token_here

# Google Gemini (Free tier - Recommended)
GOOGLE_API_KEY=your_gemini_key_here

# Anthropic Claude (Optional - $20/mo)
ANTHROPIC_API_KEY=sk-ant-your_key_here

# GitHub Copilot (Optional - Free/$10)
# Uses GitHub authentication
```

### Step 3: Configure Projects

Edit `lazy-bird/configs/projects.json` to add your projects:

```json
{
  "projects": [
    {
      "id": "my-project",
      "name": "My Awesome Project",
      "type": "python",
      "path": "/workspace/my-project",
      "repo": "https://github.com/user/my-project",
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

### Step 4: Install Python Dependencies

```bash
cd lazy-bird/scripts
pip3 install requests  # For GitHub API
```

### Step 5: Test Configuration

```bash
# Test project manager
python3 project-manager.py

# Test agent selector
python3 agent-selector.py
```

---

## Configuration

### Agent Selection Rules

Edit `lazy-bird/configs/rover-mapping.json` to customize AI agent routing:

```json
{
  "label_rules": [
    {
      "labels": ["security", "architecture", "complex"],
      "agent": "claude",
      "cost_level": "high"
    },
    {
      "labels": ["documentation", "bulk-refactor", "large-scale"],
      "agent": "gemini",
      "cost_level": "free"
    },
    {
      "labels": ["github-workflow", "quick-fix", "pr"],
      "agent": "copilot",
      "cost_level": "free-low"
    }
  ],
  "fallback_agent": "gemini"
}
```

### Systemd Service (Optional)

For production deployment, run Lazy Bird as a system service:

```bash
# Copy service file
sudo cp lazy-bird/systemd/lazy-bird-watcher.service /etc/systemd/system/

# Edit service file with your paths and credentials
sudo nano /etc/systemd/system/lazy-bird-watcher.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable lazy-bird-watcher
sudo systemctl start lazy-bird-watcher

# Check status
sudo systemctl status lazy-bird-watcher

# View logs
sudo journalctl -u lazy-bird-watcher -f
```

---

## Usage

### Manual Mode (Development)

```bash
# Navigate to scripts directory
cd lazy-bird/scripts

# Set environment variables
export GITHUB_TOKEN=ghp_xxxxx

# Run issue watcher manually
python3 issue-watcher.py
```

You'll see output like:

```
🚀 Lazy Bird Issue Watcher started
📊 Monitoring 1 projects
⏱️  Poll interval: 60s

[10:15:30] Polling GitHub issues...
  ✅ ai-orchestrator: 2 new issue(s)

🎯 Processing Issue #42: Add user authentication
   Labels: feature, security
   Agent: claude
   ✅ Created Rover task: task-abc123
```

### Automated Mode (Production)

Once systemd service is configured:

```bash
# Service runs automatically in background
sudo systemctl status lazy-bird-watcher
```

### Creating Automated Issues

1. **Create GitHub Issue** with clear description
2. **Add label:** `lazy-bird` (or your configured watch label)
3. **Optionally add agent hints:**
   - `security` → Routes to Claude (expert)
   - `documentation` → Routes to Gemini (free)
   - `github-workflow` → Routes to Copilot (GitHub specialist)
4. **Wait** - Issue Watcher will pick it up within 60 seconds
5. **Monitor** - Check issue comments for progress updates
6. **Review PR** - Merge when ready!

### Example Workflow

```bash
# 1. Create issue via GitHub CLI
gh issue create \
  --title "Add OAuth login" \
  --body "Implement OAuth2.0 authentication..." \
  --label "lazy-bird,security"

# 2. Lazy Bird detects issue (within 60s)
# 3. Agent Selector chooses Claude (security label)
# 4. Rover creates isolated workspace
# 5. Claude implements OAuth
# 6. Tests run automatically
# 7. PR created if tests pass
# 8. You review and merge!
```

---

## Troubleshooting

### Issue: Watcher not detecting issues

**Solution:**
```bash
# Check GitHub token
echo $GITHUB_TOKEN

# Verify token has correct permissions
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/user

# Check project configuration
python3 project-manager.py
```

### Issue: Rover commands failing

**Solution:**
```bash
# Verify Rover is installed
rover --version

# Check Docker is running
docker ps

# Test Rover manually
rover task "test task" --agent gemini
```

### Issue: Tests not running

**Solution:**
```bash
# Verify test command in projects.json
cat ../configs/projects.json | grep test_command

# Test command manually in project directory
cd /workspace/my-project
pytest tests/ -v
```

### Issue: High costs (using too much Claude)

**Solution:**
```bash
# Check agent usage stats
python3 agent-selector.py

# Review label rules in rover-mapping.json
# Route more tasks to Gemini (free tier)
```

---

## Cost Optimization

### Target Distribution

```
Gemini (FREE):   60-70% of tasks
Copilot (FREE):  20-30% of tasks  
Claude ($20):    10-20% of tasks
────────────────────────────────
Total: $20-30/month
```

### Optimization Tips

1. **Use Gemini for:**
   - Documentation generation
   - Bulk refactoring
   - Large-scale analysis
   - Non-critical features

2. **Use Copilot for:**
   - GitHub workflow updates
   - Quick bug fixes
   - PR reviews
   - CI/CD changes

3. **Use Claude for:**
   - Security audits
   - Architecture design
   - Complex debugging
   - Critical features

4. **Monitor Usage:**
   ```bash
   # Check agent selection stats
   python3 agent-selector.py
   ```

### Cost Examples

**Documentation Sprint** (100% FREE!)
```
Generate API docs for 200 endpoints → Gemini
Create user guide → Gemini
Generate code examples → Gemini
Total: $0 (all free tier)
```

**Feature Development** (~$1 from your $20 subscription)
```
Analyze impact → Gemini ($0)
Design architecture → Claude (~$0.50)
Implement 30 components → Gemini ($0)
Security review → Claude (~$0.50)
Create PR → Copilot ($0)
```

---

## Next Steps

1. ✅ **Test with simple issue** - Start with a documentation task
2. ✅ **Monitor first run** - Watch logs and issue comments
3. ✅ **Review PR** - Check quality of generated code
4. ✅ **Scale gradually** - Add more projects as confidence grows
5. ✅ **Optimize costs** - Review agent usage and adjust labels

---

## Support

- **Documentation:** [Lazy Bird Architecture](LAZY-BIRD-ARCHITECTURE.md)
- **Issues:** [GitHub Issues](https://github.com/LEEI1337/ai-dev-orchestrator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/LEEI1337/ai-dev-orchestrator/discussions)

---

**Made with ❤️ by developers, for developers in Austria 🇦🇹**
