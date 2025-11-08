# 🚀 Einfache Anleitung: Neues Projekt erstellen

**Für:** Lazy Bird AI Development Orchestrator v2.0
**Ziel:** Von der Idee zum fertigen Projekt in 5 Minuten

---

## 📋 Schnellstart (TL;DR)

```
1. GitHub Issue erstellen mit Labels
2. Lazy Bird erkennt automatisch (max. 60s)
3. Projekt wird initialisiert
4. AI implementiert Feature
5. PR wird erstellt
6. Du reviewst & mergst
```

**Kosten:** $0 - $3 (abhängig vom Agent)

---

## 🎯 Schritt 1: Projekt-Idee planen

### Was brauchst du?

**Frage dich:**
- Was soll das Projekt tun? (1-2 Sätze)
- Welche Programmiersprache? (Python, TypeScript, React, etc.)
- Brauche ich hohe Sicherheit? (Ja → Claude)
- Ist es komplex? (Nein → Gemini FREE)
- GitHub-spezifisch? (Ja → Copilot)

### Beispiel-Ideen:

**E-Commerce Backend API (Python + FastAPI)**
```
Was: RESTful API für Online-Shop
Features: User Auth, Product Catalog, Shopping Cart, Orders
Sprache: Python (FastAPI)
Sicherheit: Mittel (JWT Auth)
Agent: Gemini (FREE - nicht security-critical)
```

**Crypto Trading Dashboard (React + TypeScript)**
```
Was: Real-time Trading Dashboard
Features: Price Charts, Portfolio Tracking, Trade Execution
Sprache: TypeScript + React
Sicherheit: HOCH (echtes Geld!)
Agent: Claude ($20 - security first!)
```

**GitHub Actions Workflow Generator (TypeScript)**
```
Was: Tool zum Generieren von GitHub Actions
Features: Template Selection, YAML Generation, Validation
Sprache: TypeScript
GitHub-Integration: Ja
Agent: Copilot (GitHub-Experte)
```

---

## 🏷️ Schritt 2: GitHub Issue erstellen

### Template

```markdown
Titel: [Kurze Beschreibung - max. 60 Zeichen]

Labels:
- lazy-bird (PFLICHT!)
- [python|typescript|react|nextjs] (Projekt-Typ)
- [feature|bugfix|refactor|docs] (Task-Typ)
- [security|architecture] (Optional - aktiviert Claude)

Body:
## Ziel
[Was soll gebaut werden - 2-3 Sätze]

## Features
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

## Technische Details
- Framework: [z.B. FastAPI, Next.js]
- Datenbank: [z.B. PostgreSQL, MongoDB, keine]
- Auth: [z.B. JWT, OAuth, keine]

## Acceptance Criteria
- [ ] Tests laufen durch (min. 60% Coverage)
- [ ] Dokumentation vorhanden (README.md)
- [ ] Code Review bestanden
```

### Label-Guide

**Projekt-Typ (wähle EINS):**
```
python       → Python-Projekt (FastAPI, Django, Flask)
typescript   → TypeScript-Projekt (Node.js, Express)
react        → React-App (Vite, CRA)
nextjs       → Next.js-App (SSR, SSG)
rust         → Rust-Projekt (Cargo)
go           → Go-Projekt
```

**Task-Typ (wähle EINS):**
```
feature      → Neues Feature
bugfix       → Bug beheben
refactor     → Code verbessern
docs         → Dokumentation
```

**Agent-Steuerung (optional):**
```
security     → Claude ($20 - hohe Sicherheit)
architecture → Claude ($20 - komplexe Architektur)
ci-cd        → Copilot (GitHub Actions Experte)
```

**Wichtig:** Ohne `security`/`architecture` Label wählt System automatisch **Gemini (FREE)**!

---

## 💰 Schritt 3: Agent-Auswahl verstehen

### Automatische Auswahl

**Gemini (FREE) - Standard:**
```
Kosten: $0
Wann: Kein security/architecture Label
Gut für:
  - Standard CRUD Apps
  - Dokumentation
  - Prototypen
  - Refactoring
Coverage: 60-70%
Doku: ⭐⭐⭐⭐⭐
```

