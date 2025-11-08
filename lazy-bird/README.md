# 🤖 Lazy Bird - Layer 4 Automation v2.0

> **Autonomous GitHub Issue → Implementation → PR workflow with intelligent project management**
> Layer 4 orchestration with hierarchical guidelines and automatic project initialization

---

## 📋 What is This?

Lazy Bird is the **autonomous automation layer (Layer 4)** that orchestrates the entire AI development stack. It transforms GitHub issues into production-ready code through intelligent routing, automatic project setup, and hierarchical guideline enforcement.

### 🆕 Version 2.0 Highlights

1. ✨ **Hierarchical Guideline System** (Layer 0-4)
   - Zero duplication across all AI agents
   - Intelligent inheritance and specialization
   - Automatic guideline injection per layer

2. 🚀 **Automatic Project Initialization**
   - Auto-detects project type from labels/issue body
   - Assigns to next available slot (Projekt-A/B/C)
   - Creates standard structure (src/, tests/, docs/)
   - Initializes git repository
   - Updates configuration automatically

3. 🎯 **Intelligent Agent Routing**
   - Cost-optimized AI selection (60-70% FREE)
   - Label-based specialization
   - Project-specific defaults
   - Usage tracking & optimization

4. 🔄 **Complete Automation**
   - GitHub Issue → Detection (60s)
   - Project Init → Structure Creation
   - Agent Selection → Implementation
   - Test Validation → PR Creation
   - All while you sleep! ⏰

---

## 🏗️ Architecture (5-Layer System)

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 4: LAZY BIRD (This Directory)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Issue        │→ │ Project      │→ │ Agent        │  │
│  │ Watcher      │  │ Initializer  │  │ Selector     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         ↓                 ↓                  ↓          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Rover        │  │ Project      │  │ Guideline    │  │
│  │ Adapter      │  │ Manager      │  │ Injector     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  📋 Guidelines: LAYER-4.md (inherits 0-3)               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: ROVER (Orchestration)                         │
│  • Git worktree isolation                               │
│  • Docker containerization                              │
│  • Test validation before merge                         │
│  📋 Guidelines: LAYER-3.md (inherits 0-2)               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: AI CLI (Claude/Gemini/Copilot)                │
│  • Tool usage (Read/Write/Edit/Bash)                    │
│  • Code implementation                                  │
│  • Agent-specific optimizations                         │
│  📋 Guidelines: LAYER-2.md + Agent-specific             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: MCP SERVERS (18 Tools)                        │
│  • Filesystem, Git, GitHub, Brave, Docker, etc.         │
│  • Rate limiting & caching                              │
│  📋 Guidelines: LAYER-1.md (inherits 0)                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 0: UNIVERSAL STANDARDS (Basis)                   │
│  • Project structure (src/, tests/, docs/)              │
│  • Naming conventions, code quality, security           │
│  📋 Guidelines: LAYER-0.md (applies to ALL)             │
└─────────────────────────────────────────────────────────┘
```

**See:** [guidelines/LAYER-SYSTEM.md](guidelines/LAYER-SYSTEM.md) for complete architecture

---

## 📁 Directory Structure

```
lazy-bird/
├── scripts/                         # Core Python Scripts
│   ├── issue-watcher.py            # 🔄 GitHub issue monitor (main)
│   ├── project-initializer.py      # ✨ Auto project setup (NEW!)
│   ├── agent-selector.py           # 🎯 AI routing logic
│   ├── rover-adapter.py            # 🚀 Rover CLI bridge
│   ├── project-manager.py          # 📊 Multi-project config
│   └── demo.py                     # 🧪 Demo/testing script
│
├── configs/                         # Configuration Files
│   ├── projects.json               # 📋 4 projects (ai-orchestrator + A/B/C)
│   └── rover-mapping.json          # 🗺️ Agent selection rules
│
├── guidelines/                      # ✨ Hierarchical Guidelines (NEW!)
│   ├── LAYER-SYSTEM.md             # Architecture overview
│   ├── MIGRATION-GUIDE.md          # Migration from v1.0
│   ├── layers/                     # Layer-specific guidelines
│   │   ├── LAYER-0.md              # Universal standards (BASIS)
│   │   ├── LAYER-1.md              # MCP server usage
│   │   ├── LAYER-2.md              # AI CLI general
│   │   ├── LAYER-2-CLAUDE.md       # Claude-specific
│   │   ├── LAYER-2-GEMINI.md       # Gemini-specific
│   │   ├── LAYER-2-COPILOT.md      # Copilot-specific
│   │   ├── LAYER-3.md              # Rover orchestration
│   │   └── LAYER-4.md              # Lazy Bird automation
│   ├── tools/
│   │   └── guideline-injector.py   # 🔧 Auto-injection system
│   └── legacy/                     # Old guidelines (reference)
│
├── systemd/                         # Production Deployment
│   └── lazy-bird-watcher.service   # Systemd service template
│
└── README.md                        # This file
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.10+
python3 --version

