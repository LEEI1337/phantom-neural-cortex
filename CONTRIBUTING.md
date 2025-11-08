# Contributing to AI Development Orchestrator

Thank you for your interest in contributing! This project aims to provide a professional, cost-optimized multi-AI development environment.

## 🎯 Ways to Contribute

- 🐛 **Report Bugs** - Open an issue with reproduction steps
- 💡 **Suggest Features** - Share ideas for improvements
- 📝 **Improve Documentation** - Fix typos, add examples, clarify concepts
- 🔧 **Add MCP Servers** - Integrate new capabilities
- 🎨 **Share Workflows** - Document your optimization strategies
- 💰 **Cost Optimizations** - Share how you reduced costs further

## 🚀 Quick Start for Contributors

### 1. Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/LEEI1337/ai-dev-orchestrator.git
cd ai-dev-orchestrator
```

### 2. Set Up Development Environment

```bash
# Copy example environment
cp .env.example .env

# Edit .env with your API keys (never commit this!)
# Install dependencies (if any)
npm install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## 📋 Contribution Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

### Pull Request Process

1. **Update Documentation** - If you change functionality, update relevant docs
2. **Test Your Changes** - Ensure everything works as expected
3. **Keep PRs Focused** - One feature/fix per PR
4. **Write Clear Commit Messages** - Explain what and why

### Commit Message Format

```
type(scope): brief description

Detailed explanation if needed

Examples:
- feat(rover): add auto-agent-selection logic
- fix(mcp): correct GitHub server configuration
- docs(readme): update installation instructions
- chore(deps): update MCP server versions
```

### Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `chore` - Maintenance tasks
- `refactor` - Code restructuring
- `test` - Testing improvements

## 🔒 Security Guidelines

### NEVER Commit:

- ❌ API keys or tokens
- ❌ `.env` files
- ❌ OAuth credentials
- ❌ Personal data

### Before Committing:

```bash
# Always check what you're committing
git status
git diff

# Verify .env is ignored
git check-ignore .env
```

### If You Accidentally Commit Secrets:

1. **DO NOT** just delete the file in a new commit
2. **DO** rewrite history or use tools like [git-filter-repo](https://github.com/newren/git-filter-repo)
3. **DO** rotate/revoke the exposed credentials immediately
4. **DO** contact maintainers for help

## 📝 Documentation Standards

### README Updates

- Keep the main README concise and high-level
- Detailed docs go in `docs/` folder
- Use clear headings and structure
- Include code examples where helpful

### Code Comments

- Comment "why", not "what"
- Explain complex logic
- Document edge cases
- Keep comments up-to-date

## 🧪 Testing

Currently manual testing is used. When adding new features:

1. Test with all 3 AI systems (Claude, Gemini, Copilot)
2. Verify cost optimization works
3. Check that documentation matches behavior
4. Test edge cases

Future: Automated testing framework welcome!

## 🎨 Style Guide

### File Naming

- Documentation: `UPPERCASE.md` or `kebab-case.md`
- Code: `kebab-case.js/ts`
- Config: `lowercase.json` or `.lowercase`

### Directory Structure

```
.
├── docs/                   # All documentation
│   ├── guides/            # How-to guides
│   ├── setup/             # Setup instructions
│   └── architecture/      # Design docs
├── config/                # Configuration files
├── examples/              # Example workflows
├── templates/             # Templates for users
└── .github/               # GitHub-specific files
```

## 💰 Cost Optimization Contributions

When sharing cost optimization strategies:

1. **Document Real Numbers** - Share actual monthly costs
2. **Explain Strategy** - How did you optimize?
3. **Task Distribution** - What % each AI handles
4. **Use Cases** - What scenarios work best

Example:

```markdown
## My Optimization: Documentation-Heavy Projects

**Usage:**
- Gemini: 80% (all docs) = $0
- Copilot: 15% (GitHub) = $0
- Claude: 5% (reviews) = ~$5/month

**Result:** $5/month for 1000+ tasks
```

## 🛠️ Adding New MCP Servers

To add a new MCP server:

1. **Test It First** - Verify it works with Claude/Gemini/Copilot
2. **Document Purpose** - What does it enable?
3. **Cost Analysis** - Free tier? Paid? How much?
4. **Update Configs** - Add to appropriate .mcp.json files
5. **Document Usage** - Add examples to docs/

Template for MCP server PR:

```markdown
## MCP Server: [Name]

**Purpose:** Brief description

**Use Cases:**
- Use case 1
- Use case 2

**Cost:** $X/month or free tier details

**Configuration:**
```json
{
  "server-name": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "package-name"]
  }
}
```

**Recommended For:**
- [ ] Claude (if yes, why?)
- [ ] Gemini (if yes, why?)
- [ ] Copilot (if yes, why?)
```

## 🐛 Bug Reports

### Good Bug Report Includes:

1. **Clear Title** - Summarize the issue
2. **Description** - What happened vs. what should happen
3. **Steps to Reproduce** - How to trigger the bug
4. **Environment** - OS, Node version, AI CLIs used
5. **Logs/Screenshots** - If applicable
6. **Workaround** - If you found one

### Template:

```markdown
## Bug: [Brief Description]

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Steps to Reproduce:**
1. Step one
2. Step two
3. Bug appears

**Environment:**
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- Node: v20.10.0
- Claude Code: v1.0.0
- Rover: v1.4.1

**Logs:**
```
Paste relevant logs
```

**Additional Context:**
Any other helpful information
```

## 💡 Feature Requests

### Good Feature Request Includes:

1. **Use Case** - What problem does this solve?
2. **Proposed Solution** - How would it work?
3. **Alternatives** - Other options considered
4. **Priority** - How important is this?

### Template:

```markdown
## Feature: [Brief Description]

**Problem:**
Describe the problem or limitation

**Proposed Solution:**
How would this feature work?

**Use Case:**
Real-world example of when this is needed

**Alternatives Considered:**
Other ways to solve this

**Priority:** Low / Medium / High

**Implementation Ideas:**
Any thoughts on how to implement this
```

## 🎓 Questions?

- **General Questions** - Use [GitHub Discussions](https://github.com/LEEI1337/ai-dev-orchestrator/discussions)
- **Bug Reports** - Open an [Issue](https://github.com/LEEI1337/ai-dev-orchestrator/issues)
- **Quick Help** - Check existing documentation first

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AI Development Orchestrator! 🚀**
