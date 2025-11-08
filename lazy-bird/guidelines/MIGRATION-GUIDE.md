# 🔄 Migration Guide: Old → New Guideline System

**Von:** Alte standalone Guidelines (PROJECT-STRUCTURE.md, claude-guidelines.md, etc.)
**Nach:** Hierarchisches Layer-System (LAYER-0 bis LAYER-4)

---

## 📋 Was hat sich geändert?

### Alte Struktur (Deprecated)

```
lazy-bird/guidelines/
├── PROJECT-STRUCTURE.md      # Universal rules (DUPLIKATION!)
├── claude-guidelines.md       # Claude rules (enthält Universal rules NOCHMAL)
├── gemini-guidelines.md       # Gemini rules (enthält Universal rules NOCHMAL)
└── copilot-guidelines.md      # Copilot rules (enthält Universal rules NOCHMAL)
```

**Problem:** Massive Duplikation!
- Universal Standards 4x wiederholt
- Änderung in Projekt-Struktur → 4 Dateien updaten
- Unklar welche Guidelines für welchen Layer

### Neue Struktur (Aktuell)

```
lazy-bird/guidelines/
├── LAYER-SYSTEM.md            # Übersicht & Architektur
│
├── layers/                     # Hierarchische Guidelines
│   ├── LAYER-0.md             # Universal (BASIS - gilt für ALLE)
│   ├── LAYER-1.md             # MCP Servers
│   ├── LAYER-2.md             # AI CLI General
│   ├── LAYER-2-CLAUDE.md      # Claude-spezifisch
│   ├── LAYER-2-GEMINI.md      # Gemini-spezifisch
│   ├── LAYER-2-COPILOT.md     # Copilot-spezifisch
│   ├── LAYER-3.md             # Rover Orchestration
│   └── LAYER-4.md             # Lazy Bird Automation
│
├── tools/
│   └── guideline-injector.py  # Auto-Injection System
│
└── legacy/                     # Alte Dateien (Reference)
    ├── PROJECT-STRUCTURE.md
    ├── claude-guidelines.md
    ├── gemini-guidelines.md
    └── copilot-guidelines.md
```

**Vorteile:**
- ✅ Keine Duplikation
- ✅ Universal Standards nur 1x (LAYER-0)
- ✅ Klare Hierarchie
- ✅ Automatische Vererbung

---

## 🔄 Layer-Mapping

### Layer 0: Universal Standards

**Quelle:** `PROJECT-STRUCTURE.md`
**Neu:** `layers/LAYER-0.md`

**Inhalt:**
- Projekt-Struktur (src/, tests/, docs/)
- Naming Conventions
- Code Quality Basics
- Security Fundamentals
- Testing Basics

**Gilt für:** ALLE Agents, ALLE Layer

### Layer 1: MCP Server Usage

**Quelle:** NEU (war nicht explizit dokumentiert)
**Neu:** `layers/LAYER-1.md`

**Inhalt:**
- Welche 18 MCP Server verfügbar
- Wie man sie nutzt
- Rate Limits
- Caching Best Practices

**Gilt für:** Alle AI CLIs

### Layer 2: AI CLI

**Quelle:** `claude-guidelines.md`, `gemini-guidelines.md`, `copilot-guidelines.md`
**Neu:**
- `layers/LAYER-2.md` (General)
- `layers/LAYER-2-CLAUDE.md`
- `layers/LAYER-2-GEMINI.md`
- `layers/LAYER-2-COPILOT.md`

**Inhalt:**
- Tool Usage (Read, Write, Edit, Bash)
- Commit Message Format
- PR Creation
- Agent-spezifische Features

**Gilt für:** Direkte CLI Nutzung oder Rover-Aufrufe

### Layer 3: Rover Orchestration

**Quelle:** NEU (war implizit in Rover Docs)
**Neu:** `layers/LAYER-3.md`

**Inhalt:**
- Git Worktree Management
- Docker Container Regeln
- Test Validation vor Merge
- Rover CLI Command Format

**Gilt für:** Rover-orchestrierte Tasks

### Layer 4: Lazy Bird Automation

**Quelle:** NEU (war in LAZY-BIRD-SETUP Docs)
**Neu:** `layers/LAYER-4.md`

**Inhalt:**
- Automatische Projekt-Initialisierung
- Issue Label → Agent Mapping
- Projekt-Slot Management (A/B/C)
- GitHub Issue Commenting

**Gilt für:** Lazy Bird autonome Tasks

---

## 📊 Architektur-Nummerierung

### Alt: "4-Layer System"

```
Layer 4: Lazy Bird
Layer 3: Rover
Layer 2: AI CLIs
Layer 1: MCP Servers
```

### Neu: "5-Layer System (0-4)"

```
Layer 4: Lazy Bird Automation
Layer 3: Rover Orchestration
Layer 2: AI CLI (Claude/Gemini/Copilot)
Layer 1: MCP Server Usage
Layer 0: Universal Standards (BASIS)
```

**Änderung:** Layer 0 hinzugefügt als Basis!