# Rover CLI (npm)
npm install -g @endorhq/rover

# Docker (for Rover isolation)
docker --version

# GitHub Personal Access Token
# Create at: https://github.com/settings/tokens
# Scopes: repo, workflow, write:discussion
```

### 1. Setup Environment

```bash
# Navigate to lazy-bird
cd lazy-bird

# Install Python dependencies
pip3 install requests

# Set environment variables
export GITHUB_TOKEN=ghp_your_token_here
export GOOGLE_API_KEY=your_gemini_key_here  # Optional: Free tier
```

### 2. Configure Projects

Projects are auto-created on first issue, but you can pre-configure:

```bash
# Edit configs/projects.json
nano configs/projects.json
```

**Default Configuration:**
```json
{
  "projects": [
    {
      "id": "ai-orchestrator",
      "name": "AI Development Orchestrator",
      "type": "documentation",
      "path": "c:\\Users\\Thomas\\Desktop\\claude config",
      "repo": "https://github.com/LEEI1337/ai-dev-orchestrator",
      "branch": "master",
      "rover_enabled": false
    },
    {
      "id": "projekt-a",
      "name": "Projekt-A",
      "type": "placeholder",
      "path": "c:\\...\\projects\\Projekt-A",
      "rover_enabled": true
    }
  ]
}
```

### 3. Run Issue Watcher

```bash
cd scripts
python3 issue-watcher.py
```

**Output:**
```
🚀 Lazy Bird Issue Watcher started
📊 Monitoring 4 projects
⏱️  Poll interval: 60s

[10:15:30] Checking GitHub issues...
  ✅ ai-orchestrator: 0 new issue(s)
  ✅ projekt-a: 0 new issue(s)
```

### 4. Create First Automated Issue

```bash
# In your GitHub repository:
gh issue create \
  --title "Build E-Commerce Backend API" \
  --label "lazy-bird,python,feature" \
  --body "Create REST API with FastAPI:
- User authentication (JWT)
- Product catalog (CRUD)
- Shopping cart
- Order management"
```

**What Happens:**

```
[10:16:30] Checking GitHub issues...
  ✅ ai-orchestrator: 1 new issue(s)

🎯 Processing Issue #42: Build E-Commerce Backend API
   Labels: lazy-bird, python, feature

   📦 Detected new project - initializing...
   🔍 Detected type: python (from label)
   ✅ Assigning to: Projekt-A
   📁 Creating project structure...
      ✅ src/ tests/ docs/ .github/workflows/
      ✅ requirements.txt, setup.py, .gitignore
   🔧 Git repository initialized
   ⚙️  projects.json updated

   Agent: gemini (no security/architecture labels → FREE!)
   ✅ Created Rover task: task-abc123

Rover executing in isolated worktree...
AI implementing feature...
Tests running...
PR created: #43
Issue #42 commented with status
```

**Cost: $0** (Gemini free tier!)

---

## ✨ New Features (v2.0)

### 1. Automatic Project Initialization

**Trigger:** New issue with `lazy-bird` label + no existing project match

**Process:**
1. Detect project type from labels or issue body:
   - Labels: `python`, `typescript`, `javascript`, `react`, `nextjs`
   - Keywords: "Python", "FastAPI", "React", "Next.js", etc.
   - Default: `python`

2. Find next available slot:
   - Checks Projekt-A, B, C for existing projects
   - A project is "occupied" if it has src/, package.json, requirements.txt, etc.
   - Assigns to first free slot

3. Create standard structure:
   ```
   Projekt-A/
   ├── src/
   │   ├── __init__.py         # Python
   │   └── main.py             # Entry point
   ├── tests/
   │   ├── __init__.py
   │   └── test_example.py     # Sample test
   ├── docs/
   ├── .github/workflows/
   ├── .gitignore              # Type-specific
   ├── requirements.txt        # Python
   ├── setup.py                # Python
   └── README.md               # Generated
   ```

4. Initialize git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial setup for issue #42: ..."
   ```

5. Update `projects.json`:
   ```json
   {
     "id": "projekt-a",
     "name": "Build E-Commerce Backend API",
     "type": "python",
     "path": "...\\projects\\Projekt-A",
     "rover_enabled": true,
     "settings": {
       "test_command": "pytest tests/ -v",
       "build_command": "python -m build",
       "default_agent": "gemini"
     }
   }
   ```

