# Claude Config Setup Guide

## Installierte Tools

### 1. Gemini CLI Advisor
- **Status**: ✅ Konfiguriert
- **MCP-Server**: `gemini-cli`
- **Zweck**: 20 Slash-Commands für Gemini-powered Code-Analyse

**Verfügbare Commands:**
- `/gemini-plan` - Architektur-Planung
- `/gemini-review` - Code-Review
- `/gemini-test` - Test-Generierung
- `/gemini-fix` - Bug-Fixing
- `/gemini-security` - Security-Audit
- `/gemini-optimize` - Performance-Optimierung
- `/gemini-build-cycle` - Kompletter Feature-Workflow
- `/gemini-fix-cycle` - Automatischer Bug-Fix-Workflow
- ... und 12 weitere Commands

**API-Key benötigt**: `GOOGLE_API_KEY` in .env
- Holen Sie sich einen kostenlosen API-Key: https://aistudio.google.com/apikey
- Free Tier: 100 Requests/Tag

### 2. Perplexity MCP Server
- **Status**: ✅ Konfiguriert
- **MCP-Server**: `perplexity`
- **Zweck**: Echtzeit-Web-Suche & Deep Research

**Verfügbare Tools:**
- `perplexity_search` - Schnelle Web-Suche
- `perplexity_ask` - Konversations-KI
- `perplexity_research` - Deep Research
- `perplexity_reason` - Advanced Reasoning

**API-Key**: ✅ Bereits in .env vorhanden
**Kosten**: ~$5-10/Monat bei normaler Nutzung

### 3. GitHub Copilot CLI Integration
- **Status**: ✅ Installiert & Konfiguriert (v0.0.353)
- **MCP-Server**: `copilot-cli`
- **Zweck**: Claude + Copilot = Doppelte KI-Power

**Features:**
- 🤝 Claude kann Copilot um Code-Hilfe fragen
- 🧠 Zwei KI-Gehirne arbeiten zusammen
- 🔧 Copilot's GitHub-Training + Claude's Reasoning
- ⚡ Automatische Integration über MCP

**Konfiguration:**
- ✅ Authentifiziert als: **LEEI1337**
- ✅ Model: `claude-sonnet-4.5`
- ✅ Parallel Tools: Aktiviert
- ✅ Trusted Folders: Desktop, Documents, claude config
- ✅ MCP-Server aktiv

**Verwendung:**
- Claude nutzt Copilot **automatisch** bei Code-Aufgaben
- Keine manuellen Befehle nötig
- Beide AIs arbeiten transparent zusammen

### 4. Docs MCP Server
- **Status**: ✅ Konfiguriert
- **MCP-Server**: `docs`
- **Zweck**: Durchsuchbare Dokumentation für 1000+ Frameworks

**Features:**
- 📚 Indexiert Docs von npm, GitHub, Websites
- 🔍 Version-aware Search (z.B. "React 18 hooks")
- 🔒 100% lokal & privat
- ⚡ Schnelle Suche über cached Docs

**Unterstützte Quellen:**
- NPM Packages (automatisch)
- GitHub Repositories
- Offizielle Docs-Websites
- Lokale Markdown-Dateien

### 5. Postmancer - API Testing
- **Status**: ✅ Konfiguriert
- **MCP-Server**: `postmancer`
- **Zweck**: Postman/Insomnia Alternative für Claude

**Features:**
- 🌐 HTTP Requests (GET, POST, PUT, DELETE)
- 📁 Collections Management
- 🧪 API Testing direkt in Claude
- 💾 Saved Requests
- 🔄 Environment Variables

**Verwendung:**
```javascript
// Claude kann jetzt APIs testen:
"Teste die API https://api.example.com/users"
"Erstelle POST Request mit JSON body"
"Speichere Request in Collection 'MyAPI'"
```

### 6. Time & Timezone Server
- **Status**: ✅ Konfiguriert
- **MCP-Server**: `time`
- **Zweck**: Zeitzone & Datum-Handling

**Features:**
- 🕐 Aktuelle Zeit in beliebiger Timezone
- 🌍 Timezone-Konvertierungen
- 📅 ISO 8601 Formatting
- ⏰ Automatische System-Timezone-Erkennung

### 7. SQLite Database
- **Status**: ✅ Konfiguriert
- **MCP-Server**: `sqlite`
- **Zweck**: Lokale Datenbank für Persistence

**Features:**
- 📊 SQL Queries ausführen
- 💾 Lokale Datenspeicherung
- 📈 Business Intelligence
- 🔍 Schema Inspection

**DB-Pfad:** `C:\Users\Thomas\Desktop\claude config\data.db`

### 8. PostgreSQL (Optional)
- **Status**: ⚙️ Konfiguriert (needs DATABASE_URL)
- **MCP-Server**: `postgres`
- **Zweck**: Read-Only PostgreSQL Access

**Setup:**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

### 9. Rover - Multi-Agent Manager
- **Status**: ✅ Installiert (v1.4.1)
- **Docker**: ✅ Verfügbar (v28.5.1)
- **Zweck**: Parallele Agent-Orchestrierung in isolierten Containern

