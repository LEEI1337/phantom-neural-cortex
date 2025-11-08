# 🤖 Lazy Bird Integration - Einrichtungsanleitung (Deutsch)

> **Autonomer Workflow: GitHub Issue → Implementierung → PR**  
> Layer 4 (Automatisierung) über Rover für vollautomatische Entwicklung

---

## 📋 Inhaltsverzeichnis

- [Überblick](#überblick)
- [Architektur](#architektur)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Fehlerbehebung](#fehlerbehebung)
- [Kostenoptimierung](#kostenoptimierung)

---

## Überblick

**Lazy Bird** ist eine autonome Orchestrierungsebene, die **über Rover** liegt und ein 4-Schicht-KI-Entwicklungssystem erstellt:

```
┌─────────────────────────────────────────┐
│  EBENE 4: LAZY BIRD (Automatisierung)   │
│  • Überwacht GitHub/GitLab Issues       │
│  • Startet Rover-Tasks automatisch      │
│  • Verwaltet Multi-Projekt-Workflows    │
│  • Führt Test-Validierung & Wiederholungen durch │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  EBENE 3: ROVER (Task-Orchestrierung)   │
│  • Erstellt isolierte Git-Worktrees     │
│  • Verwaltet Docker-Container           │
│  • Führt KI-Agenten-Tasks aus           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  EBENE 2: KI-CLIs (Isoliert)            │
│  ┌──────┬──────┬──────┐                 │
│  │Claude│Gemini│Copilot                 │
│  └──────┴──────┴──────┘                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  EBENE 1: MCP-SERVERS (Geteilt)         │
│  18 Server mit Tools & Daten            │
└─────────────────────────────────────────┘
```

### Hauptvorteile

- ✅ **20-100 Stunden/Monat sparen** bei sich wiederholenden Entwicklungsaufgaben
- ✅ **Autonomes Arbeiten** während Ihrer Abwesenheit (morgens Issue → abends Merge)
- ✅ **Nutzung von Rover** Isolation & Multi-KI-Orchestrierung
- ✅ **Test-gesteuerte Validierung** vor PR-Erstellung
- ✅ **Automatische Wiederholungen** bei Test-Fehlern
- ✅ **Kostenoptimiert** - 60-70% der Tasks laufen KOSTENLOS

---

## Architektur

### Komponenteninteraktionen

```
GitHub Issue (Label: "lazy-bird")
    ↓
Issue Watcher (prüft alle 60s)
    ↓
Agent Selector (wählt Claude/Gemini/Copilot)
    ↓
Rover Adapter (übersetzt zu Rover CLI)
    ↓
Rover erstellt Worktree + Container
    ↓
KI-Agent implementiert Task
    ↓
Test Coordinator validiert
    ↓
Rover merged oder wiederholt
    ↓
GitHub PR automatisch erstellt
```

### Hauptkomponenten

| Komponente | Datei | Zweck |
|-----------|------|---------|
| **Issue Watcher** | `issue-watcher.py` | Prüft GitHub auf gelabelte Issues |
| **Agent Selector** | `agent-selector.py` | Wählt optimalen KI-Agenten (kostenoptimiert) |
| **Rover Adapter** | `rover-adapter.py` | Übersetzt Tasks zu Rover CLI-Befehlen |
| **Project Manager** | `project-manager.py` | Multi-Projekt-Konfiguration |

---

## Voraussetzungen

### Systemanforderungen

- **OS:** Linux (Ubuntu 20.04+) oder WSL2
- **RAM:** 16GB minimum (für Multi-Projekt)
- **Docker:** Desktop oder Podman
- **Node.js:** 22+
- **Python:** 3.10+

### Erforderliche Software

```bash
# 1. Node.js und npm installieren
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. Docker installieren
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 3. Python-Abhängigkeiten installieren
sudo apt-get install -y python3 python3-pip

# 4. Rover CLI installieren
npm install -g @endorhq/rover

# 5. KI-CLIs installieren
npm install -g @anthropic-ai/claude-code    # Claude (optional)
npm install -g @github/copilot-cli          # Copilot
npm install -g @google/generative-ai-cli    # Gemini
```

### Erforderliche API-Schlüssel

1. **GitHub Personal Access Token** (erforderlich)
   - Gehen Sie zu: https://github.com/settings/tokens
   - Erstellen Sie Token mit `repo`, `workflow`, `write:discussion` Scopes
   - Export: `export GITHUB_TOKEN=ghp_xxxxx`

2. **Google Gemini API Key** (kostenloses Tier)
   - Erhalten Sie von: https://ai.google.dev/
   - 1000 kostenlose Anfragen/Tag
   - Export: `export GOOGLE_API_KEY=xxxxx`

3. **Anthropic Claude API** (optional, $20/Monat)
   - Nur für Expertenaufgaben benötigt
   - Erhalten Sie von: https://console.anthropic.com/

4. **GitHub Copilot** (kostenloses Tier oder $10/Monat)
   - Kostenloses Tier: 2000 Vervollständigungen/Monat
   - Pro: Unbegrenzt

---

## Installation

### Schritt 1: Repository klonen

```bash
cd /workspace
git clone https://github.com/LEEI1337/ai-dev-orchestrator.git
cd ai-dev-orchestrator
```

### Schritt 2: Umgebung einrichten

```bash
# Umgebungsvorlage kopieren
cp .env.example .env

# Mit Ihren API-Schlüsseln bearbeiten
nano .env
```

Fügen Sie folgendes zu `.env` hinzu:

```bash
# GitHub (Erforderlich)
GITHUB_TOKEN=ghp_ihr_token_hier

# Google Gemini (Kostenloses Tier - Empfohlen)
GOOGLE_API_KEY=ihr_gemini_schlüssel_hier

# Anthropic Claude (Optional - $20/Monat)
ANTHROPIC_API_KEY=sk-ant-ihr_schlüssel_hier

# GitHub Copilot (Optional - Kostenlos/$10)
# Verwendet GitHub-Authentifizierung
```

### Schritt 3: Projekte konfigurieren

Bearbeiten Sie `lazy-bird/configs/projects.json` um Ihre Projekte hinzuzufügen:

```json
{
  "projects": [
    {
      "id": "mein-projekt",
      "name": "Mein Tolles Projekt",
      "type": "python",
      "path": "/workspace/mein-projekt",
      "repo": "https://github.com/benutzer/mein-projekt",
      "branch": "main",
      "rover_enabled": true,
      "settings": {
        "test_command": "pytest tests/ -v",
        "build_command": "python -m build",
        "lint_command": "ruff check .",
        "default_agent": "gemini",
        "max_retries": 3,
        "timeout_minutes": 30
      },
      "labels": {
        "watch": "lazy-bird",
        "ready": "bereit-zur-implementierung"
      }
    }
  ]
}
```

### Schritt 4: Python-Abhängigkeiten installieren

```bash
cd lazy-bird/scripts
pip3 install requests  # Für GitHub API
```

### Schritt 5: Konfiguration testen

```bash
# Projekt-Manager testen
python3 project-manager.py

# Agent-Selector testen
python3 agent-selector.py
```

---

## Konfiguration

### Agent-Auswahlregeln

Bearbeiten Sie `lazy-bird/configs/rover-mapping.json` um KI-Agenten-Routing anzupassen:

```json
{
  "label_rules": [
    {
      "labels": ["security", "architecture", "complex"],
      "agent": "claude",
      "cost_level": "high"
    },
    {
      "labels": ["documentation", "bulk-refactor", "large-scale"],
      "agent": "gemini",
      "cost_level": "free"
    },
    {
      "labels": ["github-workflow", "quick-fix", "pr"],
      "agent": "copilot",
      "cost_level": "free-low"
    }
  ],
  "fallback_agent": "gemini"
}
```

### Systemd-Service (Optional)

Für Produktions-Deployment, führen Sie Lazy Bird als System-Service aus:

```bash
# Service-Datei kopieren
sudo cp lazy-bird/systemd/lazy-bird-watcher.service /etc/systemd/system/

# Service-Datei mit Ihren Pfaden und Anmeldedaten bearbeiten
sudo nano /etc/systemd/system/lazy-bird-watcher.service

# Service aktivieren und starten
sudo systemctl daemon-reload
sudo systemctl enable lazy-bird-watcher
sudo systemctl start lazy-bird-watcher

# Status prüfen
sudo systemctl status lazy-bird-watcher

# Logs anzeigen
sudo journalctl -u lazy-bird-watcher -f
```

---

## Verwendung

### Manueller Modus (Entwicklung)

```bash
# Zum Scripts-Verzeichnis navigieren
cd lazy-bird/scripts

# Umgebungsvariablen setzen
export GITHUB_TOKEN=ghp_xxxxx

# Issue Watcher manuell ausführen
python3 issue-watcher.py
```

Sie sehen Ausgaben wie:

```
🚀 Lazy Bird Issue Watcher gestartet
📊 Überwacht 1 Projekte
⏱️  Prüfintervall: 60s

[10:15:30] Prüfe GitHub Issues...
  ✅ ai-orchestrator: 2 neue Issue(s)

🎯 Verarbeite Issue #42: Benutzerauthentifizierung hinzufügen
   Labels: feature, security
   Agent: claude
   ✅ Rover-Task erstellt: task-abc123
```

### Automatisierter Modus (Produktion)

Sobald der Systemd-Service konfiguriert ist:

```bash
# Service läuft automatisch im Hintergrund
sudo systemctl status lazy-bird-watcher
```

### Automatisierte Issues erstellen

1. **GitHub Issue erstellen** mit klarer Beschreibung
2. **Label hinzufügen:** `lazy-bird` (oder Ihr konfiguriertes Watch-Label)
3. **Optional Agenten-Hinweise hinzufügen:**
   - `security` → Leitet zu Claude (Experte)
   - `documentation` → Leitet zu Gemini (kostenlos)
   - `github-workflow` → Leitet zu Copilot (GitHub-Spezialist)
4. **Warten** - Issue Watcher erfasst es innerhalb von 60 Sekunden
5. **Überwachen** - Prüfen Sie Issue-Kommentare für Fortschrittsupdates
6. **PR überprüfen** - Mergen wenn bereit!

---

## Fehlerbehebung

### Problem: Watcher erkennt Issues nicht

**Lösung:**
```bash
# GitHub-Token prüfen
echo $GITHUB_TOKEN

# Token-Berechtigungen verifizieren
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/user

# Projektkonfiguration prüfen
python3 project-manager.py
```

### Problem: Rover-Befehle schlagen fehl

**Lösung:**
```bash
# Rover-Installation verifizieren
rover --version

# Docker-Status prüfen
docker ps

# Rover manuell testen
rover task "test task" --agent gemini
```

### Problem: Hohe Kosten (zu viel Claude-Nutzung)

**Lösung:**
```bash
# Agenten-Nutzungsstatistiken prüfen
python3 agent-selector.py

# Label-Regeln in rover-mapping.json überprüfen
# Mehr Tasks zu Gemini (kostenloses Tier) leiten
```

---

## Kostenoptimierung

### Zielverteilung

```
Gemini (KOSTENLOS):  60-70% der Tasks
Copilot (KOSTENLOS): 20-30% der Tasks  
Claude ($20):        10-20% der Tasks
────────────────────────────────────────
Gesamt: $20-30/Monat
```

### Optimierungstipps

1. **Gemini verwenden für:**
   - Dokumentationserstellung
   - Bulk-Refactoring
   - Großangelegte Analysen
   - Nicht-kritische Features

2. **Copilot verwenden für:**
   - GitHub-Workflow-Updates
   - Schnelle Bugfixes
   - PR-Reviews
   - CI/CD-Änderungen

3. **Claude verwenden für:**
   - Sicherheitsaudits
   - Architekturdesign
   - Komplexes Debugging
   - Kritische Features

4. **Nutzung überwachen:**
   ```bash
   # Agenten-Auswahlstatistiken prüfen
   python3 agent-selector.py
   ```

### Kostenbeispiele

**Dokumentations-Sprint** (100% KOSTENLOS!)
```
API-Docs für 200 Endpoints generieren → Gemini
Benutzerhandbuch erstellen → Gemini
Code-Beispiele generieren → Gemini
Gesamt: $0 (alles kostenloses Tier)
```

**Feature-Entwicklung** (~$1 von Ihrem $20-Abonnement)
```
Impact analysieren → Gemini ($0)
Architektur designen → Claude (~$0.50)
30 Komponenten implementieren → Gemini ($0)
Sicherheitsreview → Claude (~$0.50)
PR erstellen → Copilot ($0)
```

---

## Nächste Schritte

1. ✅ **Mit einfachem Issue testen** - Starten Sie mit Dokumentationsaufgabe
2. ✅ **Ersten Lauf überwachen** - Logs und Issue-Kommentare beobachten
3. ✅ **PR überprüfen** - Qualität des generierten Codes prüfen
4. ✅ **Schrittweise skalieren** - Mehr Projekte hinzufügen, wenn Vertrauen wächst
5. ✅ **Kosten optimieren** - Agenten-Nutzung überprüfen und Labels anpassen

---

## Support

- **Dokumentation:** [Lazy Bird Architektur](LAZY-BIRD-ARCHITECTURE.md)
- **Issues:** [GitHub Issues](https://github.com/LEEI1337/ai-dev-orchestrator/issues)
- **Diskussionen:** [GitHub Discussions](https://github.com/LEEI1337/ai-dev-orchestrator/discussions)

---

**Mit ❤️ von Entwicklern für Entwickler in Österreich 🇦🇹**