**File:** [scripts/project-initializer.py](scripts/project-initializer.py)

### 2. Hierarchical Guideline System

**Problem Solved:** Guidelines were duplicated across all agents!

**Old Way:**
- `claude-guidelines.md` - 8KB (contains universal rules + Claude-specific)
- `gemini-guidelines.md` - 8KB (contains universal rules + Gemini-specific)
- `copilot-guidelines.md` - 8KB (contains universal rules + Copilot-specific)
- **Total duplication:** ~15KB of repeated universal rules!

**New Way:**
- `LAYER-0.md` - Universal standards (2.6KB) **defined once**
- `LAYER-1.md` - MCP server usage (2.7KB) **extends Layer 0**
- `LAYER-2.md` - AI CLI general (0.2KB) **extends Layer 0-1**
- `LAYER-2-CLAUDE.md` - Claude-specific only (3KB) **extends Layer 0-2**
- `LAYER-2-GEMINI.md` - Gemini-specific only (3KB) **extends Layer 0-2**
- `LAYER-2-COPILOT.md` - Copilot-specific only (3KB) **extends Layer 0-2**
- `LAYER-3.md` - Rover orchestration (0.2KB) **extends Layer 0-2**
- `LAYER-4.md` - Lazy Bird automation (0.3KB) **extends Layer 0-3**

**Zero Duplication!**

**Automatic Injection:**

```python
from guideline_injector import GuidelineInjector

injector = GuidelineInjector()

# Direct Claude CLI usage (Layer 2)
guidelines = injector.get_guidelines_for_layer(layer=2, agent="claude")
# Loads: LAYER-0 + LAYER-1 + LAYER-2 + LAYER-2-CLAUDE

# Rover calling Gemini (Layer 3)
guidelines = injector.get_guidelines_for_layer(layer=3, agent="gemini")
# Loads: LAYER-0 + LAYER-1 + LAYER-2 + LAYER-2-GEMINI + LAYER-3

# Lazy Bird → Rover → Copilot (Layer 4)
guidelines = injector.get_guidelines_for_layer(layer=4, agent="copilot")
# Loads: ALL 8 layers! (LAYER-0 through LAYER-4 + COPILOT-specific)
```

**Benefits:**
- ✅ Universal standards defined once (LAYER-0)
- ✅ Each layer only contains its specific additions
- ✅ Change LAYER-0 → affects ALL agents automatically
- ✅ Clear separation of concerns
- ✅ Easy to add new agents (just add LAYER-2-NEWAGENT.md)

**Documentation:**
- [guidelines/LAYER-SYSTEM.md](guidelines/LAYER-SYSTEM.md) - Complete architecture
- [guidelines/MIGRATION-GUIDE.md](guidelines/MIGRATION-GUIDE.md) - Upgrade from v1.0
- [guidelines/tools/guideline-injector.py](guidelines/tools/guideline-injector.py) - Injection tool

### 3. Intelligent Project Slot Management

**Slots:** Projekt-A, Projekt-B, Projekt-C (expandable)

**Slot Detection:**
```python
def _is_project_occupied(project_path: Path) -> bool:
    """Check if slot has actual project."""

    # Has source code?
    if (project_path / "src").exists():
        return True

    # Has package manager files?
    if (project_path / "package.json").exists():
        return True
    if (project_path / "requirements.txt").exists():
        return True

    # Has git history?
    if (project_path / ".git").exists():
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            capture_output=True
        )
        if int(result.stdout) > 0:
            return True

    return False  # Empty slot
```

**Smart Assignment:**
- First issue → Projekt-A
- Second issue (A occupied) → Projekt-B
- Third issue (A,B occupied) → Projekt-C
- Fourth issue (all occupied) → Error (expand slots or cleanup)

**Slot Recycling:**
```bash
# After project completion, free up slot:
cd projects
mv Projekt-A Projekt-A-ecommerce-finished

# Create fresh slot
mkdir Projekt-A
echo "# Projekt-A" > Projekt-A/README.md

# Update projects.json
# Set type back to "placeholder"
```

---

## 🤖 AI Agent Selection

### Label-Based Routing

| Issue Labels | Selected Agent | Cost | Reason |
|-------------|---------------|------|---------|
| `security`, `architecture`, `complex` | **Claude** | $20/mo | Expert analysis, high code quality |
| `documentation`, `bulk-refactor`, `large-scale` | **Gemini** | **FREE** | Large output, speed, free tier |
| `github-workflow`, `ci-cd`, `quick-fix` | **Copilot** | Free/$10 | GitHub specialization |
| *No specific labels* | **Gemini** | **FREE** | Default (cost optimization) |

### Cost Optimization Target

