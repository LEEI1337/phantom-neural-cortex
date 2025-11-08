# Claude Code vs GitHub Copilot CLI - Vollständiger Setup-Guide

**Stand:** 2025-11-08

## Übersicht

Beide Tools können **parallel** verwendet werden und teilen sich MCP-Server und Konfigurationen.

---

## 🔧 Unterschiede

| Feature | Claude Code CLI | Claude VSCode Extension | Copilot CLI |
|---------|----------------|------------------------|-------------|
| **Config Location** | `~/.claude/` | VSCode Settings | `~/.copilot/` |
| **MCP Config** | `.mcp.json` (project) | `.mcp.json` (project) | `~/.copilot/mcp-config.json` |
| **Agents** | `AGENTS.md` (project) | `AGENTS.md` (project) | `~/.copilot/agents/*.md` |
| **Custom Instructions** | `.github/copilot-instructions.md` | Same | `.github/copilot-instructions.md` |
| **Subagents** | ✅ Ja | ❌ Noch nicht | ✅ Ja (Custom Agents) |
| **Checkpoints** | ✅ Ja | ❌ Noch nicht | ✅ Ja (Session State) |
| **Model Selection** | CLI oder Config | VS Code Settings | CLI Flags |
| **MCP Inspector** | ✅ Ja | ✅ Ja | ✅ Ja |

---

## 📁 Dateistruktur für BEIDE Systeme

```
C:\Users\Thomas\Desktop\claude config\
├── .claude/                          # Claude Code Settings (lokal)
│   ├── settings.json                 # Permissions
│   ├── commands/                     # Slash Commands
│   └── skills/                       # Claude Skills
│
├── .github/                          # Gemeinsam für alle
│   └── copilot-instructions.md       # Custom Instructions (BEIDE nutzen)
│
├── AGENTS.md                         # Repo-level Agents (BEIDE nutzen)
├── .mcp.json                         # MCP Server Config (BEIDE nutzen)
├── .env                              # Environment Variables (BEIDE nutzen)
└── memory-bank/                      # Memory System (BEIDE nutzen)

C:\Users\Thomas\.copilot\
├── config.json                       # Copilot CLI Settings
├── mcp-config.json                   # Copilot MCP Server Config
├── agents/                           # Copilot Custom Agents
│   ├── code-expert.md
│   ├── debug-specialist.md
│   └── api-tester.md
└── session-state/                    # Session Persistence
```

---

## ⚙️ Konfiguration

### 1. Claude Code (CLI & VSCode Extension)

#### MCP Server Config (`.mcp.json`)
```json
{
  "mcpServers": {
    "filesystem": {...},
    "memory": {...},
    "github": {...},
    "docs": {...},
    "postmancer": {...},
    // ... 18 Server total
  }
}
```

**Location:** `C:\Users\Thomas\Desktop\claude config\.mcp.json`

**Verwendet von:**
- ✅ Claude Code CLI
- ✅ Claude Code VSCode Extension

---

### 2. GitHub Copilot CLI

#### MCP Server Config (`~/.copilot/mcp-config.json`)
```json
{
  "mcpServers": {
    "filesystem": {...},
    "memory": {...},
    "github": {...},
    "docs": {...},
    "postmancer": {...},
    "playwright": {...},
    "time": {...},
    "sqlite": {...}
  }
}
```

**Location:** `C:\Users\Thomas\.copilot\mcp-config.json`

**Verwendet von:**
- ✅ GitHub Copilot CLI only

**Unterschied zu Claude:**
- Copilot nutzt eigene Config in `~/.copilot/`
- Kann unterschiedliche Server haben (wir synchronisieren die wichtigsten)

---

## 🤖 Agents System

### Claude Code: AGENTS.md (Repo-Level)

**Location:** `C:\Users\Thomas\Desktop\claude config\AGENTS.md`

**Format:**
```markdown
## Available Agents

### 1. Code Expert (@code-expert)
...

### 2. Debug Specialist (@debug-specialist)
...
```

**Verwendung:**
```bash
# Claude Code CLI
claude "Help me @code-expert"

# Claude VSCode Extension
"@code-expert review this code"
```

---

### Copilot CLI: Custom Agents

**Location:** `C:\Users\Thomas\.copilot\agents\*.md`

**Files:**
- `code-expert.md`
- `debug-specialist.md`
- `api-tester.md`

**Verwendung:**
```bash
# Copilot CLI
copilot /agent code-expert

# Interactive selection
copilot
> /agent
```

---

## 🔄 Synchronisation

### Was wird geteilt:

1. **✅ Environment Variables** (`.env`)
   - GITHUB_TOKEN
   - BRAVE_API_KEY
   - GOOGLE_API_KEY
   - PERPLEXITY_API_KEY

2. **✅ Custom Instructions** (`.github/copilot-instructions.md`)
   - Code Style
   - Security Requirements
   - Testing Standards

3. **✅ Repository Context** (`AGENTS.md`)
   - Agent Beschreibungen
   - Use Cases
   - MCP Server Liste

4. **✅ Memory Bank** (`memory-bank/`)
   - Persistenter Kontext
   - Architektur-Entscheidungen
   - System-Patterns

