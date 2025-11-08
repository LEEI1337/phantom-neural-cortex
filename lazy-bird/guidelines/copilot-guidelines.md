# 🤖 Copilot-Spezifische Guidelines

**Agent:** GitHub Copilot
**Use Case:** GitHub Workflows, Quick Fixes, PR Operations
**Kosten:** Free Tier (2000 completions/mo) oder $10/mo (unlimited)
**Stärken:** GitHub Integration, CI/CD, Workflow Automation

---

## 🎯 Wann Copilot verwendet wird

Copilot ist spezialisiert auf GitHub-bezogene Tasks:
- `github-workflow` - GitHub Actions & Workflows
- `ci-cd` - CI/CD Pipeline Setup
- `quick-fix` - Schnelle Bugfixes
- `pr` - Pull Request Operations
- `automation` - GitHub Automation

**Fokus:** GitHub Ecosystem!

---

## 📋 Copilot-Spezifische Anforderungen

### 1. GitHub Actions First

Copilot's Kernkompetenz: PERFEKTE GitHub Actions!

```yaml
# ✅ RICHTIG: Complete, Production-Ready Workflow
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.11'

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest tests/ \
            --cov=src \
            --cov-report=xml \
            --cov-report=html \
            --cov-fail-under=70

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella

  lint:
    name: Lint Code
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Run Ruff
        run: |
          pip install ruff
          ruff check .

      - name: Run Black
        run: |
          pip install black
          black --check .

  build:
    name: Build Package
    runs-on: ubuntu-latest
    needs: [test, lint]

    steps:
      - uses: actions/checkout@v4

      - name: Build distribution
        run: |
          python -m pip install build
          python -m build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Deploy to PyPI
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: |
          pip install twine
          twine upload dist/* -u __token__ -p $PYPI_TOKEN
```

### 2. Matrix Testing

```yaml
# ✅ RICHTIG: Test multiple versions
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
        exclude:
          # Exclude specific combinations if needed
          - os: macos-latest
            python-version: '3.9'

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run tests
        run: pytest tests/
```

### 3. Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
      coverage-threshold:
        required: false
        type: number
        default: 70

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}

      - name: Run tests
        run: |
          pytest tests/ \
            --cov=src \
            --cov-fail-under=${{ inputs.coverage-threshold }}
```

```yaml
# .github/workflows/ci.yml - Using reusable workflow
name: CI
on: [push, pull_request]

jobs:
  test-python-39:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: '3.9'
      coverage-threshold: 70

  test-python-312:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: '3.12'
      coverage-threshold: 80
```

---

## 📁 Copilot Projekt-Struktur Erweiterungen

```
projekt/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # Main CI Pipeline
│   │   ├── cd.yml              # Deployment Pipeline
│   │   ├── tests.yml           # Test Matrix
│   │   ├── lint.yml            # Linting
│   │   ├── security.yml        # Security Scans
│   │   ├── dependabot.yml      # Dependency Updates
│   │   └── release.yml         # Release Automation
│   │
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── config.yml
│   │
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS              # Auto-assign reviewers
│   └── dependabot.yml          # Dependabot config
│
├── scripts/
│   ├── ci/
│   │   ├── setup.sh            # CI setup script
│   │   ├── test.sh             # Test runner
│   │   └── deploy.sh           # Deployment script
│   └── github/
│       └── release.sh          # Release helper
│
└── .gitattributes              # Git attributes
```

---

## 🔧 Quick Fix Best Practices

Copilot ist perfekt für schnelle Fixes:

```python
# ✅ RICHTIG: Quick, targeted fix
def calculate_total(items: List[Item]) -> float:
    """Calculate total price of items."""
    # BUG FIX: Handle empty list
    if not items:
        return 0.0

    # BUG FIX: Filter out None prices
    valid_items = [item for item in items if item.price is not None]

    return sum(item.price for item in valid_items)
```

**Copilot Quick Fix Prozess:**
1. Identifiziere Bug
2. Minimale Änderung
3. Add Test
4. Create PR
5. Done!

---

## 🚀 CI/CD Patterns

### Continuous Integration

```yaml
# ✅ RICHTIG: Fast CI Pipeline
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  # Fast checks first (fail fast)
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint

  # Then tests
  test:
    runs-on: ubuntu-latest
    needs: lint  # Only if lint passes
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  # Then build (slowest)
  build:
    runs-on: ubuntu-latest
    needs: test  # Only if tests pass
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
```

### Continuous Deployment

```yaml
# ✅ RICHTIG: Safe Deployment
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com

    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          # Deployment logic
          ./scripts/deploy.sh production

      - name: Verify deployment
        run: |
          # Health check
          curl -f https://myapp.com/health || exit 1

      - name: Notify on success
        if: success()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployment to production successful! 🎉'

      - name: Rollback on failure
        if: failure()
        run: |
          ./scripts/rollback.sh
```

---

## 🔐 GitHub Secrets Management

```yaml
# ✅ RICHTIG: Secure secrets usage
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy with secrets
        env:
          # Never log secrets!
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          # Use secrets securely
          ./deploy.sh
          # Secrets are masked in logs automatically
```

**Secret Best Practices:**
- ✅ Use GitHub Secrets (never hardcode)
- ✅ Use Environment protection rules
- ✅ Rotate secrets regularly
- ✅ Minimal secret scope
- ❌ Never echo secrets
- ❌ Never commit secrets

---

## 📦 Dependency Management

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    reviewers:
      - "team-leads"
    labels:
      - "dependencies"
      - "python"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    labels:
      - "dependencies"
      - "github-actions"
```

---

## 🎯 PR Automation

### Auto-merge for Dependabot

```yaml
# .github/workflows/auto-merge-dependabot.yml
name: Auto-merge Dependabot PRs

on: pull_request

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'

    steps:
      - name: Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v1

      - name: Auto-merge minor updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-patch' || steps.metadata.outputs.update-type == 'version-update:semver-minor'
        run: |
          gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### PR Labeler

```yaml
# .github/workflows/labeler.yml
name: Label PRs

on: pull_request

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

```yaml
# .github/labeler.yml
'documentation':
  - '**/*.md'
  - 'docs/**/*'

'tests':
  - 'tests/**/*'
  - '**/*.test.ts'

'ci':
  - '.github/workflows/*'
```

---

## 🎯 Copilot Checkliste

- [ ] GitHub Actions workflows komplett & funktionsfähig
- [ ] Matrix testing für multiple Versionen
- [ ] Secrets sicher verwendet
- [ ] Dependabot konfiguriert
- [ ] PR templates vorhanden
- [ ] Issue templates vorhanden
- [ ] CODEOWNERS definiert
- [ ] Fast CI (fail fast principle)
- [ ] CD with rollback capability
- [ ] Notification setup (Slack/Email)

---

## 💰 Cost Efficiency

**Free Tier (2000 completions/mo):**
- Perfekt für Quick Fixes
- Workflow Updates
- PR Reviews

**Pro ($10/mo):**
- Unlimited für High-Frequency Tasks
- Lohnt sich bei > 5 Workflows/week

---

## 📚 Resource Links

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)

---

**Copilot = GitHub Mastery!** 🐙