**Monthly Distribution:**
```
🟢 Gemini:  60-70% of tasks (FREE tier: 1000 requests/day)
🔵 Copilot: 20-30% of tasks (FREE tier: 2000 completions/mo)
🔴 Claude:  10-20% of tasks ($20/mo Claude Pro)
────────────────────────────────────────────────────────────
Total Cost: $20-30/month for 500+ automated tasks
```

**Example Month:**
- 350 issues → Gemini (FREE)
- 100 issues → Copilot (FREE or $10)
- 50 issues → Claude ($20)
- **Total: ~$20-30** instead of $100-200 using Claude for everything!

### Agent-Specific Guidelines

Each agent follows its specialized guidelines:

**Claude (LAYER-2-CLAUDE):**
- Security First (input validation, SQL injection prevention)
- 80-90% test coverage requirement
- Type safety (TypeScript, Python type hints)
- Comprehensive error handling
- Extensive documentation
- Best for: Security audits, architecture design, complex debugging

**Gemini (LAYER-2-GEMINI):**
- Efficiency & speed optimized
- 60-70% test coverage (pragmatic)
- Template-based generation for bulk tasks
- Excellent documentation (superkraft!)
- DRY principles
- Best for: Documentation sprints, bulk refactoring, API generation

**Copilot (LAYER-2-COPILOT):**
- GitHub Actions expertise
- Matrix testing (multiple OS/versions)
- Reusable workflows
- PR/Issue template mastery
- Quick fixes
- Best for: CI/CD pipelines, GitHub automation, dependency updates

**All agents inherit:**
- LAYER-0: Universal standards (project structure, naming, security basics)
- LAYER-1: MCP server usage (18 tools, rate limits, caching)
- LAYER-2: AI CLI basics (tool usage, commits, PRs)

---

## 📝 Components

### Issue Watcher (`issue-watcher.py`)

**Purpose:** Monitor GitHub repositories for labeled issues

**Features:**
- Polls GitHub API every 60 seconds
- Multi-project support (reads from projects.json)
- Filters by configurable watch labels
- Tracks processed issues (prevents duplicates)
- Auto-detects new projects vs existing
- Triggers project initialization when needed
- Comments on issues with status updates
- Error handling with retries

**Key Functions:**
```python
def _process_issue(issue, project):
    # Check if placeholder (new project needed)
    if project.get("type") == "placeholder":
        # Detect type from labels/body
        project_type = self._detect_project_type(labels, body)

        # Initialize new project
        new_project = self.project_initializer.initialize_project(
            issue_title, issue_number, project_type
        )

    # Select optimal agent
    agent = self.agent_selector.select_agent(labels, project_id)

    # Create Rover task
    task_id = self.rover_adapter.create_task(issue, project, agent)
```

**Usage:**
```bash
export GITHUB_TOKEN=ghp_xxxxx
python3 issue-watcher.py
```

### Project Initializer (`project-initializer.py`) ✨ NEW

**Purpose:** Automatic project setup and slot management

**Features:**
- Finds next available project slot (A/B/C)
- Detects project type from labels/issue keywords
- Creates standard directory structure
- Generates type-specific files (package.json, requirements.txt, etc.)
- Initializes git repository with .gitignore
- Updates projects.json automatically
- Windows UTF-8 compatible

**Key Functions:**
```python
def find_available_slot() -> Optional[str]:
    """Find next free Projekt-A/B/C slot."""
    for slot in ["Projekt-A", "Projekt-B", "Projekt-C"]:
        if not self._is_project_occupied(project_path / slot):
            return slot
    return None

def initialize_project(title, issue_num, type) -> Dict:
    """Create complete project structure."""
    slot = find_available_slot()
    _create_project_structure(slot, type)  # src/, tests/, etc.
    _init_git_repo(slot, title)
    _update_projects_json(config)
    return config
```

**Supported Types:**
- `python` - Python with pytest, ruff, black
- `typescript` - TypeScript with jest, eslint
- `javascript` - Node.js with jest
- `react` - React app (creates setup guide for CRA)
- `nextjs` - Next.js app (creates setup guide)

**Usage:**
```bash
# Standalone test
python3 project-initializer.py

# Or automatically via issue-watcher
# (triggered when placeholder project receives issue)
```

### Agent Selector (`agent-selector.py`)

**Purpose:** Cost-optimized AI agent routing

**Features:**
- Label-based selection with fallback rules
- Project-specific default agents
- Usage statistics tracking
- Cost optimization suggestions
- Budget alert system
- Configurable routing rules