**Claude ($20) - Premium:**
```
Kosten: ~$0.50 - $3 pro Task
Wann: security ODER architecture Label
Gut für:
  - Payment Systems
  - Crypto/Finance
  - Health/Medical
  - Complex Architecture
Coverage: 80-90%
Security: ⭐⭐⭐⭐⭐
```

**Copilot (Kostenlos mit GitHub Pro):**
```
Kosten: $0 (mit Pro Account)
Wann: ci-cd Label oder GitHub-Workflow Keyword
Gut für:
  - GitHub Actions
  - CI/CD Pipelines
  - Bulk Refactoring
Coverage: 60%
GitHub: ⭐⭐⭐⭐⭐
```

### Kosten optimieren

**Beispiel 1: Blog Website**
```
❌ SCHLECHT: Label "security" → Claude → $2
✅ GUT: Kein security Label → Gemini → $0
Grund: Blog braucht keine high-security (nur Basic Auth)
```

**Beispiel 2: Payment Gateway**
```
❌ SCHLECHT: Kein Label → Gemini → $0 → Unsicher!
✅ GUT: Label "security" → Claude → $2 → Sicher!
Grund: Echtes Geld = hohe Sicherheit PFLICHT!
```

---

## 🛠️ Schritt 4: Issue erstellen & warten

### Issue erstellen

1. Gehe zu GitHub Repository
2. **Issues** → **New Issue**
3. Fülle Template aus (siehe oben)
4. **Wichtig:** Label `lazy-bird` + Projekt-Typ!
5. **Submit new issue**

### Was passiert automatisch?

**Innerhalb von 60 Sekunden:**

```
[00:10] 🔍 Lazy Bird Issue Watcher erkennt Issue #42
[00:15] 📋 Analysiert Labels: lazy-bird, python, feature
[00:20] 🤖 Wählt Agent: gemini (kein security Label)
[00:25] 📦 Findet freien Slot: Projekt-A
[00:30] 📁 Erstellt Struktur:
        ✅ projects/Projekt-A/src/
        ✅ projects/Projekt-A/tests/
        ✅ projects/Projekt-A/docs/
        ✅ requirements.txt
        ✅ .gitignore
        ✅ README.md
[00:40] 🔧 Git Repository initialisiert
[00:45] ⚙️  projects.json updated
[00:50] 🚀 Rover Task gestartet mit Gemini
[00:60] ✅ Issue kommentiert: "Projekt initialisiert!"
```

### GitHub Issue Kommentar

Lazy Bird kommentiert automatisch:

```markdown
✅ **Projekt initialisiert!**

**Slot:** Projekt-A
**Typ:** python
**Agent:** gemini
**Struktur:**
- src/ (Source Code)
- tests/ (Tests)
- docs/ (Dokumentation)

**Rover Task:** #RT-042 gestartet
**Status:** 🔄 In Progress

---
🤖 Lazy Bird v2.0
```

---

## 🏗️ Schritt 5: AI implementiert

### Was passiert im Hintergrund?

**Rover orchestriert:**
1. Erstellt Git Worktree (isoliert vom main Branch)
2. Startet Docker Container mit Gemini
3. Gemini erhält Guidelines:
   - LAYER-0 (Universal Standards)
   - LAYER-1 (MCP Servers)
   - LAYER-2 (AI CLI)
   - LAYER-2-GEMINI (Gemini-spezifisch)
   - LAYER-3 (Rover Orchestration)
   - LAYER-4 (Lazy Bird Automation)

**Gemini implementiert:**
```python
# Beispiel: E-Commerce Backend

projects/Projekt-A/
├── src/
│   ├── main.py              # FastAPI App
│   ├── lib/
│   │   ├── auth.py          # JWT Authentication
│   │   ├── products.py      # Product CRUD
│   │   ├── cart.py          # Shopping Cart
│   │   └── orders.py        # Order Management
│   └── models/
│       ├── user.py
│       ├── product.py
│       └── order.py
├── tests/
│   ├── test_auth.py         # 65% Coverage ✅
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── docs/
│   ├── API.md               # API Documentation
│   └── SETUP.md             # Setup Guide
├── requirements.txt
├── .env.example
└── README.md
```

