# 🏗️ Architektur-Übersicht

**Einfache 3-Ebenen-Architektur für Multi-AI Orchestrierung.**

---

## Die 3 Ebenen

```
┌─────────────────────────────────────────┐
│  EBENE 3: ROVER                         │
│  • Orchestriert parallele AI-Tasks      │
│  • Erstellt isolierte git worktrees     │
│  • Verwaltet Docker Container           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  EBENE 2: AI CLIs (Isoliert)            │
│  ┌──────┬──────┬──────┐                 │
│  │Claude│Gemini│Copilot                 │
│  └──────┴──────┴──────┘                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  EBENE 1: MCP SERVER (Geteilt)          │
│  18 Server mit Tools & Daten            │
└─────────────────────────────────────────┘
```

---

## AI Rollen-Spezialisierung

### Claude ($20/Monat) - Senior Architect
**10-20% der Tasks**

✅ Nutze für:
- Security Audits
- Architektur-Design
- Komplexes Debugging
- Code Reviews

❌ Nicht nutzen für:
- Bulk-Operationen → Gemini
- GitHub Ops → Copilot
- Dokumentation → Gemini

### Gemini (KOSTENLOS!) - Bulk Worker
**60-70% der Tasks**

✅ Nutze für:
- Large-Scale Dokumentation (2M Token Context!)
- Repository-weite Analyse
- Bulk Refactoring
- Daten-Verarbeitung

❌ Nicht nutzen für:
- Security-kritischer Code → Claude
- GitHub Operationen → Copilot

### Copilot ($0-10/Monat) - GitHub Specialist
**20-30% der Tasks**

✅ Nutze für:
- GitHub PR/Issues
- Quick Fixes
- Single-File Edits
- Workflow Updates

❌ Nicht nutzen für:
- Große Analysen → Gemini
- Security Audits → Claude

---

## MCP Server (18 Total)

**Von allen AIs geteilt, aber separat konfiguriert:**

- `filesystem` - Datei-Operationen
- `github` - GitHub Integration
- `memory` - Context Persistence
- `docs` - Dokumentations-Suche
- `gemini-cli` - Gemini Zugriff
- `copilot-cli` - Copilot Zugriff
- `sqlite` - Datenbank Operationen
- `playwright` - Browser Automation
- `brave-search` - Web-Suche
- ... und 9 weitere

Jede AI CLI hat ihre eigene `.mcp.json` oder Config-Datei.

---

## Kern-Prinzipien

### 1. Isolation
Jede AI CLI ist **komplett isoliert**:
- Separate Configs
- Separate MCP Server Listen
- Keine direkte Kommunikation

### 2. Spezialisierung
Jede AI hat eine **optimale Rolle**:
- Claude: Experte (teuer, nur kritisch)
- Gemini: Worker (gratis, maximieren)
- Copilot: Spezialist (GitHub + quick tasks)

### 3. Orchestrierung
Rover **verwaltet Prozesse**, kein MCP-Zugriff:
- Startet separate CLI Prozesse
- Erstellt git worktrees
- Läuft in Docker Containern

---

## Kosten-Strategie

```
60-70% Gemini   → KOSTENLOS (1000/Tag)
20-30% Copilot  → $0-10/Monat
10-20% Claude   → $20/Monat
────────────────────────────────────
Total: $20-30/Monat
```

**vs.** Claude Max für alles: $100-200/Monat

---

## Datenfluss Beispiel

```
User: "Behebe Security-Issue in auth.ts"
  ↓
Rover erstellt isolierten Workspace
  ↓
Rover startet Claude CLI (Security Task)
  ↓
Claude nutzt MCP Server:
  - filesystem (liest auth.ts)
  - github (prüft PR History)
  - memory (merkt sich Context)
  ↓
Claude behebt Issue
  ↓
Rover merged Änderungen zurück
```

---

**Mehr erfahren:**
- [Dokumentations-Index](INDEX.md) - Alle Dokumentation organisiert
- [MCP Servers](MCP-SERVERS.md) - Alle 18 Server erklärt
- [Schnellstart](QUICKSTART-DE.md) - In 5 Minuten loslegen
