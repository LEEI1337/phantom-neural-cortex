# 🏗️ Hierarchisches Layer-Guideline-System

**Ziel:** Jeder Layer hat seine eigenen Anweisungen, Guidelines werden intelligent vererbt ohne Duplikation.

---

## 📊 Layer-Architektur

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 4: LAZY BIRD (Automatisierung)                        │
│ - Issue → Projekt Mapping                                   │
│ - Automatische Projekt-Initialisierung                      │
│ - Agent-Auswahl basierend auf Labels                        │
│ Guidelines: LAYER-4.md (erbt von Layer 3)                   │
└─────────────────────────────────────────────────────────────┘
                          ↓ ruft auf
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: ROVER (Task-Orchestrierung)                        │
│ - Git Worktree Isolation                                    │
│ - Docker Container Management                               │
│ - Multi-Agent Koordination                                  │
│ Guidelines: LAYER-3.md (erbt von Layer 2)                   │
└─────────────────────────────────────────────────────────────┘
                          ↓ ruft auf
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: AI CLI (Claude Code, Gemini CLI, Copilot CLI)      │
│ - Direkter Chat mit User oder Rover                         │
│ - Code-Generierung                                          │
│ - Tool Usage (Read, Write, Bash, etc.)                      │
│ Guidelines: LAYER-2.md (erbt von Layer 1)                   │
│                                                              │
│ Agent-Spezifisch:                                           │
│ - LAYER-2-CLAUDE.md                                         │
│ - LAYER-2-GEMINI.md                                         │
│ - LAYER-2-COPILOT.md                                        │
└─────────────────────────────────────────────────────────────┘
                          ↓ verwendet
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: MCP SERVERS (Tools & Daten)                        │
│ - Filesystem, Git, Docker, Brave Search, etc.               │
│ - 18 MCP Server mit spezialisierten Tools                   │
│ Guidelines: LAYER-1.md (erbt von Layer 0)                   │
└─────────────────────────────────────────────────────────────┘
                          ↓ basiert auf
┌─────────────────────────────────────────────────────────────┐
│ LAYER 0: UNIVERSAL STANDARDS (Basis für ALLES)              │
│ - Projekt-Struktur (src/, tests/, docs/)                    │
│ - Naming Conventions                                        │
│ - Code Quality Standards                                    │
│ - Security Basics                                           │
│ Guidelines: LAYER-0.md (BASIS - keine Vererbung)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Vererbungs-Hierarchie

### Prinzip: "Erweitert, nicht überschreibt"

Jeder Layer:
1. **Erbt** alle Guidelines der darunter liegenden Layer
2. **Erweitert** mit layer-spezifischen Anweisungen
3. **Überschreibt NICHT** (nur bei explizitem Konflikt)

### Beispiel: Claude Code CLI (Layer 2)

**Bekommt automatisch:**
```
LAYER-0.md (Universal Standards)
    ↓
LAYER-1.md (MCP Server Usage)
    ↓
LAYER-2.md (AI CLI General)
    ↓
LAYER-2-CLAUDE.md (Claude-spezifisch)
```

**Wenn Claude Code DIREKT vom User verwendet wird:**
- Liest: `LAYER-0 → LAYER-1 → LAYER-2 → LAYER-2-CLAUDE`
- Befolgt ALLE diese Guidelines

**Wenn Claude Code von ROVER aufgerufen wird:**
- Rover injiziert zusätzlich: `LAYER-3` (Rover-spezifisch)
- Claude befolgt: `LAYER-0 → LAYER-1 → LAYER-2 → LAYER-2-CLAUDE → LAYER-3`

**Wenn Claude Code von LAZY BIRD aufgerufen wird:**
- Lazy Bird injiziert: `LAYER-3 + LAYER-4`
- Claude befolgt: `LAYER-0 → LAYER-1 → LAYER-2 → LAYER-2-CLAUDE → LAYER-3 → LAYER-4`

---

## 📋 Guideline-Dateien

### Layer 0 - Universal (Basis)
```
lazy-bird/guidelines/layers/LAYER-0.md
```
**Inhalt:**
- Projekt-Struktur Standards
- Naming Conventions (Python, TypeScript, etc.)
- Code Quality Basics
- Security Fundamentals
- Testing Basics

**Für:** JEDEN Agent, JEDEN Layer, JEDES Projekt

---

### Layer 1 - MCP Servers
```
lazy-bird/guidelines/layers/LAYER-1.md
```
**Inhalt:**
- Welche MCP Server verfügbar sind
- Wie man sie verwendet
- Tool-spezifische Best Practices
- Rate Limits beachten

**Erweitert:** LAYER-0
**Für:** AI CLIs die MCP Server verwenden

