# OpenHands Setup - E2E Testing & CI/CD Integration

**Version:** Latest (formerly OpenDevin)
**Best Model:** Claude Sonnet 4.5
**Free Credits:** $10 for new users

---

## Was ist OpenHands?

OpenHands ist eine **AI-powered Software Development Platform**, die:
- 🤖 Autonome Code-Änderungen durchführt
- 🧪 E2E Tests automatisch schreibt & ausführt
- 🔄 CI/CD Workflows automatisiert
- 🌐 Web browsing & API calls macht
- 📝 Issues automatisch bearbeitet

**Perfekt für:**
- E2E Test-Automatisierung
- CI/CD Pipeline-Integration
- Autonome Bug-Fixes
- Feature-Implementierung
- Code-Reviews & Refactoring

---

## Installation

### Methode 1: CLI (Empfohlen)

```bash
# 1. Install uv package manager
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Install OpenHands
uvx --python 3.12 openhands serve

# 3. Öffne Browser
# http://localhost:3000
```

### Methode 2: Docker

```bash
# Pull Image
docker pull ghcr.io/openhands/openhands:main

# Run
docker run -it --rm \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e WORKSPACE_MOUNT_PATH=$WORKSPACE_BASE \
  -v $WORKSPACE_BASE:/opt/workspace_base \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  --name openhands-app \
  ghcr.io/openhands/openhands:main
```

---

## Claude Integration (Free Account)

### Option 1: Claude Code API Key
```bash
# Set API Key
export ANTHROPIC_API_KEY="sk-ant-..."

# Start OpenHands
uvx openhands serve
```

