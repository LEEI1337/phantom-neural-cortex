# 🤖 AI Development Orchestrator

> **Professional multi-AI development environment with intelligent cost optimization**

Transform your development workflow with 5 harmonized AI systems, 18 MCP servers, and intelligent task orchestration - all for <$15/month.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🎯 What is This?

A **production-ready AI development environment** that intelligently orchestrates multiple AI systems (Claude, Gemini, Copilot, OpenHands) with cost-optimized task distribution, achieving **3-5x faster development** for **<$15/month**.

### Key Features

- 🤖 **5 AI Systems** harmonized with specialized roles
- ⚡ **18 MCP Servers** for extended capabilities
- 💰 **Cost-Optimized** - 60-70% of tasks run FREE
- 🔄 **Parallel Execution** via Rover orchestration
- 🔒 **Isolated Workspaces** with git worktrees & Docker
- 📊 **Intelligent Selection** - right AI for each task type
- 🚀 **Complete Automation** - CI/CD, E2E testing, auto-fixes

---

## 💡 The Big Idea

**Problem:** Using expensive AI (Claude) for everything = $40-50/month
**Solution:** Intelligently distribute tasks across 3 AI systems based on strengths & cost

### Optimized Strategy

```
┌─────────────────────────────────────────────────────────┐
│ Claude (10-20%)    → Security, Architecture   ~$10-15  │
│ Gemini (60-70%)    → Bulk, Docs, Analysis     $0 FREE! │
│ Copilot (20-30%)   → GitHub, Quick Fixes      $0 FREE! │
├─────────────────────────────────────────────────────────┤
│ TOTAL: ~500 tasks/month                     = ~$10-15  │
│ ROI: 3-5x faster development                           │
└─────────────────────────────────────────────────────────┘
```

**Result:** ~75% cost reduction + massive productivity gains!

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ & npm
- **Docker** Desktop (for Rover isolation)
- **Git** 2.25+
- **API Keys:**
  - GitHub Token (free)
  - Brave Search API (free tier)
  - Google Gemini API (1500 free/day)
  - Anthropic Claude API (optional, for Claude Code)

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/ai-dev-orchestrator.git
cd ai-dev-orchestrator

# 2. Install AI CLIs
npm install -g @anthropic-ai/claude-code
npm install -g @github/copilot-cli
npm install -g @google/generative-ai-cli
npm install -g @endorhq/rover

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Initialize
git init  # if not cloned
rover init .

# 5. Verify setup
npm run verify-setup
```

### First Task

```bash
# Try parallel AI orchestration
rover task "Analyze project structure" --agent gemini    # FREE
rover task "Create GitHub PR template" --agent copilot   # FREE
rover task "Review security patterns" --agent claude     # PAID

# Monitor progress
rover ls -w
```

**📖 Full Guide:** [docs/QUICK-START.md](docs/QUICK-START.md)

---

## 📊 System Architecture

### The 3-Layer Stack

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: ROVER (Orchestration)                         │
│  • Manages parallel AI tasks                            │
│  • Git worktree isolation                               │
│  • Docker containerization                              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: AI CLI TOOLS (Isolated)                       │
│  ┌──────────┬──────────┬──────────┐                     │
│  │ Claude   │ Gemini   │ Copilot  │                     │
│  │ Expert   │ Worker   │Specialist│                     │
│  └──────────┴──────────┴──────────┘                     │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: MCP SERVERS (Shared)                          │
│  18 servers: filesystem, github, docs, sqlite, ...      │
└─────────────────────────────────────────────────────────┘
```

### AI Role Specialization

| AI | Role | Cost | Use For | Don't Use For |
|---|---|---|---|---|
| **Claude** | Senior Architect | $15-20/mo | Security, Architecture, Complex Debug | Bulk ops, Docs, GitHub |
| **Gemini** | Bulk Worker | **$0/mo** | Large analysis, Docs, Refactoring | Security audits, GitHub |
| **Copilot** | GitHub Specialist | **$0/mo** | PR, Issues, Quick fixes | Large analysis, Security |

**📖 Full Details:** [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)

---

## 🎓 Documentation

### Getting Started
- **[Quick Start](docs/QUICK-START.md)** - 5-minute setup guide
- **[Setup Guide](docs/setup/SETUP-GUIDE.md)** - Detailed installation
- **[Setup Verification](docs/setup/SETUP-VERIFICATION.md)** - Test your setup

### Architecture & Strategy
- **[Architecture Overview](docs/architecture/ARCHITECTURE.md)** - 3-layer system explained
- **[AI Capability Matrix](docs/architecture/AI-CAPABILITY-MATRIX.md)** - Cost & capability analysis
- **[Claude vs Copilot](docs/architecture/CLAUDE-VS-COPILOT.md)** - When to use what