---

### Layer 2 - AI CLI
```
lazy-bird/guidelines/layers/LAYER-2.md          (General)
lazy-bird/guidelines/layers/LAYER-2-CLAUDE.md   (Claude-spezifisch)
lazy-bird/guidelines/layers/LAYER-2-GEMINI.md   (Gemini-spezifisch)
lazy-bird/guidelines/layers/LAYER-2-COPILOT.md  (Copilot-spezifisch)
```

**LAYER-2.md Inhalt:**
- Tool Usage (Read, Write, Edit, Bash)
- Commit Message Format
- PR Creation
- User Interaction Patterns

**LAYER-2-CLAUDE.md Inhalt:**
- Claude-spezifische Features
- Artifacts Usage
- Extended thinking
- Claude Code CLI specifics

**Erweitert:** LAYER-0 + LAYER-1
**Für:** Direkte CLI Nutzung oder Rover-Aufrufe

---

### Layer 3 - Rover
```
lazy-bird/guidelines/layers/LAYER-3.md
```
**Inhalt:**
- Git Worktree Management
- Docker Container Regeln
- Isolation Requirements
- Test Validation vor Merge
- Rover CLI Command Format

**Erweitert:** LAYER-0 + LAYER-1 + LAYER-2
**Für:** Rover-orchestrierte Tasks

---

### Layer 4 - Lazy Bird
```
lazy-bird/guidelines/layers/LAYER-4.md
```
**Inhalt:**
- Automatische Projekt-Initialisierung
- Issue Label → Agent Mapping
- Projekt-Slot Management (A/B/C)
- GitHub Issue Commenting Format
- Multi-Projekt Koordination

**Erweitert:** LAYER-0 + LAYER-1 + LAYER-2 + LAYER-3
**Für:** Lazy Bird autonome Tasks

---

## 🔧 Guideline Injection Mechanismus

### Option 1: File Concatenation (Einfach)

```python
def get_guidelines_for_layer(layer: int, agent: str = None) -> str:
    """
    Lade alle Guidelines für einen Layer.

    Args:
        layer: Layer number (0-4)
        agent: Optional agent name (claude, gemini, copilot)

    Returns:
        Concatenated guidelines
    """
    guidelines = []

    # Layer 0 (immer)
    guidelines.append(read_file("layers/LAYER-0.md"))

    # Layer 1+ (je nach layer)
    if layer >= 1:
        guidelines.append(read_file("layers/LAYER-1.md"))

    if layer >= 2:
        guidelines.append(read_file("layers/LAYER-2.md"))

        # Agent-spezifisch
        if agent:
            guidelines.append(read_file(f"layers/LAYER-2-{agent.upper()}.md"))

    if layer >= 3:
        guidelines.append(read_file("layers/LAYER-3.md"))

    if layer >= 4:
        guidelines.append(read_file("layers/LAYER-4.md"))

    return "\n\n---\n\n".join(guidelines)
```

### Option 2: System Prompt Injection (Optimal)

```python
def inject_guidelines(layer: int, agent: str, base_prompt: str) -> str:
    """
    Injiziere Guidelines in System Prompt.

    Args:
        layer: Layer number
        agent: Agent name
        base_prompt: Basis System Prompt

    Returns:
        Erweiterter System Prompt
    """
    guidelines = get_guidelines_for_layer(layer, agent)

    enhanced_prompt = f"""
{base_prompt}

# GUIDELINES (Layer {layer} - {agent.upper()})

Du befindest dich in Layer {layer} der AI Development Architektur.
Befolge ALLE folgenden Guidelines in dieser Reihenfolge:

{guidelines}

**WICHTIG:**
- Diese Guidelines bauen aufeinander auf (Layer 0 → {layer})
- Spätere Guidelines erweitern frühere, überschreiben sie NICHT
- Bei Konflikt hat die höchste Layer-Nummer Vorrang
"""

    return enhanced_prompt
```

---

## 💡 Verwendungs-Beispiele

### Beispiel 1: Direkter Claude Code CLI Aufruf

```bash
# User startet Claude Code direkt
claude-code chat

# System lädt:
guidelines = get_guidelines_for_layer(
    layer=2,        # AI CLI Layer
    agent="claude"  # Claude-spezifisch
)

# Claude bekommt:
# - LAYER-0.md (Universal)
# - LAYER-1.md (MCP Servers)
# - LAYER-2.md (AI CLI)
# - LAYER-2-CLAUDE.md (Claude-spezifisch)
```

### Beispiel 2: Rover ruft Claude auf

