# OpenHands Repository Configuration

This directory contains custom configuration for OpenHands AI agent.

## Structure

```
.openhands/
├── setup.sh              # Runs on every OpenHands session start
├── pre-commit.sh         # Runs before every commit (quality checks)
├── microagents/          # Project-specific instructions
│   ├── code-quality.md   # Code standards & best practices
│   └── ai-collaboration.md  # Multi-AI workflow guidelines
└── README.md             # This file
```

## Files

### setup.sh
**Purpose:** Initialize repository environment for OpenHands

**Runs:**
- Environment variable setup
- Dependency installation (npm, pip)
- Tool verification (node, git, etc.)
- MCP server validation
- Playwright browser setup
- Memory bank initialization

**Triggers:** Every time OpenHands starts working with this repo

### pre-commit.sh
**Purpose:** Ensure code quality before commits

**Checks:**
- ✅ ESLint (JavaScript/TypeScript linting)
- ✅ TypeScript type checking
- ✅ Prettier (code formatting)
- ✅ Unit tests
- ✅ Security audit (npm audit)
- ✅ JSON validation
- ✅ Merge conflict detection
- ⚠️ console.log detection (warning only)
- ⚠️ Large file detection (warning only)

**Exit Codes:**
- `0` - All checks passed, commit allowed
- `1` - Checks failed, commit blocked

**Bypass:** `git commit --no-verify` (not recommended)

### microagents/code-quality.md
**Purpose:** Define code quality standards

**Contents:**
- Language-specific standards (TypeScript, Python)
- File organization & naming conventions
- Security requirements
- Testing requirements & coverage targets
- Performance guidelines
- Error handling patterns
- Documentation standards
- Git commit message format
- Code review checklist
- Accessibility standards

**Usage:** OpenHands automatically follows these when generating code

### microagents/ai-collaboration.md
**Purpose:** Multi-AI workflow coordination

**Contents:**
- When to defer to Claude Code, Copilot, Gemini
- OpenHands specialization areas
- Collaboration patterns
- Communication protocols for PRs
- MCP server awareness
- Custom agent awareness
- Quality standards
- Error handling guidelines

**Usage:** Guides OpenHands on when to work autonomously vs. recommend other AIs

## How It Works

### 1. Session Start
```bash
# User runs OpenHands
openhands

# OpenHands automatically executes:
.openhands/setup.sh

# Result: Environment ready, dependencies installed
```

### 2. During Development
```
OpenHands reads microagents:
- code-quality.md → Applies code standards
- ai-collaboration.md → Knows when to defer to other AIs
```

### 3. Before Commit
```bash
# OpenHands attempts to commit
git commit -m "feat: add new feature"

# Automatically triggers:
.openhands/pre-commit.sh

# If checks pass: Commit succeeds
# If checks fail: Commit blocked, issues reported
```

## Configuration

### Enable/Disable Checks

**Edit pre-commit.sh:**
```bash
# Disable specific check by commenting out:
# if npm run lint; then
#     echo "✅ Lint check passed"
# fi
```

### Customize Standards

**Edit microagents/code-quality.md:**
```markdown
# Change coverage targets
**Coverage Targets**
- Critical paths: 80% coverage  # Changed from 100%
```

### Add New Microagent

**Create new file:**
```bash
touch .openhands/microagents/custom-workflow.md
```

**Content:**
```markdown
# Custom Workflow Microagent

Define specific workflows or patterns here.
OpenHands will read and apply these automatically.
```

## Integration with Other AIs

### Claude Code
- Setup scripts ensure Claude's MCP servers are available
- Microagents reference Claude's custom agents (@code-expert, etc.)

### Copilot CLI
- Pre-commit checks align with Copilot's code style
- Microagents reference Copilot agents

### Gemini
- Large-scale analysis patterns defined in ai-collaboration.md
- When to use Gemini's 2M token context window

## Troubleshooting

### Setup script fails
```bash
# Run manually to see errors
bash .openhands/setup.sh
```

### Pre-commit blocks commits
```bash
# See what failed
bash .openhands/pre-commit.sh

# Fix issues, then commit again

# Emergency bypass (not recommended):
git commit --no-verify
```

### OpenHands ignores microagents
- Ensure files are in `.openhands/microagents/`
- Use `.md` extension
- Check file permissions (should be readable)

## Best Practices

### 1. Keep Scripts Fast
- Setup should complete in <30 seconds
- Pre-commit should complete in <60 seconds
- Skip heavy operations (e.g., full E2E tests)

### 2. Fail Fast
- Exit on first critical error
- Use `set -e` in scripts
- Clear error messages

### 3. Be Informative
- Echo progress messages
- Use emojis for clarity (✅ ❌ ⚠️)
- Log to console for visibility

### 4. Version Control
- Commit all `.openhands/` files
- Share configurations with team
- Document changes in PRs

### 5. Security
- Never hardcode secrets in scripts
- Use environment variables
- Don't log sensitive data

## Examples

### Example: Add Python linting
**Edit pre-commit.sh:**
```bash
# Add after existing checks
if [ -f "requirements.txt" ]; then
    echo "Running Python linting..."
    if python -m flake8 .; then
        echo "✅ Python lint passed"
    else
        echo "❌ Python lint failed"
        CHECKS_FAILED=1
    fi
fi
```

### Example: Custom setup for Docker
**Edit setup.sh:**
```bash
# Add Docker check
if command -v docker &> /dev/null; then
    echo "✅ Docker $(docker --version)"

    # Start required containers
    docker-compose up -d
else
    echo "⚠️  Docker not found"
fi
```

### Example: Project-specific microagent
**Create `.openhands/microagents/api-design.md`:**
```markdown
# API Design Standards

## REST Conventions
- Use plural nouns for resources
- HTTP methods: GET, POST, PUT, DELETE
- Status codes: 200, 201, 404, 500

## Response Format
All APIs must return:
{
  "success": boolean,
  "data": any,
  "error": string | null
}
```

---

**This configuration makes OpenHands a true team player, working seamlessly with your existing tools and AI assistants!**