**Dokumentationen die aktualisiert werden müssen:**
- [x] `README.md` - Architektur-Diagramm
- [x] `lazy-bird/README.md` - Layer-Beschreibung
- [x] `docs/LAZY-BIRD-ARCHITECTURE.md` - Technische Architektur
- [x] `docs/LAZY-BIRD-SETUP-DE.md` - Setup-Guide
- [x] `docs/LAZY-BIRD-SETUP-EN.md` - Setup-Guide

---

## 🔧 Wie Guidelines jetzt geladen werden

### Vorher (Manuell)

Jeder Agent musste manuell alle Guidelines lesen:

```python
# ❌ ALT: Manuell alle Guidelines laden
claude_guidelines = read("claude-guidelines.md")
project_structure = read("PROJECT-STRUCTURE.md")

# Problem: Duplikation, keine Hierarchie
```

### Jetzt (Automatisch)

Guideline Injector lädt automatisch basierend auf Layer:

```python
# ✅ NEU: Automatische hierarchische Ladung
from guideline_injector import GuidelineInjector

injector = GuidelineInjector()

# Beispiel: Claude Code direkt (Layer 2)
guidelines = injector.get_guidelines_for_layer(
    layer=2,
    agent="claude"
)

# Lädt automatisch:
# - LAYER-0 (Universal)
# - LAYER-1 (MCP Servers)
# - LAYER-2 (AI CLI)
# - LAYER-2-CLAUDE (Claude-spezifisch)
```

---

## ✅ Vererbungs-Logik

### Prinzip: "Erweitert, nicht überschreibt"

```python
# Layer 0: Basis (IMMER geladen)
LAYER_0 = {
    "project_structure": "src/tests/docs",
    "naming": "snake_case/camelCase",
    "security": "input_validation"
}

# Layer 1: Erweitert Layer 0
LAYER_1 = {
    **LAYER_0,  # Erbt alles von Layer 0
    "mcp_servers": "18 servers available",
    "rate_limits": "respect limits"
}

# Layer 2: Erweitert Layer 1
LAYER_2 = {
    **LAYER_1,  # Erbt alles von Layer 1 (+ Layer 0)
    "tools": "Read/Write/Edit/Bash",
    "commits": "conventional format"
}

# Layer 2-CLAUDE: Erweitert Layer 2
LAYER_2_CLAUDE = {
    **LAYER_2,  # Erbt alles von Layer 2 (+ Layer 1 + Layer 0)
    "security_first": True,
    "test_coverage": "80%+"
}
```

**Ergebnis:** Keine Duplikation, klare Hierarchie!

---

## 📝 Update-Checkliste

### Für Entwickler

- [ ] Alte Guidelines in `legacy/` verschoben
- [ ] Neue Layer-Guidelines gelesen
- [ ] `guideline-injector.py` verstanden
- [ ] Lokale Scripts updated (falls vorhanden)

### Für Dokumentation

- [ ] README.md - Architektur von "4-Layer" → "5-Layer (0-4)"
- [ ] lazy-bird/README.md - Layer-Beschreibungen
- [ ] LAZY-BIRD-ARCHITECTURE.md - Technische Details
- [ ] LAZY-BIRD-SETUP-DE.md - Setup-Anleitung
- [ ] LAZY-BIRD-SETUP-EN.md - Setup-Anleitung

### Für Integration

- [ ] Claude Code: `.claude/settings.json` erweitern
- [ ] Rover: System Prompt mit Guideline Injection
- [ ] Lazy Bird: Issue Watcher updated

---

## 🚀 Nächste Schritte

1. **Alte Guidelines archivieren**
   ```bash
   mv lazy-bird/guidelines/*.md lazy-bird/guidelines/legacy/
   ```

2. **Neue Guidelines nutzen**
   ```python
   from guideline_injector import GuidelineInjector
   injector = GuidelineInjector()
   guidelines = injector.get_guidelines_for_layer(layer=2, agent="claude")
   ```

3. **Dokumentationen aktualisieren**
   - Siehe Update-Checkliste oben

4. **Testing**
   ```bash
   cd lazy-bird/guidelines/tools
   python guideline-injector.py
   ```

---

## ❓ FAQ

### Warum Layer 0-4 statt 1-5?

**Antwort:** Layer 0 ist die BASIS (Universal Standards). Alle anderen Layer bauen darauf auf. So ist klar dass Layer 0 IMMER geladen wird, unabhängig vom darüber liegenden Layer.

### Muss ich alle alten Guidelines löschen?

**Antwort:** Nein! Sie sind in `legacy/` zur Referenz. Aber nutze NUR die neuen Layer-Guidelines!

### Was wenn ich einen neuen Agent hinzufüge?

**Antwort:** Erstelle einfach `LAYER-2-NEUERAGENT.md` und der Injector erkennt ihn automatisch!

### Wie teste ich ob alles richtig geladen wird?

**Antwort:**
```bash
cd lazy-bird/guidelines/tools
python guideline-injector.py

# Zeigt was für jeden Layer geladen wird
```

---

**Migration abgeschlossen!** 🎉

Alle neuen Features nutzen jetzt das hierarchische Layer-System.