**Key Functions:**
```python
def select_agent(labels: List[str], project_id: str) -> str:
    """Select optimal agent based on labels."""

    # Check label rules (security → claude, etc.)
    for rule in self.label_rules:
        if any(label in rule["labels"] for label in labels):
            return rule["agent"]

    # Check project default
    if project_id in self.project_defaults:
        return self.project_defaults[project_id]

    # Fallback to cost-optimized default
    return self.fallback_agent  # "gemini"
```

**Usage:**
```python
from agent_selector import AgentSelector

selector = AgentSelector()
agent = selector.select_agent(["security"], "my-project")
print(agent)  # "claude"

# With statistics
stats = selector.get_usage_stats()
print(f"Gemini: {stats['gemini']['percentage']}%")
```

### Rover Adapter (`rover-adapter.py`)

**Purpose:** Bridge between Lazy Bird and Rover CLI

**Features:**
- Translates GitHub issues to Rover task format
- Executes Rover CLI commands
- Monitors task execution status
- Extracts test results from output
- Implements retry logic on failure
- Agent escalation (gemini → claude on critical failure)
- Cleanup on completion

**Key Functions:**
```python
def create_task(issue_data, project_config, agent) -> str:
    """Create Rover task from GitHub issue."""

    task_description = f"""
    GitHub Issue #{issue_data['number']}: {issue_data['title']}

    {issue_data['body']}

    Requirements:
    - Follow project structure in {project_config['path']}
    - Run tests: {project_config['settings']['test_command']}
    - Ensure all tests pass
    """

    # Execute Rover
    result = subprocess.run([
        "rover", "task",
        task_description,
        "--agent", agent,
        "--project", project_config['path']
    ])

    return extract_task_id(result.stdout)

def monitor_task(task_id) -> Dict:
    """Monitor Rover task until completion."""
    while True:
        status = get_task_status(task_id)
        if status in ["completed", "failed"]:
            return status
        time.sleep(30)
```

### Project Manager (`project-manager.py`)

**Purpose:** Multi-project configuration management

**Features:**
- Loads and validates projects.json
- Project CRUD operations
- Configuration defaults
- Path validation
- Type checking

**Key Functions:**
```python
def get_project(project_id: str) -> Optional[Dict]:
    """Get project configuration by ID."""
    for project in self.projects:
        if project["id"] == project_id:
            return project
    return None

def get_all_projects() -> List[Dict]:
    """Get all configured projects."""
    return self.projects

def update_project(project_id: str, updates: Dict):
    """Update project configuration."""
    # Implementation
```

### Guideline Injector (`guidelines/tools/guideline-injector.py`) ✨ NEW

**Purpose:** Hierarchical guideline loading and injection

**Features:**
- Loads guidelines for specific layer
- Combines all inherited layers
- Agent-specific extensions
- Adds hierarchy headers
- Windows UTF-8 support

**Key Functions:**
```python
def get_guidelines_for_layer(layer: int, agent: str) -> str:
    """Load all guidelines for layer with inheritance."""

    guidelines = []

    # Load cumulative layers
    for i in range(layer + 1):
        guidelines.append(self._read_layer(i))

    # Add agent-specific (Layer 2 only)
    if layer >= 2 and agent:
        guidelines.append(self._read_agent_specific(agent))

    # Combine with headers
    return self._combine_guidelines(guidelines, layer, agent)
```

**Usage:**
```python
from guideline_injector import GuidelineInjector

injector = GuidelineInjector()

# For Lazy Bird → Rover → Gemini
guidelines = injector.get_guidelines_for_layer(4, "gemini")

# Inject into system prompt
enhanced_prompt = injector.inject_into_prompt(4, "gemini", base_prompt)
```

---

## ⚙️ Configuration

### Projects (`configs/projects.json`)

**Complete Example:**

