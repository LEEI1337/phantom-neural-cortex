# 📁 Projekte - Lazy Bird AI Orchestrator

Dieser Ordner enthält dedizierte Projektverzeichnisse für die automatisierte Entwicklung mit dem Lazy Bird Framework.

## 📋 Übersicht

| Projekt | Status | Typ | Rover | Beschreibung |
|---------|--------|-----|-------|--------------|
| **Projekt-A** | 🆕 Bereit | TBD | ✅ | Bereit für automatisierte Entwicklung |
| **Projekt-B** | 🆕 Bereit | TBD | ✅ | Bereit für automatisierte Entwicklung |
| **Projekt-C** | 🆕 Bereit | TBD | ✅ | Bereit für automatisierte Entwicklung |

## 🚀 Quick Start für neues Projekt

### 1. Projekt-Typ definieren

Bearbeite `/lazy-bird/configs/projects.json` und setze den `type` für dein Projekt:

**Verfügbare Typen:**
- `python` - Python-Projekt
- `typescript` - TypeScript/Node.js Projekt
- `javascript` - JavaScript-Projekt
- `react` - React-Anwendung
- `nextjs` - Next.js Anwendung
- `documentation` - Reine Dokumentation

### 2. Build/Test Commands konfigurieren

```json
{
  "id": "projekt-a",
  "type": "python",
  "settings": {
    "test_command": "pytest tests/ -v",
    "build_command": "python -m build",
    "lint_command": "ruff check .",
    "default_agent": "gemini"
  }
}
```

### 3. GitHub Repository verlinken (Optional)

```json
{
  "repo": "https://github.com/DEIN_USERNAME/projekt-a",
  "branch": "main"
}
```

### 4. Projekt initialisieren

```bash
cd projects/Projekt-A

# Python Projekt
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# TypeScript Projekt
npm init -y
npm install typescript @types/node --save-dev
npx tsc --init

# React Projekt
npx create-react-app .
```

### 5. Issue Watcher starten

```powershell
cd lazy-bird/scripts
$env:GITHUB_TOKEN = "dein_token"
python issue-watcher.py
```

## 📖 Workflow

### Automatische Entwicklung aktivieren

1. **Issue erstellen** in deinem GitHub Repo
2. **Label hinzufügen:** `lazy-bird`
3. **Optional:** Agent-Hint Labels
   - `security` → Claude (Experte, $20/mo)
   - `documentation` → Gemini (KOSTENLOS)
   - `github-workflow` → Copilot (GitHub-Spezialist)

### Beispiel Issue

```markdown
**Titel:** Add user authentication

**Labels:** lazy-bird, security, feature

**Body:**
Implement JWT-based authentication with:
- User registration
- Login/logout
- Password hashing (bcrypt)
- Access/refresh tokens
- Protected routes

Requirements:
- Use FastAPI for endpoints
- SQLAlchemy for database
- Pytest for tests
- Full test coverage
```

### Was passiert automatisch

1. ✅ Issue Watcher erkennt Issue (alle 60s)
2. ✅ Agent Selector wählt besten AI-Agent
3. ✅ Rover Adapter erstellt isolierten Worktree
4. ✅ AI implementiert Feature in Docker-Container
5. ✅ Tests laufen automatisch
6. ✅ Pull Request wird erstellt
7. 👤 Du reviewst und mergst

## 🎯 Agent-Auswahl

Das System wählt automatisch den optimalen Agent basierend auf Labels:

| Labels | Agent | Kosten | Use Case |
|--------|-------|--------|----------|
| `security`, `architecture` | **Claude** | $20/mo | Sicherheit, komplexe Architektur |
| `documentation`, `bulk-refactor` | **Gemini** | KOSTENLOS | Docs, große Refactorings |
| `github-workflow`, `quick-fix` | **Copilot** | Free/$10 | GitHub Actions, schnelle Fixes |
| Keine spezifischen Labels | **Gemini** | KOSTENLOS | Fallback |

## 📊 Projekt-Status prüfen

```python
cd lazy-bird/scripts
python project-manager.py
```

Zeigt:
- Alle konfigurierten Projekte
- Repository-Status
- Rover-Einstellungen
- Test/Build Commands

## 📚 Weitere Infos

- **Setup-Guide:** [/docs/LAZY-BIRD-SETUP-DE.md](../docs/LAZY-BIRD-SETUP-DE.md)
- **Architektur:** [/docs/LAZY-BIRD-ARCHITECTURE.md](../docs/LAZY-BIRD-ARCHITECTURE.md)
- **Projekt-Konfiguration:** [/lazy-bird/configs/projects.json](../lazy-bird/configs/projects.json)
- **Agent-Mapping:** [/lazy-bird/configs/rover-mapping.json](../lazy-bird/configs/rover-mapping.json)

## 🔧 Troubleshooting

### Projekt wird nicht erkannt

```bash
# Prüfe projects.json Syntax
python -c "import json; json.load(open('../lazy-bird/configs/projects.json'))"

# Liste alle Projekte
cd lazy-bird/scripts
python project-manager.py
```

### Rover findet Projekt nicht

Stelle sicher dass:
- ✅ `path` existiert und korrekt ist
- ✅ `rover_enabled: true` gesetzt ist
- ✅ Git-Repository initialisiert ist (`git init`)

### Tests schlagen fehl

```bash
# Teste manuell
cd projects/Projekt-A
pytest tests/ -v

# Prüfe test_command in projects.json
cat lazy-bird/configs/projects.json | grep -A5 "projekt-a"
```

---

**Bereit für automatisierte Entwicklung!** 🤖🚀