### Option 2: OpenHands Cloud ($10 Free Credits)
1. Gehe zu [OpenHands Cloud](https://app.all-hands.dev)
2. Sign up (kostenlos)
3. $10 Credits werden automatisch hinzugefügt
4. Select: "Claude Sonnet 4.5"

**Free Tier:**
- $10 free credits
- ~200-400 tasks (abhängig von Komplexität)
- Claude Sonnet 4.5 empfohlen

---

## Repository-Spezifische Konfiguration

### .openhands/ Directory

OpenHands nutzt das `.openhands/` Verzeichnis für projekt-spezifische Konfiguration:

```
.openhands/
├── setup.sh              # Auto-runs beim Session-Start
├── pre-commit.sh         # Auto-runs vor jedem Commit
├── microagents/          # Project-specific instructions
│   ├── code-quality.md   # Code standards
│   └── ai-collaboration.md  # Multi-AI workflows
└── README.md             # Dokumentation
```

#### setup.sh
**Runs automatically** wenn OpenHands startet:
- ✅ Environment Variables laden
- ✅ npm/pip Dependencies installieren
- ✅ MCP Server validieren
- ✅ Playwright Browsers installieren
- ✅ Memory Bank initialisieren

#### pre-commit.sh
**Runs automatically** vor jedem Commit:
- ✅ ESLint (Code linting)
- ✅ TypeScript type check
- ✅ Prettier (formatting)
- ✅ Unit tests
- ✅ Security audit
- ✅ JSON validation
- ⚠️ console.log warnings
- ⚠️ Large file detection

**Blocks commit** wenn kritische Checks feilen!

#### microagents/
**OpenHands liest diese automatisch:**
- `code-quality.md` - Code standards, testing requirements
- `ai-collaboration.md` - Wann Claude/Copilot/Gemini nutzen

### Beispiel Setup:
```bash
# OpenHands startet
openhands

# Automatisch:
# 1. .openhands/setup.sh runs → Environment ready
# 2. Microagents geladen → Standards bekannt
# 3. Ready to work!
```

---

## Konfiguration

### 1. LLM Config (Claude Sonnet 4.5)

**In OpenHands Web UI:**
```
Settings → LLM Provider
- Provider: Anthropic
- Model: claude-sonnet-4-5-20250929
- API Key: sk-ant-...
```

**Via Config File (`~/.openhands/config.toml`):**
```toml
[llm]
model = "anthropic/claude-sonnet-4-5-20250929"
api_key = "${ANTHROPIC_API_KEY}"
temperature = 0.7
max_tokens = 4096
```

### 2. Workspace Setup

```toml
[workspace]
base_path = "C:\\Users\\Thomas\\Desktop\\claude config"
auto_mount = true
```

### 3. CI/CD Integration

**GitHub Actions (`.github/workflows/openhands.yml`):**
```yaml
name: OpenHands Auto-Fix

on:
  issues:
    types: [labeled]

jobs:
  openhands:
    if: contains(github.event.issue.labels.*.name, 'openhands')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run OpenHands
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          uvx --python 3.12 openhands \
            --task "${{ github.event.issue.body }}" \
            --model anthropic/claude-sonnet-4-5-20250929

      - name: Create PR
        uses: peter-evans/create-pull-request@v6
        with:
          title: "OpenHands: ${{ github.event.issue.title }}"
          body: "Automated fix by OpenHands AI"
          branch: openhands/${{ github.event.issue.number }}
```

---

## E2E Testing Setup

### 1. Playwright Integration

**OpenHands kann automatisch Playwright Tests erstellen:**

```bash
# In OpenHands CLI/Web
"Create E2E tests for the login flow using Playwright"
```

**Generiert:**
```typescript
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test('user can login successfully', async ({ page }) => {
  await page.goto('http://localhost:3000/login');

  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('http://localhost:3000/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

### 2. CI/CD Test Automation

**`.github/workflows/e2e-tests.yml`:**
```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Use Cases

### 1. Autonome Bug-Fixes

**GitHub Issue:**
```
Title: Login button not working on mobile
Labels: bug, openhands

Description:
When clicking login on mobile Safari, nothing happens.
Expected: User should be redirected to dashboard.
```

**OpenHands Action:**
1. Analysiert Code
2. Findet Bug (event handler fehlt)
3. Schreibt Fix
4. Erstellt Tests
5. Öffnet PR

### 2. E2E Test Generierung

**Prompt:**
```
"Create comprehensive E2E tests for the checkout flow:
1. Add items to cart
2. Proceed to checkout
3. Fill payment details
4. Complete order
5. Verify order confirmation"
```

**OpenHands:**
- Generiert Playwright Tests
- Erstellt Page Objects
- Schreibt Assertions
- Committet zu Repo

### 3. CI/CD Pipeline Setup

**Prompt:**
```
"Set up complete CI/CD pipeline with:
- Linting (ESLint)
- Unit tests (Jest)
- E2E tests (Playwright)
- Build
- Deploy to Vercel"
```

**OpenHands:**
- Erstellt `.github/workflows/ci.yml`
- Konfiguriert alle Tools
- Testet Pipeline
- Dokumentiert

---

## Integration mit Claude Code & Copilot

### Workflow-Strategie

**1. OpenHands für:**
- ✅ Autonome Feature-Implementierung
- ✅ E2E Test-Generierung
- ✅ CI/CD Setup
- ✅ Bug-Fixing (mit GitHub Issues)

**2. Claude Code für:**
- ✅ Komplexe Architektur-Entscheidungen
- ✅ Code-Reviews
- ✅ Debugging & Root Cause Analysis

**3. Copilot CLI für:**
- ✅ Quick Edits
- ✅ GitHub Operations
- ✅ Incrementelle Änderungen

**4. Gemini für:**
- ✅ Large-Scale Refactoring
- ✅ Codebase-wide Analysis

### Beispiel-Workflow

```bash
# 1. OpenHands: Feature implementieren
openhands "Implement user authentication with OAuth"

# 2. Gemini: Code analysieren
gemini "@gemini-specialist analyze authentication implementation"

# 3. Claude: Security Review
claude "@code-expert review authentication for security issues"

# 4. OpenHands: E2E Tests
openhands "Create E2E tests for authentication flow"

# 5. Copilot: Quick fixes
copilot /agent code-expert
> Fix the issues found in review
```

---

## Kosten-Übersicht

| Service | Free Tier | Paid |
|---------|-----------|------|
| **OpenHands Cloud** | $10 credits | $20/month |
| **Claude API** | Free (rate limited) | Pay-as-you-go |
| **Anthropic Credits** | - | ~$0.003/1K tokens |

**Geschätzte Kosten mit $10 Free Credits:**
- Simple Bug Fix: ~$0.05
- Feature Implementation: ~$0.20-0.50
- E2E Test Suite: ~$0.10-0.30
- CI/CD Setup: ~$0.15

**Total Tasks mit $10:** ~20-200 Tasks (je nach Komplexität)

---

## Best Practices

### 1. Task-Beschreibungen
**Gut:**
```
"Create a user registration form with:
- Email validation
- Password strength checker
- Confirmation email flow
- E2E tests with Playwright"
```

**Schlecht:**
```
"Make registration better"
```

### 2. Incremental Tasks
- Breche große Features in kleinere Tasks
- Ein Task = eine klare Aufgabe
- Verwende GitHub Issues für Tracking

### 3. Review AI-Generated Code
- **Immer** AI-Code reviewen
- Security-kritischen Code manuell prüfen
- Tests vor Merge ausführen

### 4. Version Control
- Committe AI-Changes in separatem Branch
- Nutze PRs für Reviews
- Tag AI-generated commits

---

## Troubleshooting

### OpenHands startet nicht
```bash
# Prüfe Python Version
python --version  # Muss 3.12 sein

# Reinstall
uvx --python 3.12 openhands --reinstall
```

### Claude API Fehler
```bash
# Prüfe API Key
echo $ANTHROPIC_API_KEY

# Test API
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Docker Issues
```bash
# Prüfe Docker
docker ps

# Restart
docker restart openhands-app
```

---

## Weitere Ressourcen

- [OpenHands Docs](https://docs.all-hands.dev)
- [GitHub Repository](https://github.com/OpenHands/OpenHands)
- [Discord Community](https://discord.gg/openhands)
- [Claude API Docs](https://docs.anthropic.com)

---

## Setup-Checklist

- [ ] uv package manager installiert
- [ ] OpenHands installiert
- [ ] Claude API Key konfiguriert
- [ ] Workspace Pfad gesetzt
- [ ] GitHub Actions Template erstellt
- [ ] E2E Tests Framework ready
- [ ] CI/CD Pipeline konfiguriert
- [ ] Free Credits activated

**Alles ready für autonome AI Development! 🚀**

---

**Last Updated:** 2025-11-08
**Recommended Model:** Claude Sonnet 4.5
**Free Tier:** $10 Credits