```json
{
  "projects": [
    {
      "id": "ai-orchestrator",
      "name": "AI Development Orchestrator",
      "type": "documentation",
      "path": "c:\\Users\\Thomas\\Desktop\\claude config",
      "repo": "https://github.com/LEEI1337/ai-dev-orchestrator",
      "branch": "master",
      "rover_enabled": false,
      "settings": {
        "test_command": "echo 'No tests for docs'",
        "build_command": "echo 'No build needed'",
        "lint_command": "markdownlint *.md",
        "default_agent": "gemini",
        "max_retries": 3,
        "timeout_minutes": 30
      },
      "labels": {
        "watch": "lazy-bird",
        "ready": "ready-for-implementation"
      }
    },
    {
      "id": "projekt-a",
      "name": "Projekt-A",
      "type": "placeholder",
      "path": "c:\\Users\\Thomas\\Desktop\\claude config\\projects\\Projekt-A",
      "repo": "",
      "branch": "main",
      "rover_enabled": true,
      "settings": {
        "test_command": "echo 'Tests not configured yet'",
        "build_command": "echo 'Build not configured yet'",
        "lint_command": "echo 'Linting not configured yet'",
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

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique project identifier |
| `name` | string | Display name |
| `type` | string | `python`, `typescript`, `react`, `placeholder`, etc. |
| `path` | string | Absolute path to project directory |
| `repo` | string | GitHub repository URL |
| `branch` | string | Main branch name |
| `rover_enabled` | boolean | Use Rover for this project |
| `settings.test_command` | string | Command to run tests |
| `settings.build_command` | string | Command to build project |
| `settings.lint_command` | string | Command to lint code |
| `settings.default_agent` | string | Default AI agent (`claude`, `gemini`, `copilot`) |
| `settings.max_retries` | number | Max retry attempts on failure |
| `settings.timeout_minutes` | number | Task timeout in minutes |
| `labels.watch` | string | Label to watch for (trigger automation) |
| `labels.ready` | string | Label indicating ready for implementation |

### Agent Mapping (`configs/rover-mapping.json`)

```json
{
  "label_rules": [
    {
      "labels": ["security", "architecture", "complex"],
      "agent": "claude",
      "cost_level": "high",
      "description": "Expert-level tasks requiring high code quality"
    },
    {
      "labels": ["documentation", "bulk-refactor", "large-scale"],
      "agent": "gemini",
      "cost_level": "free",
      "description": "Large-scale tasks with free tier optimization"
    },
    {
      "labels": ["github-workflow", "quick-fix", "ci-cd", "pr"],
      "agent": "copilot",
      "cost_level": "low",
      "description": "GitHub-specific operations"
    }
  ],
  "project_defaults": {
    "ai-orchestrator": "gemini",
    "projekt-a": "gemini",
    "projekt-b": "gemini",
    "projekt-c": "gemini"
  },
  "fallback_agent": "gemini",
  "cost_optimization": {
    "target_percentages": {
      "gemini": 65,
      "copilot": 25,
      "claude": 10
    },
    "alert_threshold": {
      "claude": 20
    }
  }
}
```

---

## 🔧 Production Deployment

### Systemd Service (Linux)

```bash
# 1. Copy service file
sudo cp systemd/lazy-bird-watcher.service /etc/systemd/system/

# 2. Edit with your credentials
sudo nano /etc/systemd/system/lazy-bird-watcher.service

# Update these lines:
# Environment="GITHUB_TOKEN=ghp_YOUR_TOKEN"
# WorkingDirectory=/path/to/ai-dev-orchestrator/lazy-bird/scripts
# User=your-username

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Enable auto-start
sudo systemctl enable lazy-bird-watcher

# 5. Start service
sudo systemctl start lazy-bird-watcher

# 6. Check status
sudo systemctl status lazy-bird-watcher

# 7. View logs
sudo journalctl -u lazy-bird-watcher -f
```

### Windows Task Scheduler

```powershell
# Create batch file: start-lazy-bird.bat
@echo off
set GITHUB_TOKEN=ghp_YOUR_TOKEN
set GOOGLE_API_KEY=YOUR_GEMINI_KEY
cd "C:\Users\Thomas\Desktop\claude config\lazy-bird\scripts"
python issue-watcher.py

# Task Scheduler:
# 1. Open Task Scheduler (taskschd.msc)
# 2. Create Task
#    - Name: Lazy Bird Issue Watcher
#    - Trigger: At startup or At logon
#    - Action: Run start-lazy-bird.bat
#    - Settings: Run whether user is logged on or not
```

### Docker Container

```dockerfile
# Dockerfile (example)
FROM python:3.11-slim

WORKDIR /app
COPY lazy-bird/scripts/ /app/scripts/
COPY lazy-bird/configs/ /app/configs/

RUN pip install requests

ENV GITHUB_TOKEN=""
ENV GOOGLE_API_KEY=""

CMD ["python3", "scripts/issue-watcher.py"]
```

```bash
# Build and run
docker build -t lazy-bird-watcher .
docker run -d \
  -e GITHUB_TOKEN=ghp_xxx \
  -e GOOGLE_API_KEY=xxx \
  --name lazy-bird \
  lazy-bird-watcher