### Was ist separat:

1. **❌ MCP Server Configs**
   - Claude: `.mcp.json` (18 Server)
   - Copilot: `~/.copilot/mcp-config.json` (9 Server)
   - **Grund:** Copilot braucht nicht alle Server

2. **❌ Agent Definitions**
   - Claude: `AGENTS.md` (Markdown Format)
   - Copilot: `~/.copilot/agents/*.md` (Separate Dateien)
   - **Grund:** Unterschiedliche Formate

3. **❌ Session State**
   - Claude: Memory Bank
   - Copilot: `~/.copilot/session-state/`
   - **Grund:** Unterschiedliche Implementierungen

---

## 🚀 Verwendung

### Scenario 1: Code Review

**Mit Claude Code:**
```bash
cd "C:\Users\Thomas\Desktop\claude config"
claude "@code-expert review src/components/UserProfile.tsx"
```

**Mit Copilot CLI:**
```bash
cd "C:\Users\Thomas\Desktop\claude config"
copilot /agent code-expert
> Review the UserProfile component
```

**In VSCode Extension:**
- Öffne Command Palette (Ctrl+Shift+P)
- "Claude Code: Chat"
- "@code-expert review this file"

---

### Scenario 2: API Testing

**Mit Claude Code:**
```bash
claude "@api-tester test GET https://api.github.com/users/octocat"
```

**Mit Copilot CLI:**
```bash
copilot /agent api-tester
> Test the GitHub API
```

---

### Scenario 3: Debugging

**Mit Claude Code:**
```bash
claude "@debug-specialist I'm getting CORS errors"
```

**Mit Copilot CLI:**
```bash
copilot /agent debug-specialist
> Help me debug CORS errors
```

---

## 🎯 Welches Tool wann?

| Aufgabe | Empfohlen | Warum |
|---------|-----------|-------|
| Code-Generierung | **Copilot CLI** | Direkter GitHub-Zugriff |
| Komplexes Reasoning | **Claude Code** | Sequential Thinking |
| API Testing | **Beide** | Postmancer in beiden |
| Debugging | **Claude Code** | Bessere Analyse |
| Quick Edits | **Copilot** | Schneller |
| Architektur | **Claude Code** | Tiefere Kontexte |
| Git Operations | **Copilot CLI** | Native GitHub Integration |
| Browser Testing | **Claude Code** | Playwright Support |

---

## 🔧 Optimierungen

### Copilot CLI Performance

**In `~/.copilot/config.json`:**
```json
{
  "defaultModel": "claude-sonnet-4.5",
  "logLevel": "warning",
  "streamMode": "on",
  "parallelToolsExecution": true
}
```

**In `.env`:**
```env
COPILOT_MODEL=claude-sonnet-4.5
COPILOT_STREAM=on
COPILOT_PARALLEL_TOOLS=true
```

### Claude Code Performance

**In `.claude/settings.json`:**
```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Edit(*)",
      "Read(*)",
      "Write(*)"
    ]
  }
}
```

---

## 📊 Setup-Status

### ✅ Claude Code
- [x] 18 MCP-Server konfiguriert
- [x] Custom Skills aktiv
- [x] Slash Commands verfügbar
- [x] Memory Bank konfiguriert
- [x] Permissions optimiert
- [x] AGENTS.md erstellt

### ✅ Copilot CLI
- [x] 9 MCP-Server konfiguriert
- [x] 3 Custom Agents erstellt
- [x] Config optimiert
- [x] Authentifiziert (LEEI1337)
- [x] Model: claude-sonnet-4.5
- [x] Parallel Tools aktiviert

### ✅ Gemeinsame Ressourcen
- [x] .env mit allen API Keys
- [x] .github/copilot-instructions.md
- [x] AGENTS.md
- [x] Memory Bank synchronisiert

---

## 🐛 Troubleshooting

### Copilot erkennt Agents nicht
```bash
# Prüfen
ls ~/.copilot/agents/

# Fix: Agents erstellen
mkdir -p ~/.copilot/agents
# Dateien manuell kopieren
```

### MCP Server starten nicht
```bash
# Claude Code
claude --mcp-debug

# Copilot
copilot --log-level debug
```

### Environment Variables werden nicht geladen
```bash
# Prüfen
cat .env

# In Copilot testen
copilot -p "What's my GITHUB_TOKEN?" --allow-all-tools
```

---

## 📚 Weitere Ressourcen

- [Claude Code Docs](https://docs.claude.com/en/docs/claude-code)
- [GitHub Copilot CLI Docs](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-cli)
- [MCP Specification](https://modelcontextprotocol.io)
- [Custom Agents Guide](https://github.blog/changelog/2025-10-28-custom-agents-for-github-copilot/)

---

**BEIDE SYSTEME FUNKTIONIEREN PARALLEL! 🚀**

Sie teilen sich:
- ✅ Environment Variables
- ✅ Custom Instructions
- ✅ Memory Bank
- ✅ Repository Context

Aber haben eigene:
- 📁 MCP Configs (angepasst)
- 🤖 Agent Formats (kompatibel)
- ⚙️ Settings (optimiert)

**Setup ist komplett! Beide Tools ready to use!**
