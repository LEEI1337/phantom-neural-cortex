# 🚀 Schnellstart-Anleitung

**Dein AI-Entwicklungs-Setup in 5 Minuten.**

---

## Voraussetzungen

- Node.js 18+
- Docker Desktop
- Git
- API Keys (GitHub Token erforderlich, Rest optional)

---

## Installation

```bash
# 1. Klonen
git clone https://github.com/LEEI1337/ai-dev-orchestrator.git
cd ai-dev-orchestrator

# 2. Environment Setup
cp .env.example .env
# .env mit deinen API Keys bearbeiten

# 3. CLIs installieren (wähle was du brauchst)
npm install -g @anthropic-ai/claude-code      # $20/Monat
npm install -g @google/generative-ai-cli      # KOSTENLOS
npm install -g @github/copilot-cli            # KOSTENLOS oder $10/Monat
npm install -g @endorhq/rover                 # KOSTENLOS

# 4. Rover initialisieren
git init  # falls nötig
rover init .
```

---

## Erste Schritte

### Teste Gemini (KOSTENLOS)
```bash
gemini "Hallo, teste ob du funktionierst"
```

### Teste Rover Parallel Execution
```bash
rover task "Liste alle Markdown-Dateien" --agent gemini
rover ls
```

### Teste Claude Agent
```bash
claude "@code-expert review README.md"
```

---

## Kosten-Optimierung

**Minimum Setup:** $20/Monat
- Claude Pro: $20 (erforderlich)
- Gemini: KOSTENLOS (1000/Tag)
- Copilot: KOSTENLOS (Free Tier)

**Optimal Setup:** $30/Monat
- Claude Pro: $20
- Gemini: KOSTENLOS
- Copilot Pro: $10

**Strategie:** Maximiere Free Tiers (Gemini + Copilot kostenlos)

---

## Setup Verifizieren

```bash
# Alle Tools prüfen
claude --version
gemini --version
copilot --version
rover --version

# MCP Server prüfen
ls .mcp.json
```

---

## Nächste Schritte

1. **[Architektur](architecture/ARCHITECTURE.md)** - 3-Ebenen-System verstehen
2. **[AI Selector](guides/ROVER-AI-SELECTOR.md)** - Welche AI für welche Aufgabe
3. **[Kosten-Guide](OPTIMIZATION-SUMMARY.md)** - Monatliche Kosten optimieren

---

## Häufige Probleme

**"Rover not found"**
```bash
npm install -g @endorhq/rover
```

**"Git not initialized"**
```bash
git init
git config user.email "du@example.com"
git config user.name "Dein Name"
```

**"MCP servers not loading"**
- Prüfe ob `.mcp.json` existiert
- Verifiziere API Keys in `.env`
- Starte Claude Code neu

---

**Brauchst du Hilfe?** Öffne ein [Issue](https://github.com/LEEI1337/ai-dev-orchestrator/issues)