```

---

## 📖 Documentation

### Core Documentation

- **This File:** [README.md](README.md) - Overview & quick start
- **Layer System:** [guidelines/LAYER-SYSTEM.md](guidelines/LAYER-SYSTEM.md) - Architecture
- **Migration Guide:** [guidelines/MIGRATION-GUIDE.md](guidelines/MIGRATION-GUIDE.md) - v1 → v2
- **Updates:** [../UPDATES-V2.md](../UPDATES-V2.md) - Version 2.0 changes

### Setup Guides

- **English Setup:** [../docs/LAZY-BIRD-SETUP-EN.md](../docs/LAZY-BIRD-SETUP-EN.md)
- **German Setup:** [../docs/LAZY-BIRD-SETUP-DE.md](../docs/LAZY-BIRD-SETUP-DE.md)
- **Architecture Deep Dive:** [../docs/LAZY-BIRD-ARCHITECTURE.md](../docs/LAZY-BIRD-ARCHITECTURE.md)

### Guidelines

- **Layer 0:** [guidelines/layers/LAYER-0.md](guidelines/layers/LAYER-0.md) - Universal standards
- **Layer 1:** [guidelines/layers/LAYER-1.md](guidelines/layers/LAYER-1.md) - MCP servers
- **Layer 2:** [guidelines/layers/LAYER-2.md](guidelines/layers/LAYER-2.md) - AI CLI
- **Layer 3:** [guidelines/layers/LAYER-3.md](guidelines/layers/LAYER-3.md) - Rover
- **Layer 4:** [guidelines/layers/LAYER-4.md](guidelines/layers/LAYER-4.md) - Lazy Bird

### Project Management

- **Projects Guide:** [../projects/README.md](../projects/README.md)

---

## 🎯 Use Cases & Examples

### Example 1: E-Commerce Backend (FREE)

**Issue:**
```markdown
Title: Build E-Commerce Backend API
Labels: lazy-bird, python, feature

Description:
Create REST API with FastAPI:
- User authentication (JWT)
- Product catalog (CRUD)
- Shopping cart
- Order management
- Payment integration (Stripe)
```

**Automated Flow:**
1. Issue Watcher detects issue (60s)
2. Detects type: `python` (from label)
3. Assigns to: Projekt-A (first free slot)
4. Creates:
   - src/main.py (FastAPI app)
   - src/lib/auth.py (JWT auth)
   - src/lib/products.py (CRUD)
   - src/lib/cart.py
   - tests/ (pytest with 60% coverage)
   - docs/API.md
5. Agent: Gemini (no security label)
6. PR created within 30-60 minutes
7. **Cost: $0** (Gemini free tier)

### Example 2: Security Audit ($1)

**Issue:**
```markdown
Title: Security audit of authentication system
Labels: lazy-bird, security, audit

Description:
Review authentication implementation for:
- SQL injection vulnerabilities
- XSS vulnerabilities
- CSRF protection
- Password hashing (bcrypt)
- Session management
```

**Automated Flow:**
1. Issue Watcher detects
2. Agent: Claude (`security` label)
3. Claude performs thorough audit:
   - 90% test coverage
   - Security-specific tests
   - Comprehensive report
4. PR with fixes + security docs
5. **Cost: ~$0.50** from Claude Pro subscription

### Example 3: GitHub Workflow Update (FREE)

**Issue:**
```markdown
Title: Add dependency auto-update workflow
Labels: lazy-bird, github-workflow

Description:
Create GitHub Action to:
- Run Dependabot weekly
- Auto-merge minor updates
- Create PR for major updates
```

**Automated Flow:**
1. Issue Watcher detects
2. Agent: Copilot (`github-workflow` label)
3. Copilot creates perfect workflow:
   - .github/workflows/dependabot.yml
   - .github/dependabot.yml config
   - Auto-merge action
4. PR created
5. **Cost: $0** (Copilot free tier)

### Example 4: Documentation Sprint (FREE)

**Batch Issues:**
```bash
gh issue create --label "lazy-bird,documentation" --title "API docs for Auth"
gh issue create --label "lazy-bird,documentation" --title "API docs for Products"
gh issue create --label "lazy-bird,documentation" --title "API docs for Cart"
gh issue create --label "lazy-bird,documentation" --title "User guide"
gh issue create --label "lazy-bird,documentation" --title "Deployment guide"
```

**Result:**
- All routed to Gemini (free)
- Parallel processing possible (via Rover)
- Excellent documentation (Gemini's strength)
- **Total cost: $0**

---

## 🧪 Testing & Development

### Test Individual Components

```bash
cd scripts

# Test project initializer
python3 project-initializer.py
# Output: Creates demo project in Projekt-A

# Test agent selector
python3 agent-selector.py
# Output: Shows agent selection for various label combinations

# Test project manager
python3 project-manager.py
# Output: Lists all configured projects

# Test guideline injector
cd ../guidelines/tools
python3 guideline-injector.py
# Output: Shows guidelines for each layer/agent combination

# Test complete demo
cd ../../scripts
python3 demo.py
# Output: Simulates complete workflow with mock data
```

### Integration Testing

```bash
# Start issue watcher in test mode
export GITHUB_TOKEN=ghp_test_token
export TEST_MODE=true
python3 issue-watcher.py