### Rover Orchestration
- **[Rover Guide](docs/guides/ROVER-GUIDE.md)** - Multi-agent orchestration
- **[AI Selector](docs/guides/ROVER-AI-SELECTOR.md)** - Intelligent task routing
- **[Workflows](docs/guides/ROVER-AI-SELECTOR.md#workflows)** - Real-world examples

### Reference
- **[MCP Servers](docs/MCP-SERVERS.md)** - All 18 servers explained
- **[Custom Agents](config/AGENTS.md)** - 4 specialized agents
- **[OpenHands Setup](docs/setup/OPENHANDS-SETUP.md)** - E2E & CI/CD automation

---

## 💰 Cost Breakdown

### Monthly Costs (Real)

```
┌─────────────────────────────────────────────────────┐
│ Service         │ Usage    │ Free Tier  │ Cost     │
├─────────────────────────────────────────────────────┤
│ Gemini AI       │ 60-70%   │ 1500/day   │ $0       │
│ Copilot CLI     │ 20-30%   │ Unlimited  │ $0       │
│ Claude Code     │ 10-20%   │ Limited    │ ~$10-15  │
│ OpenHands       │ Optional │ $10 credit │ $0       │
│ Rover           │ Unlimited│ Open source│ $0       │
│ MCP Servers     │ Unlimited│ All local  │ $0       │
├─────────────────────────────────────────────────────┤
│ TOTAL                                   │ ~$10-15  │
└─────────────────────────────────────────────────────┘
```

### Cost Optimization Examples

**Feature Development** (~$5)
```bash
rover task "Analyze impact" --agent gemini          # $0
rover task "Design architecture" --agent claude     # $2
rover task "Implement 30 components" --agent gemini # $0
rover task "Security review" --agent claude         # $3
rover task "Create PR" --agent copilot              # $0
```

**Documentation Sprint** ($0!)
```bash
rover task "Generate API docs (200 endpoints)" --agent gemini  # $0
rover task "Create integration guide" --agent gemini           # $0
rover task "Generate code examples" --agent gemini             # $0
# All parallel, all FREE!
```

**📊 Full Analysis:** [docs/OPTIMIZATION-SUMMARY.md](docs/OPTIMIZATION-SUMMARY.md)

---

## 🛠️ What's Included

### AI Systems (5)
- ✅ **Claude Code** - Complex reasoning, debugging (18 MCP servers, 22 skills)
- ✅ **Google Gemini** - 2M token analysis, bulk operations (8 MCP servers)
- ✅ **GitHub Copilot** - GitHub native operations (9 MCP servers)
- ✅ **OpenHands** - Autonomous E2E testing & CI/CD
- ✅ **Rover** - Multi-agent orchestration

### MCP Servers (18)
- filesystem, memory, github, brave-search
- sequential-thinking, gemini-cli, perplexity
- playwright, browser-tools, studentofjs
- mcp-inspector, copilot-cli, docs
- postmancer, time, sqlite, postgres, Rover

### Custom Agents (4)
- **@code-expert** - Code review & architecture
- **@debug-specialist** - 4-phase debugging
- **@api-tester** - API testing with Postmancer
- **@gemini-specialist** - Large-scale analysis

### Automation (6)
- OpenHands Auto-Fix (label issue → auto PR)
- E2E Tests (Chromium, Firefox, WebKit)
- Complete CI/CD Pipeline
- Pre-commit Quality Gates
- Repository Setup Scripts
- Parallel Task Orchestration

---

## 🎯 Use Cases

### ✅ Perfect For

- 🚀 Rapid feature development (3-5x faster)
- 🏗️ Architecture design & reviews
- 🔐 Security audits & code reviews
- 📚 Large-scale documentation
- 🐛 Complex debugging & root cause analysis
- 🔄 Repository-wide refactoring
- 🧪 E2E test automation
- 💰 Cost-conscious development (<$15/month)

### Example Workflows

**Parallel Feature Development**
```bash
rover task "Design user roles system" --agent claude
rover task "Implement RBAC in 30 files" --agent gemini
rover task "Create E2E tests" --agent gemini
rover task "Update GitHub workflow" --agent copilot

rover ls -w  # Monitor all tasks
rover merge 1 2 3 4  # Merge when ready
```

**Auto-Fix Bug from GitHub Issue**
```
1. Create GitHub Issue: "Fix login bug"
2. Add label: "openhands"
3. ✨ OpenHands auto-creates fix PR
4. Review & merge
```

---

## 📈 Performance Metrics

- **Setup Time:** ~45 minutes (one-time)
- **MCP Server Start:** ~10-15 seconds
- **Agent Response:** <3 seconds
- **Parallel Speedup:** 3-5x faster
- **Context Window:** Up to 2M tokens (Gemini)
- **Daily Free Requests:** 1500+ (Gemini)
- **Monthly Cost:** <$15 (with optimization)

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### Ways to Contribute

- 🐛 Report bugs or issues
- 💡 Suggest new features or workflows
- 📝 Improve documentation
- 🔧 Add new MCP servers or agents
- 🎨 Share your optimization strategies

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Anthropic](https://www.anthropic.com/)** - Claude Code & API
- **[Google](https://ai.google.dev/)** - Gemini AI with 2M context
- **[GitHub](https://github.com/)** - Copilot CLI
- **[Endor Labs](https://www.endorlabs.com/)** - Rover orchestration
- **[OpenHands](https://github.com/OpenHands/OpenHands)** - Autonomous AI development
- **[Model Context Protocol](https://modelcontextprotocol.io/)** - MCP specification

---

## 🔗 Links

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/ai-dev-orchestrator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/ai-dev-orchestrator/discussions)

---

## ⚡ Quick Links

| Document | Description |
|---|---|
| [Quick Start](docs/QUICK-START.md) | Get started in 5 minutes |
| [Architecture](docs/architecture/ARCHITECTURE.md) | System design & flow |
| [Cost Analysis](docs/OPTIMIZATION-SUMMARY.md) | Detailed cost breakdown |
| [Rover Guide](docs/guides/ROVER-GUIDE.md) | Orchestration workflows |
| [AI Selector](docs/guides/ROVER-AI-SELECTOR.md) | Task routing logic |
| [MCP Servers](docs/MCP-SERVERS.md) | Server reference |

---

<div align="center">

**Made with ❤️ by developers, for developers**

[⭐ Star this repo](https://github.com/YOUR_USERNAME/ai-dev-orchestrator) if you find it useful!

</div>
