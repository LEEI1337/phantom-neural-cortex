# 🚀 Quick Start Guide

**Get your AI development environment running in 5 minutes.**

---

## Prerequisites

- Node.js 18+
- Docker Desktop
- Git
- API Keys (GitHub token required, others optional)

---

## Installation

```bash
# 1. Clone
git clone https://github.com/LEEI1337/ai-dev-orchestrator.git
cd ai-dev-orchestrator

# 2. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 3. Install CLIs (choose what you need)
npm install -g @anthropic-ai/claude-code      # $20/month
npm install -g @google/generative-ai-cli      # FREE
npm install -g @github/copilot-cli            # FREE or $10/month
npm install -g @endorhq/rover                 # FREE

# 4. Initialize Rover
git init  # if needed
rover init .
```

---

## First Steps

### Test Gemini (FREE)
```bash
gemini "Hello, test if you're working"
```

### Test Rover Parallel Execution
```bash
rover task "List all markdown files" --agent gemini
rover ls
```

### Test Claude Agent
```bash
claude "@code-expert review README.md"
```

---

## Cost Optimization

**Minimum Setup:** $20/month
- Claude Pro: $20 (required)
- Gemini: FREE (1000/day)
- Copilot: FREE tier

**Optimal Setup:** $30/month
- Claude Pro: $20
- Gemini: FREE
- Copilot Pro: $10

**Strategy:** Maximize free tiers (Gemini + Copilot free)

---

## Verify Setup

```bash
# Check all tools
claude --version
gemini --version
copilot --version
rover --version

# Test MCP servers
ls .mcp.json
```

---

## Next Steps

1. **[Architecture](architecture/ARCHITECTURE.md)** - Understand the 3-layer system
2. **[AI Selector](guides/ROVER-AI-SELECTOR.md)** - Learn which AI for which task
3. **[Cost Guide](OPTIMIZATION-SUMMARY.md)** - Optimize your monthly costs

---

## Common Issues

**"Rover not found"**
```bash
npm install -g @endorhq/rover
```

**"Git not initialized"**
```bash
git init
git config user.email "you@example.com"
git config user.name "Your Name"
```

**"MCP servers not loading"**
- Check `.mcp.json` exists
- Verify API keys in `.env`
- Restart Claude Code

---

**Need help?** Open an [issue](https://github.com/LEEI1337/ai-dev-orchestrator/issues)