# Create test issue
gh issue create \
  --repo LEEI1337/ai-dev-orchestrator \
  --title "TEST: Auto project init" \
  --label "lazy-bird,python" \
  --body "Test automatic project initialization"

# Observe logs for:
# - Issue detection
# - Type detection
# - Slot assignment
# - Project creation
# - Agent selection
# - Rover task creation
```

---

## 🐛 Troubleshooting

### Issue Not Detected

**Symptoms:** Watcher running but doesn't pick up issues

**Solutions:**
1. Check GITHUB_TOKEN is set and valid:
   ```bash
   curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/user
   ```

2. Verify label matches `labels.watch` in projects.json:
   ```bash
   cat configs/projects.json | grep "watch"
   ```

3. Check issue is in correct repository:
   ```bash
   cat configs/projects.json | grep "repo"
   ```

4. Increase log verbosity:
   ```python
   # In issue-watcher.py
   logging.basicConfig(level=logging.DEBUG)
   ```

### Project Not Initializing

**Symptoms:** Issue detected but project not created

**Solutions:**
1. Check project slots not all occupied:
   ```bash
   cd ../projects
   ls -la Projekt-*
   ```

2. Verify write permissions:
   ```bash
   touch projects/Projekt-A/test.txt
   rm projects/Projekt-A/test.txt
   ```

3. Check git is installed:
   ```bash
   git --version
   ```

4. Run initializer manually with debug:
   ```python
   python3 project-initializer.py
   ```

### Agent Selection Wrong

**Symptoms:** Wrong agent chosen for issue

**Solutions:**
1. Check label rules in rover-mapping.json
2. Verify issue labels match exactly
3. Test agent selector manually:
   ```python
   from agent_selector import AgentSelector
   selector = AgentSelector()
   agent = selector.select_agent(["security"], "test-project")
   print(agent)  # Should be "claude"
   ```

### Rover Task Fails

**Symptoms:** Rover task created but fails

**Solutions:**
1. Check Rover is installed:
   ```bash
   rover --version
   ```

2. Verify Docker is running:
   ```bash
   docker ps
   ```

3. Check project path is accessible:
   ```bash
   ls -la /path/from/projects.json
   ```

4. Review Rover logs:
   ```bash
   rover logs <task-id>
   ```

---

## 🤝 Contributing

Lazy Bird v2.0 is production-ready but extensible!

### Future Enhancements

**High Priority:**
- [ ] Web UI for monitoring (dashboard)
- [ ] Metrics & analytics (Grafana/Prometheus)
- [ ] Slack/Discord notifications
- [ ] Multi-repository support
- [ ] Advanced retry strategies

**Medium Priority:**
- [ ] Custom guideline injection per project
- [ ] A/B testing for agent selection
- [ ] Cost budget limits & alerts
- [ ] Template library for common patterns
- [ ] Plugin system for custom agents

**Low Priority:**
- [ ] GitLab support
- [ ] Bitbucket support
- [ ] Self-hosted LLM support
- [ ] Fine-tuned agent models

### How to Contribute

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Follow guidelines in [../CONTRIBUTING.md](../CONTRIBUTING.md)
4. Test thoroughly
5. Submit PR with clear description

---

## 📜 License

MIT License - see [../LICENSE](../LICENSE)

---

## 🙏 Acknowledgments

### Inspiration & Tools

- **Lazy Bird:** https://github.com/yusufkaraaslan/lazy-bird - Original autonomous development concept
- **Rover:** https://github.com/endorhq/rover - Multi-agent orchestration
- **Anthropic Claude:** https://www.anthropic.com/ - Expert AI agent
- **Google Gemini:** https://ai.google.dev/ - Free-tier powerhouse
- **GitHub Copilot:** https://github.com/features/copilot - GitHub specialist

### Contributors

- **Primary Development:** LEEI1337
- **Architecture Design:** AI Development Orchestrator Team
- **Guideline System:** Hierarchical layer concept
- **Testing & Feedback:** Community

---

## 📞 Support

- **Issues:** https://github.com/LEEI1337/ai-dev-orchestrator/issues
- **Discussions:** https://github.com/LEEI1337/ai-dev-orchestrator/discussions
- **Documentation:** https://github.com/LEEI1337/ai-dev-orchestrator/tree/master/docs
- **Updates:** [../UPDATES-V2.md](../UPDATES-V2.md)

---

**Made with ❤️ for autonomous development in Austria 🇦🇹**

**Version:** 2.0
**Status:** Production Ready
**Last Updated:** 2025-11-08
