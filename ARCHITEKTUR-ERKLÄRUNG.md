# 🏗️ AI Development Stack - Vollständige Architektur

**Die komplette Hierarchie & Interaktion aller AI-Systeme**

---

## 📊 Die 3 Ebenen

```
┌─────────────────────────────────────────────────────────────┐
│                    EBENE 3: ORCHESTRATION                    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                      ROVER                           │    │
│  │  - Verwaltet mehrere SEPARATE CLI-Prozesse         │    │
│  │  - Jeder Task = eigener Git Worktree + Container   │    │
│  │  - Kein direkter Zugriff auf MCP/Skills            │    │
│  └─────────────────────────────────────────────────────┘    │
│         │              │                │                     │
│         ▼              ▼                ▼                     │
└─────────────────────────────────────────────────────────────┘
         │              │                │
         │              │                │
┌────────┴──────────────┴────────────────┴─────────────────────┐
│              EBENE 2: AI CLI TOOLS (ISOLIERT!)               │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Claude Code  │  │  Gemini CLI  │  │ Copilot CLI  │       │
│  │    CLI       │  │              │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                 │                 │                │
│         ▼                 ▼                 ▼                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ .mcp.json    │  │~/.gemini/    │  │~/.copilot/   │       │
│  │ (18 Server)  │  │settings.json │  │mcp-config.json│      │
│  │              │  │ (eigene MCP) │  │ (9 Server)   │       │
│  │ AGENTS.md    │  │              │  │agents/*.md   │       │
│  │ .claude/     │  │              │  │              │       │
│  │ skills/      │  │              │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────────────────────────────────────────────┘
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│              EBENE 1: MCP SERVER (GETEILT)                   │
│                                                               │
│  ┌────────┬────────┬────────┬─────────┬──────────┐          │
│  │ docs   │postman │sqlite  │playwright│ github  │  ...     │
│  └────────┴────────┴────────┴─────────┴──────────┘          │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 🔍 Ebene für Ebene erklärt

### **EBENE 1: MCP Server (Die Basis)**

**Was sind MCP Server?**
- Standalone Node.js Prozesse
- Kommunizieren via stdio (Standard Input/Output)
- Können von **jedem** MCP-Client genutzt werden

**Beispiel:**
```bash
# MCP Server läuft als separater Prozess
npx @modelcontextprotocol/server-docs

# Kann von verbinden:
# - Claude Code ✅
# - Gemini CLI ✅
# - Copilot CLI ✅
# - Jeder MCP-Client ✅
```

**WICHTIG:**
- MCP Server sind **shared resources**
- Können von mehreren Clients gleichzeitig genutzt werden
- Haben KEINE Ahnung wer sie nutzt (Claude? Gemini? Copilot?)

---

### **EBENE 2: AI CLI Tools (Isoliert!)**

#### **Claude Code CLI**

**Eigene Configs:**
```
.mcp.json           → 18 MCP Server konfiguriert
.claude/skills/     → 22 Skills (NUR für Claude!)
AGENTS.md           → 4 Agents (repo-level)
.env                → Shared environment vars
```

**Was Claude kann:**
```bash
# Claude nutzt EIGENE MCP Server
claude "Search React docs"
→ Nutzt MCP 'docs' server aus .mcp.json

# Claude nutzt EIGENE Skills
claude → Skill 'test-driven-development' aktiv
→ NUR Claude hat Skills!

# Claude kann NICHT direkt Gemini/Copilot steuern
# (Außer via Rover auf höherer Ebene)
```

**Subagenten in Claude:**
- ❌ **NICHT** Gemini als Subagent
- ❌ **NICHT** Copilot als Subagent
- ✅ **JA** - Task-Tool für parallele Tasks (aber intern)
- ✅ **JA** - @agent mentions (via AGENTS.md)

#### **Gemini CLI**

**Eigene Configs:**
```
~/.gemini/settings.json  → Gemini MCP Config
~/.gemini/              → Eigene Settings
```

**Was Gemini kann:**
```bash
# Gemini nutzt EIGENE MCP Server config
gemini "Analyze code"
→ Nutzt MCP Server aus ~/.gemini/settings.json

