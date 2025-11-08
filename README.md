# 🤖 AI Development Orchestrator

> **Professional multi-AI development environment with intelligent cost optimization**

Transform your development workflow with 5 harmonized AI systems, 18 MCP servers, and intelligent task orchestration - starting from $20/month with strategic free tier usage.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Issues](https://img.shields.io/github/issues/LEEI1337/ai-dev-orchestrator)](https://github.com/LEEI1337/ai-dev-orchestrator/issues)
[![GitHub Stars](https://img.shields.io/github/stars/LEEI1337/ai-dev-orchestrator?style=social)](https://github.com/LEEI1337/ai-dev-orchestrator/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/LEEI1337/ai-dev-orchestrator?style=social)](https://github.com/LEEI1337/ai-dev-orchestrator/network/members)
[![Made in Austria](https://img.shields.io/badge/Made%20in-Austria%20🇦🇹-red)](https://github.com/LEEI1337/ai-dev-orchestrator)

---

## 🎯 What is This?

A **production-ready AI development environment** that intelligently orchestrates multiple AI systems (Claude, Gemini, Copilot, OpenHands) with cost-optimized task distribution, achieving **3-5x faster development** for **~$20-30/month** (or $20 minimum with strategic free tier maximization).

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

**Problem:** Using Claude Max for everything = $100-200/month
**Solution:** Intelligently distribute tasks + maximize free tiers

### Optimized Strategy

```
┌─────────────────────────────────────────────────────────┐
│ Claude Pro (10-20%)  → Security, Architecture    $20   │
│ Gemini (60-70%)      → Bulk, Docs, Analysis      $0!   │
│ Copilot (20-30%)     → GitHub, Quick Fixes      $0-10  │
├─────────────────────────────────────────────────────────┤
│ TOTAL: ~500 tasks/month                   = $20-30/mo  │
│ ROI: 3-5x faster development                           │
└─────────────────────────────────────────────────────────┘
```

**Result:** Use free tiers strategically + Claude Pro minimum = $20-30/month!

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ & npm
- **Docker** Desktop (for Rover isolation)
- **Git** 2.25+
- **API Keys:**
  - GitHub Token (free)
  - Brave Search API (free tier)
  - Google Gemini API (1000 free/day)
  - Anthropic Claude API (optional, for Claude Code)

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/LEEI1337/ai-dev-orchestrator.git
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

**📖 Full Guide:** [EN](docs/QUICKSTART-EN.md) | [DE](docs/QUICKSTART-DE.md)

---

## 📊 System Architecture

### The 5-Layer Stack (0-4) with Hierarchical Guidelines ✨

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 4: LAZY BIRD (Automation) 🆕                     │
│  • Auto project init (Projekt-A/B/C slots)              │
│  • Intelligent AI agent routing                         │
│  • Autonomous GitHub Issue → PR workflow                │
│  • Cost-optimized task distribution                     │
│  📋 Guidelines: LAYER-4.md (inherits 0-3)               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: ROVER (Orchestration)                         │
│  • Parallel AI task management                          │
│  • Git worktree isolation                               │
│  • Docker containerization                              │
│  • Test validation & auto-merge                         │
│  📋 Guidelines: LAYER-3.md (inherits 0-2)               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: AI CLI TOOLS (Isolated)                       │
│  ┌──────────┬──────────┬──────────┐                     │
│  │ Claude   │ Gemini   │ Copilot  │                     │
│  │ Expert   │ Worker   │Specialist│                     │
│  └──────────┴──────────┴──────────┘                     │
│  📋 Guidelines: LAYER-2.md + Agent-specific (inherits 0-1) │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: MCP SERVERS (Tools & Data)                    │
│  • 18 servers: filesystem, git, github, brave, etc.     │
│  • Rate limiting & caching                              │
│  • Unified tool interface                               │
│  📋 Guidelines: LAYER-1.md (inherits 0)                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 0: UNIVERSAL STANDARDS (Basis) ⭐                │
│  • Project structure (src/, tests/, docs/)              │
│  • Naming conventions (Python, TypeScript, etc.)        │
│  • Code quality & security basics                       │
│  • Testing fundamentals                                 │
│  📋 Guidelines: LAYER-0.md (applies to ALL)             │
└─────────────────────────────────────────────────────────┘
```

**🆕 Hierarchical Guideline System:**
- Each layer inherits all guidelines from layers below
- Layer 0 = Universal standards (applies to ALL agents)
- Agent-specific guidelines at Layer 2
- Zero duplication, intelligent inheritance
- See: [LAYER-SYSTEM.md](lazy-bird/guidelines/LAYER-SYSTEM.md)

### AI Role Specialization

| AI | Role | Cost | Use For | Don't Use For |
|---|---|---|---|---|
| **Claude** | Senior Architect | Pro $20/mo | Security, Architecture, Complex Debug | Bulk ops, Docs, GitHub |
| **Gemini** | Bulk Worker | **FREE** (1000/day) | Large analysis, Docs, Refactoring | Security audits, GitHub |
| **Copilot** | GitHub Specialist | FREE or Pro $10/mo | PR, Issues, Quick fixes | Large analysis, Security |

**📖 Full Details:** [EN](docs/ARCHITECTURE-EN.md) | [DE](docs/ARCHITECTURE-DE.md)

---

## 🤖 Lazy Bird Automation (NEW!)

**Autonomous GitHub Issue → Implementation → PR** workflow powered by Layer 4 automation.

### What is Lazy Bird?

Lazy Bird adds a fully autonomous orchestration layer **above Rover**, enabling:

- ✅ **Automatic Issue Processing** - Watches GitHub for labeled issues
- ✅ **Intelligent AI Routing** - Chooses optimal agent (Claude/Gemini/Copilot) based on labels
- ✅ **Zero-Touch Development** - Morning issue → Evening PR, no manual intervention
- ✅ **Cost-Optimized** - 60-70% tasks run FREE (Gemini), stays within $20-30/month budget
- ✅ **Test-Driven** - Validates with tests before creating PR
- ✅ **Multi-Project** - Manages 2-20+ projects from single instance

### Quick Example

```bash
# 1. Create GitHub Issue
gh issue create \
  --title "Add OAuth login" \
  --body "Implement JWT-based authentication..." \
  --label "lazy-bird,security"

# 2. Lazy Bird automatically:
#    ✅ Detects issue (60s polling)
#    ✅ Selects Claude (security label)
#    ✅ Creates Rover task
#    ✅ Claude implements in isolated container
#    ✅ Runs tests automatically
#    ✅ Creates PR when tests pass

# 3. You review and merge! 🎉
```

### Benefits

- 💰 **Save 20-100 hours/month** on repetitive tasks
- 🤖 **Work autonomously** while you're away
- 🎯 **Smart agent selection** based on task complexity
- 🔒 **Isolated execution** via Rover + Docker
- 📊 **Cost tracking** and optimization suggestions

### Documentation

- **Setup Guide:** [EN](docs/LAZY-BIRD-SETUP-EN.md) | [DE](docs/LAZY-BIRD-SETUP-DE.md)
- **Architecture:** [Technical Design](docs/LAZY-BIRD-ARCHITECTURE.md)
- **Quick Start:** [lazy-bird/README.md](lazy-bird/README.md)

### Agent Selection Strategy

| Issue Labels | Agent | Cost | When to Use |
|-------------|-------|------|-------------|
| `security`, `architecture`, `complex` | **Claude** | $20/mo | Expert-level reasoning required |
| `documentation`, `bulk-refactor`, `large-scale` | **Gemini** | **FREE** | Bulk work, 1000 free/day |
| `github-workflow`, `quick-fix`, `pr` | **Copilot** | FREE/$10 | GitHub-specific operations |
| *No specific label* | **Gemini** | **FREE** | Default cost-optimized choice |

**Cost Target:** 60-70% Gemini (free), 20-30% Copilot (free/$10), 10-20% Claude ($20) = **$20-30/month total**

---

## 🎓 Documentation

### Getting Started
- **Quick Start** - 5-minute setup guide ([EN](docs/QUICKSTART-EN.md) | [DE](docs/QUICKSTART-DE.md))

### Architecture & Strategy
- **Architecture Overview** - 3-layer system explained ([EN](docs/ARCHITECTURE-EN.md) | [DE](docs/ARCHITECTURE-DE.md))

### Reference
- **[MCP Servers](docs/MCP-SERVERS.md)** - All 18 servers explained
- **[Custom Agents](config/AGENTS.md)** - 4 specialized agents

---

## 💰 Cost Breakdown

### Monthly Costs (Real)

```
┌──────────────────────────────────────────────────────────────┐
│ Service         │ Usage    │ Free Tier      │ Cost          │
├──────────────────────────────────────────────────────────────┤
│ Gemini AI       │ 60-70%   │ 1000 req/day   │ $0 FREE!      │
│ Copilot CLI     │ 20-30%   │ 2000/month     │ $0-10/mo      │
│ Claude Code     │ 10-20%   │ None           │ $20/mo (Pro)  │
│ OpenHands       │ Optional │ $10 credit     │ $0-20/mo      │
│ Perplexity      │ Optional │ Limited        │ $0-20/mo      │
│ Rover           │ Unlimited│ Open source    │ $0 FREE!      │
│ MCP Servers     │ Unlimited│ All local      │ $0 FREE!      │
├──────────────────────────────────────────────────────────────┤
│ MINIMUM (Free tiers)                        │ $20/mo        │
│ OPTIMAL (Best value)                        │ $30/mo        │
│ POWER USER                                  │ $100-200/mo   │
└──────────────────────────────────────────────────────────────┘
```

### Real Cost Examples

**Minimum Setup** ($20/month)
- Claude Pro: $20 (required for Code)
- Gemini: FREE (1000/day limit)
- Copilot: FREE tier (2000/month)
- Total: **$20/month**

**Optimal Setup** ($30/month)
- Claude Pro: $20
- Gemini: FREE (maximized!)
- Copilot Pro: $10
- Total: **$30/month**

**Example Workflow Costs:**

```bash
# Feature Development (uses ~3 Claude requests)
rover task "Analyze impact" --agent gemini          # $0
rover task "Design architecture" --agent claude     # ~$0.50
rover task "Implement 30 components" --agent gemini # $0
rover task "Security review" --agent claude         # ~$0.50
rover task "Create PR" --agent copilot              # $0
# Total: ~$1 from your $20 Claude Pro subscription
```

**Documentation Sprint** ($0!)
```bash
rover task "Generate API docs (200 endpoints)" --agent gemini  # $0
rover task "Create integration guide" --agent gemini           # $0
rover task "Generate code examples" --agent gemini             # $0
# All parallel, all FREE!
```

**📊 Full Analysis:** See [Architecture](docs/ARCHITECTURE-EN.md) for cost strategy

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
- 💰 Cost-conscious development ($20-30/month with free tier optimization)

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
- **Daily Free Requests:** 1000 (Gemini)
- **Monthly Cost:** $20-30 (with strategic free tier usage)

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

### Core AI Systems
- **[Anthropic](https://www.anthropic.com/)** - Claude Code & API ([Documentation](https://docs.anthropic.com/))
- **[Google AI](https://ai.google.dev/)** - Gemini AI with 2M context ([Gemini Docs](https://ai.google.dev/gemini-api/docs))
- **[GitHub](https://github.com/)** - Copilot CLI ([Copilot Docs](https://docs.github.com/en/copilot))
- **[Endor Labs](https://www.endorlabs.com/)** - Rover multi-agent orchestration
  - **[Rover GitHub](https://github.com/endorhq/rover)** - Apache 2.0 license, npm package `@endorhq/rover`
  - **[Rover Docs](https://endor.dev/rover)** - Official documentation
- **[OpenHands](https://github.com/OpenHands/OpenHands)** - Autonomous AI software developer
  - **[All-Hands-AI](https://github.com/All-Hands-AI)** - Organization behind OpenHands (64k+ stars)
  - Formerly known as OpenDevin

### MCP Ecosystem
- **[Model Context Protocol](https://modelcontextprotocol.io/)** - MCP specification & foundation
- **[MCP Servers](https://github.com/modelcontextprotocol/servers)** - Official server implementations
  - `@modelcontextprotocol/server-filesystem` - File operations
  - `@modelcontextprotocol/server-memory` - Knowledge persistence
  - `@modelcontextprotocol/server-github` - GitHub integration
  - `@modelcontextprotocol/server-brave-search` - Web search
  - `@modelcontextprotocol/server-sequential-thinking` - Reflective reasoning
  - `@modelcontextprotocol/server-puppeteer` - Browser automation
  - `@modelcontextprotocol/server-sqlite` - SQLite database
  - `@modelcontextprotocol/server-postgres` - PostgreSQL integration
  - `@modelcontextprotocol/server-everything` - Testing framework
  - `@modelcontextprotocol/inspector` - Live debugging

### Community MCP Servers
- **[@executeautomation](https://github.com/executeautomation/playwright-mcp-server)** - Playwright MCP server
- **[@perplexity-ai](https://github.com/perplexity-ai/mcp-server)** - Perplexity AI search
- **[gemini-mcp-tool](https://www.npmjs.com/package/gemini-mcp-tool)** - Gemini CLI integration
- **[copilot-mcp-server](https://www.npmjs.com/package/copilot-mcp-server)** - Copilot CLI integration
- **[docs-mcp-server](https://www.npmjs.com/package/docs-mcp-server)** - Documentation search
- **[mcp-server-time](https://www.npmjs.com/package/mcp-server-time)** - Timezone handling
- **[postmancer](https://www.npmjs.com/package/postmancer)** - API testing tool

### Additional Tools & Infrastructure
- **[Brave Search API](https://brave.com/search/api/)** - Web search service
- **[Playwright](https://playwright.dev/)** - Browser automation framework by Microsoft
- **[Docker](https://www.docker.com/)** - Containerization platform for Rover isolation
- **[Node.js](https://nodejs.org/)** - JavaScript runtime for CLI tools
- **[Git](https://git-scm.com/)** - Version control system for worktrees

### Community & Open Source
Special thanks to all MCP server developers, npm package maintainers, and the open source community for making this ecosystem possible!

---

## 🔗 Links

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/LEEI1337/ai-dev-orchestrator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/LEEI1337/ai-dev-orchestrator/discussions)

---

## ⚡ Quick Links

| Document | Description |
|---|---|
| [Quick Start EN](docs/QUICKSTART-EN.md) / [DE](docs/QUICKSTART-DE.md) | Get started in 5 minutes |
| [Architecture EN](docs/ARCHITECTURE-EN.md) / [DE](docs/ARCHITECTURE-DE.md) | System design & AI roles |
| [MCP Servers](docs/MCP-SERVERS.md) | All 18 servers reference |
| [Custom Agents](config/AGENTS.md) | 4 specialized agents |
| [Documentation Index](docs/INDEX.md) | All docs organized |

---

<div align="center">

**Made with ❤️ by developers, for developers in Austria 🇦🇹**

[⭐ Star this repo](https://github.com/LEEI1337/ai-dev-orchestrator) if you find it useful!

</div>