**Verwendung:**
```bash
# Task erstellen
rover task "Feature implementieren"

# Status prüfen
rover ls -w

# Task inspizieren
rover inspect 1

# Ergebnisse mergen
rover merge 1
```

## Aktive MCP-Server (18 Total!)

**Core Server (5):**
1. **filesystem** - Dateisystem-Zugriff
2. **memory** - Wissens-Graph & Kontext
3. **github** - GitHub-Integration
4. **brave-search** - Web-Suche (kostenlos)
5. **sequential-thinking** - Reflektives Reasoning

**Multi-LLM Integration (3):**
6. **gemini-cli** - Gemini AI-Integration
7. **perplexity** - Perplexity AI-Suche
8. **copilot-cli** - ✅ GitHub Copilot Integration

**Development Tools (6):**
9. **playwright** - Browser-Automatisierung
10. **browser-tools** - Erweiterte Browser-Tools
11. **studentofjs** - Everything Server
12. **mcp-inspector** - MCP Debugging
13. **docs** - ✅ **NEU!** Durchsuchbare Dokumentation
14. **postmancer** - ✅ **NEU!** API Testing (Postman Alternative)

**Data & Utilities (4):**
15. **time** - ✅ **NEU!** Timezone & Datum-Handling
16. **sqlite** - ✅ **NEU!** Lokale SQLite Datenbank
17. **postgres** - ✅ **NEU!** PostgreSQL Integration (optional)
18. **Rover** - Multi-Agent Orchestrierung

## Benötigte API-Keys

### ✅ Bereits vorhanden:
- `GITHUB_TOKEN` - GitHub API
- `BRAVE_API_KEY` - Brave Search API
- `PERPLEXITY_API_KEY` - Perplexity AI

### ⚠️ Noch hinzufügen:
- `GOOGLE_API_KEY` - Für Gemini CLI Advisor
  - Holen unter: https://aistudio.google.com/apikey
  - In .env eintragen

## Kosten-Übersicht

| Service | Status | Kosten/Monat |
|---------|--------|--------------|
| GitHub API | ✅ Aktiv | $0 |
| Brave Search | ✅ Aktiv | $0 (2000 req/Monat) |
| Gemini API | ⚠️ Key fehlt | $0 (Free Tier 100/Tag) |
| Perplexity API | ✅ Aktiv | ~$5-10 |
| Rover Software | ✅ Installiert | $0 |
| **GESAMT** | | **~$5-10/Monat** |

## Nächste Schritte

1. **Gemini API Key holen**:
   - Gehe zu https://aistudio.google.com/apikey
   - Erstelle einen API-Key
   - Füge ihn in .env ein: `GOOGLE_API_KEY=your-key-here`

2. **Claude Code neu starten**:
   - Damit alle MCP-Server geladen werden
   - Gemini-Commands verfügbar werden

3. **Testen**:
   ```bash
   # Gemini Commands testen
   /gemini-plan "Neue Feature-Idee"

   # Perplexity Suche nutzen
   # (automatisch in Claude Code verfügbar)

   # Rover Task starten
   rover task "Test-Implementierung"
   ```

## Workflows

### Multi-LLM-Strategie:
- **Claude Code** - Haupt-Orchestrierung, komplexe Logik
- **GitHub Copilot** - Code-Generierung, GitHub-spezifisches Wissen (NEU!)
- **Gemini** - Code-Reviews, Testing, Planung
- **Perplexity** - Web-Recherche, aktuelle Docs

**Workflow-Beispiel:**
1. Claude analysiert Ihre Anfrage
2. Bei Code-Aufgaben → fragt Copilot um Hilfe
3. Bei Recherche → nutzt Perplexity/Brave
4. Bei Reviews → nutzt Gemini
5. Alle Ergebnisse werden kombiniert & optimiert

### Parallel-Development mit Rover:
1. `rover task "Feature A"` - Task 1 in Container
2. `rover task "Feature B"` - Task 2 parallel
3. Beide entwickeln gleichzeitig in isolierten Umgebungen
4. `rover merge 1 && rover merge 2` - Ergebnisse integrieren

## Troubleshooting

### Gemini CLI funktioniert nicht:
- Prüfen: `GOOGLE_API_KEY` in .env gesetzt?
- Testen: `npx -y gemini-mcp-tool`
- API-Key valide? Prüfen unter https://aistudio.google.com/

### Perplexity Fehler:
- API-Key valide? Testen unter https://www.perplexity.ai/account/api
- Guthaben vorhanden?

### Rover startet nicht:
- Docker läuft? `docker ps`
- Windows: Docker Desktop gestartet?

## Weitere Ressourcen

- Gemini CLI Docs: https://github.com/jezweb/gemini-cli-advisor-for-claude-code
- Rover Docs: https://github.com/endorhq/rover
- Perplexity API Docs: https://docs.perplexity.ai/

---

**Setup abgeschlossen am**: 2025-11-08
**Claude Code Version**: Latest
**Konfiguriert von**: Claude Code Assistant