**Gemini folgt Guidelines:**
- ✅ src/ Struktur (LAYER-0)
- ✅ Nutzt MCP Filesystem Server (LAYER-1)
- ✅ Conventional Commits (LAYER-2)
- ✅ 60-70% Test Coverage (LAYER-2-GEMINI)
- ✅ Exzellente Dokumentation (LAYER-2-GEMINI)
- ✅ Git Worktree Isolation (LAYER-3)
- ✅ Issue Commenting (LAYER-4)

**Dauer:** 5-15 Minuten (abhängig von Komplexität)

---

## ✅ Schritt 6: Review & Merge

### Pull Request Review

**PR wird automatisch erstellt:**

```markdown
Titel: feat: Build E-Commerce Backend API (#42)

## Summary
Implemented RESTful API with FastAPI:
- JWT Authentication (auth.py)
- Product Catalog CRUD (products.py)
- Shopping Cart (cart.py)
- Order Management (orders.py)

## Changes
- Added src/ with main.py and lib/ modules
- Added comprehensive tests (65% coverage)
- Added API documentation
- Added setup guide

## Tests
✅ 12/12 tests passed
✅ Coverage: 65%

## Checklist
- [x] Tests pass
- [x] Coverage >= 60%
- [x] Documentation added
- [x] No secrets in code

Closes #42

---
🤖 Generated with Lazy Bird v2.0
Agent: Gemini FREE
Cost: $0
```

### Code Review Checkliste

```markdown
- [ ] Code ist verständlich
- [ ] Tests laufen durch (pytest)
- [ ] Keine Secrets (.env.example ✅, .env committed ❌)
- [ ] Dokumentation vollständig
- [ ] Security Basics beachtet (Input Validation)
- [ ] Naming Conventions eingehalten
```

### Merge PR

```bash
# Option 1: GitHub UI
→ Review PR
→ "Approve"
→ "Merge pull request"
→ Issue #42 wird automatisch geschlossen

# Option 2: CLI
gh pr review 43 --approve
gh pr merge 43
```

---

## 🎯 Vollständiges Beispiel

### Beispiel: To-Do List API

**1. Planung:**
```
Idee: Simple To-Do List REST API
Sprache: Python + FastAPI
Sicherheit: Niedrig (Basic Auth)
Agent: Gemini (FREE)
```

**2. GitHub Issue:**
```markdown
Titel: Build To-Do List REST API

Labels: lazy-bird, python, feature

## Ziel
Create REST API for managing to-do lists with user authentication.

## Features
- [ ] User registration & login (Basic Auth)
- [ ] CRUD operations for to-dos
- [ ] Filter by status (done/pending)
- [ ] SQLite database

## Technische Details
- Framework: FastAPI
- Datenbank: SQLite
- Auth: Basic Authentication

## Acceptance Criteria
- [ ] Tests >= 60% coverage
- [ ] API documentation (Swagger)
- [ ] README with setup instructions
```

**3. Warten (60s):**
```
[System initialisiert automatisch Projekt-A]
```

**4. AI implementiert (10 Min):**
```python
# Gemini erstellt:
src/main.py          # FastAPI app with auth
src/lib/todos.py     # CRUD operations
src/lib/users.py     # User management
tests/               # 68% coverage
docs/API.md          # Swagger docs
```

**5. Review & Merge (5 Min):**
```
✅ Tests: 18/18 passed
✅ Coverage: 68%
✅ Docs: Complete
→ Approve PR
→ Merge
```

**Gesamt-Zeit:** 15-20 Minuten
**Kosten:** $0 (Gemini FREE)
**Deine Arbeit:** 5 Minuten (Issue schreiben + Review)

---

## 🔧 Troubleshooting

### Issue wird nicht erkannt

**Problem:** Nach 2 Minuten kein Kommentar
**Lösung:**
```bash
# Prüfe Issue Watcher läuft
cd lazy-bird/scripts
python issue-watcher.py

# Prüfe Labels
→ Muss "lazy-bird" Label haben!
```

