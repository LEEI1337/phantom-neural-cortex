---
name: 🤖 Lazy Bird Automated Task
about: Create a task for automated implementation via Lazy Bird + Rover
title: '[AUTO] '
labels: ['lazy-bird', 'automation']
assignees: ''
---

## 🎯 Task Description

<!-- Provide a clear, detailed description of what needs to be implemented -->

## 📋 Requirements

<!-- List specific requirements and acceptance criteria -->

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## 🤖 AI Agent Selection

<!-- Add one of these labels to influence which AI agent processes this task -->

- `security` or `architecture` or `complex` → **Claude** (Expert, $20/mo)
- `documentation` or `bulk-refactor` or `large-scale` → **Gemini** (Free, 1000/day)
- `github-workflow` or `quick-fix` or `pr` → **Copilot** (Free/$10)
- No specific label → **Gemini** (Default free tier)

## 🧪 Test Requirements

<!-- Specify how this should be tested -->

```bash
# Example test commands
pytest tests/test_feature.py -v
npm test
```

## 📚 Additional Context

<!-- Add any other context, screenshots, or examples -->

---

## 🔧 How This Works

Once this issue is labeled with `lazy-bird`, the automation will:

1. ✅ **Lazy Bird Issue Watcher** detects this issue
2. ✅ **Agent Selector** chooses optimal AI (Claude/Gemini/Copilot)
3. ✅ **Rover** creates isolated worktree + Docker container
4. ✅ **AI Agent** implements the task
5. ✅ **Test Coordinator** validates with tests
6. ✅ **PR Created** automatically when tests pass
7. ✅ You review and merge!

**Cost:** Most tasks run FREE (Gemini/Copilot) 🎉

**Architecture:**
```
Layer 4: LAZY BIRD (this automation) → Watches & orchestrates
Layer 3: ROVER → Isolated execution environment
Layer 2: AI AGENTS → Claude/Gemini/Copilot
Layer 1: MCP SERVERS → 18 tool servers
```

---

## ⚙️ Configuration

The following project settings will be used:

- **Project:** ai-orchestrator
- **Test Command:** `pytest tests/ -v`
- **Default Agent:** gemini (FREE tier)
- **Max Retries:** 3
- **Timeout:** 30 minutes

---

**Note:** This issue will be processed automatically. You'll receive updates via comments as the automation progresses.