# Gemini hat KEINE Claude Skills
# Gemini hat KEINE Claude Subagents
# Gemini ist STANDALONE CLI
```

#### **Copilot CLI**

**Eigene Configs:**
```
~/.copilot/mcp-config.json  → 9 MCP Server
~/.copilot/agents/*.md      → 4 Custom Agents
~/.copilot/config.json      → Settings
```

**Was Copilot kann:**
```bash
# Copilot nutzt EIGENE MCP Server
copilot "Test API"
→ Nutzt MCP 'postmancer' aus ~/.copilot/mcp-config.json

# Copilot nutzt EIGENE Agents
copilot /agent code-expert
→ Lädt ~/.copilot/agents/code-expert.md

# Copilot hat KEINE Claude Skills
# Copilot ist STANDALONE CLI
```

**KRITISCH:**
- Jedes CLI ist **isoliert**
- Jedes hat **eigene Config**
- Jedes nutzt **eigene MCP Server** (können gleiche sein!)
- **KEIN direkter Zugriff** auf andere CLI's Skills/Agents

---

### **EBENE 3: Rover (Orchestration)**

**Was Rover WIRKLICH macht:**

```bash
# Rover startet SEPARATE CLI-Prozesse
rover task "Analyze code" --agent claude

# Was passiert:
1. Rover erstellt git worktree
2. Rover startet Docker Container
3. Rover führt AUS: `claude "Analyze code"` im Container
4. Claude nutzt .mcp.json (im Container)
5. Claude nutzt .claude/skills/ (im Container)
6. Ergebnis → Rover sammelt Output
```

**Rover ist NICHT:**
- ❌ Ein Super-Agent der alle steuert
- ❌ Hat KEINEN direkten MCP-Zugriff
- ❌ Hat KEINE eigenen Skills/Agents
- ❌ Kann NICHT Claude's Skills direkt nutzen

**Rover IST:**
- ✅ Ein **Process Manager**
- ✅ Startet separate CLI-Prozesse
- ✅ Managed Git Worktrees
- ✅ Managed Docker Containers
- ✅ Sammelt Outputs & mergt Results

---

## ❓ Ihre Fragen - Beantwortet

### **1. "Claude kann Gemini und Copilot als Subagenten nutzen?"**

**NEIN - NICHT DIREKT!**

**Was Claude KANN:**
```bash
# Via MCP 'copilot-cli' Server
claude → copilot-mcp-server → Copilot CLI
# Aber: Nur indirekt, als Tool-Call

# Via MCP 'gemini' Server (wenn konfiguriert)
claude → gemini-mcp-server → Gemini
# Aber: Auch nur als Tool
```

**Was Claude NICHT kann:**
```bash
# Direkter Zugriff auf Copilot's Agents
claude → ❌ ~/.copilot/agents/code-expert.md
# Geht NICHT! Das ist Copilot's Territory

# Direkter Zugriff auf Gemini Settings
claude → ❌ ~/.gemini/settings.json
# Geht NICHT! Isolierte Config
```

**ABER - via Rover indirekt:**
```bash
# Rover kann orchestrieren
rover task "Claude task" --agent claude
rover task "Gemini task" --agent gemini

# Beide laufen parallel, aber ISOLIERT
# Kein direkter Zugriff aufeinander
```

---

### **2. "Rover ist eine Ebene höher und steuert alle CLIs?"**

**JA - ABER NUR ALS PROCESS MANAGER!**

**Was Rover macht:**
```bash
rover task "Task 1" --agent claude
# → Startet: `claude "Task 1"` in Container

rover task "Task 2" --agent gemini
# → Startet: `gemini "Task 2"` in anderem Container

rover task "Task 3" --agent copilot
# → Startet: `copilot "Task 3"` in anderem Container
```

**Was Rover NICHT macht:**
```bash
# Rover hat KEINEN Zugriff auf:
❌ Claude's Skills
❌ Copilot's Agents
❌ Gemini's Settings
❌ MCP Server direkt

# Rover managed NUR:
✅ Git Worktrees
✅ Docker Containers
✅ CLI-Prozess Lifecycle
✅ Output Collection
```

---

### **3. "MCP Server, Skills, Subagenten in allen verfügbar?"**

**TEILWEISE - hier die Details:**

#### **MCP Server:**
**✅ JA - aber separat konfiguriert**

```
Claude:   .mcp.json (18 Server)
Gemini:   ~/.gemini/settings.json (custom)
Copilot:  ~/.copilot/mcp-config.json (9 Server)

Jeder CLI hat EIGENE MCP Config!
Können gleiche Server sein, aber separat konfiguriert.
```

**Beispiel:**
```json
// Claude's .mcp.json
{
  "docs": {...},
  "postmancer": {...},
  "sqlite": {...}
}

// Copilot's mcp-config.json
{
  "docs": {...},      // ✅ Gleicher Server
  "postmancer": {...}, // ✅ Gleicher Server
  "sqlite": {...}      // ✅ Gleicher Server
}

// Beide nutzen DENSELBEN MCP Server-Prozess
// Aber via EIGENE Config!
```

#### **Skills:**
**❌ NEIN - NUR Claude Code!**

```
.claude/skills/  → Nur für Claude Code
Gemini hat KEINE Skills
Copilot hat KEINE Skills
```

**Skills sind Claude-spezifisch!**

#### **Subagenten/Agents:**
**JEDER HAT EIGENE!**

```
Claude:   AGENTS.md (repo-level)
Copilot:  ~/.copilot/agents/*.md
Gemini:   KEINE Agents
```

**WICHTIG:**
- Copilot's Agents ≠ Claude's Agents
- Nur Format/Namen sind ähnlich
- Funktional ISOLIERT

---

## 🔄 Wie es WIRKLICH zusammenarbeitet

### **Szenario 1: Claude nutzt Copilot (indirekt)**

```bash
# In .mcp.json konfiguriert:
{
  "copilot-cli": {
    "command": "npx copilot-mcp-server"
  }
}

# Claude nutzt Copilot als MCP Tool
claude "Ask Copilot to review code"

# Flow:
Claude → copilot-mcp-server (MCP) → Copilot CLI
                                   ↓
                         Copilot's eigene Config
                         Copilot's eigene Agents
                                   ↓
                              Result zurück
```

**Aber:**
- Claude hat KEINEN direkten Zugriff auf Copilot's Agents
- Nur via MCP Server als "black box"

---

### **Szenario 2: Rover orchestriert parallel**

```bash
rover task "Analyze with Claude" --agent claude
rover task "Docs with Gemini" --agent gemini

# Was passiert:

Container 1 (Claude):
├── Git Worktree 1
├── Eigene .mcp.json
├── Eigene .claude/skills/
└── `claude "Analyze..."`

Container 2 (Gemini):
├── Git Worktree 2
├── Eigene ~/.gemini/settings.json
└── `gemini "Docs..."`

# KOMPLETT ISOLIERT!
# Kein Zugriff aufeinander!
```

---

### **Szenario 3: Shared MCP Server**

```bash
# Claude nutzt 'docs' server
claude "Search React docs"
→ npx docs-mcp-server (Prozess A)

# Copilot nutzt 'docs' server
copilot "Search Vue docs"
→ npx docs-mcp-server (Prozess A)

# GLEICHER Server-Prozess!
# Aber separate Clients!
```

---

## ✅ Die Wahrheit

### **WAS FUNKTIONIERT:**

1. **MCP Server sharing:**
   ```
   Claude → docs-mcp-server ← Copilot
   Gleicher Server, verschiedene Clients
   ```

2. **Rover Process Management:**
   ```
   Rover → Startet Claude (Container 1)
        → Startet Gemini (Container 2)
        → Startet Copilot (Container 3)
   Alle parallel, alle isoliert
   ```

3. **Indirekte Integration:**
   ```
   Claude → copilot-mcp-server → Copilot
   (Claude nutzt Copilot als Tool, nicht als Subagent)
   ```

### **WAS NICHT FUNKTIONIERT:**

1. **Direkte Subagents:**
   ```
   Claude → ❌ Gemini als Subagent
   Claude → ❌ Copilot als Subagent
   (Keine native Subagent-Funktion)
   ```

2. **Skill Sharing:**
   ```
   Copilot → ❌ .claude/skills/
   Gemini → ❌ .claude/skills/
   (Skills nur für Claude)
   ```

3. **Agent Sharing:**
   ```
   Claude → ❌ ~/.copilot/agents/
   Copilot → ❌ AGENTS.md direkt
   (Separate Configs)
   ```

---

## 🎯 RICHTIGE Mentale Model

**Denken Sie an:**
- **MCP Server** = Shared Libraries (wie npm packages)
- **CLI Tools** = Separate Apps (Chrome, Firefox, Edge)
- **Rover** = Process Manager (wie systemd/PM2)

**Nicht denken an:**
- ❌ Claude steuert Gemini/Copilot
- ❌ Alle teilen Skills/Agents
- ❌ Rover ist Super-AI

**Sondern:**
- ✅ Jedes CLI ist eigenständig
- ✅ MCP Server sind shared resources
- ✅ Rover managed separate Prozesse
- ✅ Integration via MCP (nicht direkt)

---

## 📊 Zusammenfassung

| Feature | Claude | Gemini | Copilot | Rover |
|---------|--------|--------|---------|-------|
| **Eigene Config** | ✅ .mcp.json | ✅ ~/.gemini/ | ✅ ~/.copilot/ | ❌ Keine |
| **MCP Server** | ✅ 18 | ✅ Custom | ✅ 9 | ❌ Nutzt nur CLIs |
| **Skills** | ✅ 22 | ❌ Keine | ❌ Keine | ❌ Keine |
| **Agents** | ✅ AGENTS.md | ❌ Keine | ✅ agents/*.md | ❌ Keine |
| **Subagents** | ⚠️ Nur via MCP | ❌ Keine | ⚠️ Nur via MCP | ❌ Keine |
| **Parallel Tasks** | ⚠️ Intern | ❌ Keine | ❌ Keine | ✅ **JA!** |

**Legende:**
- ✅ = Native Support
- ⚠️ = Möglich aber nicht direkt
- ❌ = Nicht verfügbar

---

## 🚀 Best Use Case

**Optimal Workflow:**

```bash
# 1. Rover orchestriert verschiedene CLIs
rover task "Architecture review" --agent claude
rover task "Codebase analysis (2M tokens)" --agent gemini
rover task "GitHub PR review" --agent copilot

# 2. Jeder CLI nutzt EIGENE Stärken:
# - Claude: Claude's Skills + Sequential Thinking
# - Gemini: 2M token context + Speed
# - Copilot: GitHub integration + Custom agents

# 3. MCP Server werden geteilt:
# - Alle nutzen 'docs' für documentation
# - Alle nutzen 'postmancer' für API testing
# - Alle nutzen 'sqlite' für data

# 4. Rover merged Results
rover merge 1 2 3
```

---

**Sie verstehen es fast perfekt - nur die Details sind wichtig! 🎯**

**Key Takeaway:**
- Jedes CLI ist **eigenständig**
- MCP Server sind **shared**
- Rover **managed Prozesse**
- **Keine direkte Subagent-Beziehung**
- Integration **via MCP Protocol**