### Falscher Agent gewählt

**Problem:** Claude statt Gemini
**Lösung:**
```
Entferne Labels: security, architecture
→ System wählt automatisch Gemini
```

### Projekt-Slot voll

**Problem:** Alle Slots (A/B/C) besetzt
**Lösung:**
```bash
# Prüfe welche Slots belegt
ls -la projects/

# Altes Projekt löschen oder archivieren
mv projects/Projekt-A projects/archive/old-project-a
```

### Tests schlagen fehl

**Problem:** PR zeigt failing tests
**Lösung:**
```bash
# Lokal testen
cd projects/Projekt-A
pytest tests/ -v

# Falls AI Fehler gemacht hat:
→ Kommentiere im PR was fehlt
→ AI erstellt Fix-Commit
```

---

## 📊 Kosten-Rechner

### Beispiel-Projekte & Kosten

| Projekt | Agent | Kosten | Grund |
|---------|-------|--------|-------|
| Blog Website | Gemini | $0 | Kein Security-Risk |
| To-Do API | Gemini | $0 | Basic Auth reicht |
| E-Commerce API | Gemini | $0 | Kein Payment (nur Catalog) |
| Payment Gateway | Claude | $2 | Echtes Geld → Security! |
| Health Records | Claude | $3 | HIPAA/DSGVO → Security! |
| Crypto Wallet | Claude | $2 | Crypto → Security! |
| GitHub Action | Copilot | $0 | Mit Pro Account |
| CI/CD Pipeline | Copilot | $0 | Mit Pro Account |

### Regel:

```
Echtes Geld / Sensitive Daten / Compliance?
→ JA: Claude ($2-3)
→ NEIN: Gemini ($0)

GitHub-spezifisch?
→ JA: Copilot ($0 mit Pro)
→ NEIN: Gemini/Claude
```

---

## 🚀 Nächste Schritte

### Nach erfolgreichem Merge

**1. Projekt testen:**
```bash
cd projects/Projekt-A

# Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest tests/

# TypeScript
npm install
npm test
npm run build
```

**2. Deployment vorbereiten:**
```bash
# Docker (empfohlen)
docker build -t projekt-a .
docker run -p 8000:8000 projekt-a

# Oder manuell
python src/main.py
```

**3. Weitere Features:**
```
→ Erstelle neues Issue für nächstes Feature
→ Lazy Bird orchestriert wieder
→ Iteriere!
```

---

## 📚 Weitere Ressourcen

- **Technische Doku:** `lazy-bird/README.md`
- **Architektur:** `docs/LAZY-BIRD-ARCHITECTURE.md`
- **Setup Guide (DE):** `docs/LAZY-BIRD-SETUP-DE.md`
- **Setup Guide (EN):** `docs/LAZY-BIRD-SETUP-EN.md`
- **Updates v2.0:** `UPDATES-V2.md`
- **Layer System:** `lazy-bird/guidelines/LAYER-SYSTEM.md`

---

## ❓ FAQ

### Kann ich mehrere Projekte parallel erstellen?

**Ja!** Bis zu 3 gleichzeitig (Slot A/B/C).

```
Issue #1 → Projekt-A (In Progress)
Issue #2 → Projekt-B (In Progress)
Issue #3 → Projekt-C (In Progress)
Issue #4 → Wartet auf freien Slot
```

### Muss ich jedes Mal ein GitHub Issue erstellen?

**Für Lazy Bird Automation: JA**

Alternative (manuell):
```bash
cd lazy-bird/scripts
python project-initializer.py

# Dann Rover manuell starten
rover task "Implement feature X" --agent gemini
```

### Kann ich den Agent manuell wählen?

**Ja!** Über Labels:
```
security → Claude
architecture → Claude
ci-cd → Copilot
(kein Label) → Gemini
```

### Was wenn AI Fehler macht?

**Kein Problem!**
1. Kommentiere im PR was falsch ist
2. AI erstellt Fix-Commit
3. Oder: Editiere lokal und push

---

**Happy Coding! 🚀**

v2.0 - 2025-11-08