```bash
# Rover startet Task
rover task "Add authentication" --agent claude

# Rover injiziert:
guidelines = get_guidelines_for_layer(
    layer=3,        # Rover Layer
    agent="claude"
)

# Claude bekommt:
# - LAYER-0.md (Universal)
# - LAYER-1.md (MCP Servers)
# - LAYER-2.md (AI CLI)
# - LAYER-2-CLAUDE.md (Claude-spezifisch)
# - LAYER-3.md (Rover-spezifisch) ← NEU!
```

### Beispiel 3: Lazy Bird → Rover → Gemini

```python
# Lazy Bird erkennt Issue
issue_watcher.process_issue(issue)

# Lazy Bird injiziert:
guidelines = get_guidelines_for_layer(
    layer=4,        # Lazy Bird Layer
    agent="gemini"
)

# Gemini bekommt:
# - LAYER-0.md (Universal)
# - LAYER-1.md (MCP Servers)
# - LAYER-2.md (AI CLI)
# - LAYER-2-GEMINI.md (Gemini-spezifisch)
# - LAYER-3.md (Rover-spezifisch)
# - LAYER-4.md (Lazy Bird-spezifisch) ← NEU!
```

---

## 📁 Datei-Organisation

```
lazy-bird/guidelines/
├── LAYER-SYSTEM.md              # Diese Datei (Übersicht)
│
├── layers/                       # Layer-spezifische Guidelines
│   ├── LAYER-0.md               # Universal Standards (BASIS)
│   ├── LAYER-1.md               # MCP Server Usage
│   ├── LAYER-2.md               # AI CLI General
│   ├── LAYER-2-CLAUDE.md        # Claude-spezifisch
│   ├── LAYER-2-GEMINI.md        # Gemini-spezifisch
│   ├── LAYER-2-COPILOT.md       # Copilot-spezifisch
│   ├── LAYER-3.md               # Rover Orchestration
│   └── LAYER-4.md               # Lazy Bird Automation
│
├── legacy/                       # Alte Guidelines (zur Migration)
│   ├── PROJECT-STRUCTURE.md     # → wird zu LAYER-0.md
│   ├── claude-guidelines.md     # → wird zu LAYER-2-CLAUDE.md
│   ├── gemini-guidelines.md     # → wird zu LAYER-2-GEMINI.md
│   └── copilot-guidelines.md    # → wird zu LAYER-2-COPILOT.md
│
└── tools/
    └── guideline-injector.py    # Utility zur Guideline-Injektion
```

---

## 🔄 Migration Plan

### Schritt 1: Alte Guidelines aufteilen

```bash
# PROJECT-STRUCTURE.md → LAYER-0.md
# - Universal Standards extrahieren
# - Projekt-Struktur Regeln
# - Naming Conventions

# claude-guidelines.md → LAYER-2-CLAUDE.md
# - Claude-spezifische Anweisungen
# - Universal Parts → LAYER-0.md verschieben

# gemini-guidelines.md → LAYER-2-GEMINI.md
# - Gemini-spezifische Anweisungen
# - Universal Parts → LAYER-0.md verschieben

# copilot-guidelines.md → LAYER-2-COPILOT.md
# - Copilot-spezifische Anweisungen
# - Universal Parts → LAYER-0.md verschieben
```

### Schritt 2: Neue Layer Guidelines erstellen

- LAYER-1.md (MCP Server Usage)
- LAYER-2.md (AI CLI General)
- LAYER-3.md (Rover Orchestration)
- LAYER-4.md (Lazy Bird Automation)

### Schritt 3: Guideline Injector implementieren

```python
# lazy-bird/guidelines/tools/guideline-injector.py
# - get_guidelines_for_layer()
# - inject_guidelines()
# - validate_guidelines()
```

### Schritt 4: Integration

- Claude Code CLI: `.claude/settings.json` erweitern
- Rover: System Prompt Injection
- Lazy Bird: Rover Aufruf mit Guidelines

---

## ✅ Vorteile

1. **Keine Duplikation**
   - Universal Standards nur in LAYER-0
   - Jeder Layer nur seine spezifischen Anweisungen

2. **Flexibel**
   - Direkter CLI Aufruf: Nur notwendige Layer
   - Rover Aufruf: + Layer 3
   - Lazy Bird: + Layer 4

3. **Wartbar**
   - Änderung in LAYER-0 → Gilt für ALLE
   - Änderung in LAYER-2-CLAUDE → Nur Claude betroffen

4. **Erweiterbar**
   - Neuer Layer? Einfach LAYER-5.md hinzufügen
   - Neuer Agent? LAYER-2-NEUERAGENT.md erstellen

5. **Transparent**
   - Agent weiß IMMER welche Layer aktiv sind
   - Klare Hierarchie

---

**Nächster Schritt:** Layer-spezifische Guidelines erstellen! 🚀
