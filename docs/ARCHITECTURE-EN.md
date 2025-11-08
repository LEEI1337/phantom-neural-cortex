# 🏗️ Architecture Overview

**Simple 3-layer architecture for multi-AI orchestration.**

---

## The 3 Layers

```
┌─────────────────────────────────────────┐
│  LAYER 3: ROVER                         │
│  • Orchestrates parallel AI tasks       │
│  • Creates isolated git worktrees       │
│  • Manages Docker containers            │
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
│  18 servers providing tools & data      │
└─────────────────────────────────────────┘
```

---

## AI Role Specialization

### Claude ($20/mo) - Senior Architect
**10-20% of tasks**

✅ Use for:
- Security audits
- Architecture design
- Complex debugging
- Code reviews

❌ Don't use for:
- Bulk operations → Gemini
- GitHub ops → Copilot
- Documentation → Gemini

### Gemini (FREE!) - Bulk Worker
**60-70% of tasks**

✅ Use for:
- Large-scale documentation (2M token context!)
- Repository-wide analysis
- Bulk refactoring
- Data processing

❌ Don't use for:
- Security-critical code → Claude
- GitHub operations → Copilot

### Copilot ($0-10/mo) - GitHub Specialist
**20-30% of tasks**

✅ Use for:
- GitHub PR/Issues
- Quick fixes
- Single-file edits
- Workflow updates

❌ Don't use for:
- Large analysis → Gemini
- Security audits → Claude

---

## MCP Servers (18 Total)

**Shared by all AIs, but configured separately:**

- `filesystem` - File operations
- `github` - GitHub integration
- `memory` - Context persistence
- `docs` - Documentation search
- `gemini-cli` - Gemini access
- `copilot-cli` - Copilot access
- `sqlite` - Database operations
- `playwright` - Browser automation
- `brave-search` - Web search
- ... and 9 more

Each AI CLI has its own `.mcp.json` or config file.

---

## Key Principles

### 1. Isolation
Each AI CLI is **completely isolated**:
- Separate configs
- Separate MCP server lists
- No direct communication

### 2. Specialization
Each AI has an **optimal role**:
- Claude: Expert (expensive, critical only)
- Gemini: Worker (free, maximize usage)
- Copilot: Specialist (GitHub + quick tasks)

### 3. Orchestration
Rover **manages processes**, doesn't access MCP:
- Starts separate CLI processes
- Creates git worktrees
- Runs in Docker containers

---

## Cost Strategy

```
60-70% Gemini   → FREE (1000/day)
20-30% Copilot  → $0-10/month
10-20% Claude   → $20/month
───────────────────────────────
Total: $20-30/month
```

**vs.** using Claude Max for everything: $100-200/month

---

## Data Flow Example

```
User: "Fix security issue in auth.ts"
  ↓
Rover creates isolated workspace
  ↓
Rover starts Claude CLI (security task)
  ↓
Claude uses MCP servers:
  - filesystem (read auth.ts)
  - github (check PR history)
  - memory (remember context)
  ↓
Claude fixes issue
  ↓
Rover merges changes back
```

---

**Learn more:**
- [Documentation Index](INDEX.md) - All documentation organized
- [MCP Servers](MCP-SERVERS.md) - All 18 servers explained
- [Quick Start](QUICKSTART-EN.md) - Get started in 5 minutes
