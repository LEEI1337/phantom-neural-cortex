# Phantom Agent System — Technische Dokumentation

> **Version:** 1.0.0 | **Datum:** 2026-03-07 | **Status:** Implementiert
> **Repo:** `LEEI1337/phantom-neural-cortex` | **Autor:** LEEI1337 / AI Engineering

---

## 1. Ueberblick

Das Phantom Agent System vereint vier Kernsysteme zu einem deploybaren AI-Mitarbeiter:

| System | Port | Funktion |
|--------|------|----------|
| **PNC** (Phantom Neural Cortex) | :18789 | Orchestrierung, Gateway, Swarm Intelligence |
| **NSS** (Neural Security System) | :11337-11339 | 6-Layer Security, DSGVO, EU AI Act |
| **echo_log** (Voice Gateway) | :8085 | 42 Tools, RAG, Reasoning, Tool-Calling |
| **Mattermost Bridge** | :8065 | Team-Kommunikation (Jak Bot Pattern) |

### Architektur-Prinzip: HRM (Hierarchical Reasoning Model)

```
Komplexe Aufgabe
    |
    v
[HRM Router] --> Komplexitaet bewerten (Score 0.0 - 1.0)
    |                    |
    v                    v
[HIGH: Planner]    [LOW: Executor]
Cloud LLM           Ollama lokal
(Opus/Codex)        (mistral-small3.2)
    |                    |
    v                    v
Plan-Steps         Direkte Ausfuehrung
    |               via echo_log /chat
    v
[Executor] --> echo_log Tools
    |
    v
[Feedback Loop] --> Bei Failure zurueck zum Planner
```

---

## 2. Komponenten

### 2.1 HRM Controller (`hrm/`)

**Dateien:**
- `hrm/router.py` — Komplexitaetsbewertung + Modell-Routing
- `hrm/planner.py` — Plan-Erstellung via Cloud LLM
- `hrm/executor.py` — Step-Ausfuehrung via Ollama + echo_log

**Komplexitaets-Bewertung (`router.py`):**

| Signal | Score-Aenderung |
|--------|-----------------|
| High-Complexity Keywords (architect, debug, refactor...) | +0.08 pro Treffer |
| Low-Complexity Keywords (status, check, list...) | -0.06 pro Treffer |
| Multi-Step Erkennung (1., 2., dann, danach...) | +0.1 bis +0.2 |
| Laenge > 100 Woerter | +0.15 |
| Code-Keywords (class, function, import) | +0.1 |

**Schwellwerte:**
- `>= 0.6` → HIGH → Planner (Cloud LLM)
- `>= 0.35` → MEDIUM → Executor (Ollama)
- `< 0.35` → LOW → Executor (Ollama)

**Planner (`planner.py`):**
- Nimmt komplexe Aufgabe, erstellt JSON-Plan mit Steps
- Jeder Step hat: `step_id`, `description`, `tool`, `tool_args`, `depends_on`
- Verfuegbare Tools: file_read, file_write, shell_exec, http_request, docker_status, mattermost_send, knowledge_search, git_status, deploy
- Bei Failure: `refine_plan()` mit Feedback → verbesserter Plan

**Executor (`executor.py`):**
- Fuehrt Steps sequentiell aus (respektiert `depends_on`)
- NSS Security Check vor jedem Step
- Fallback-Chain: `mistral-small3.2` → `llama3.1:8b`
- Eskalation bei kritischem Failure → zurueck zum Planner

### 2.2 Integration Layer (`integrations/`)

**NSS Client (`nss_client.py`):**

| Methode | NSS Service | Port | Funktion |
|---------|-------------|------|----------|
| `check_risk()` | Guardian / MARS | :11338 | Risk Scoring (0-1, Tier 0-3) |
| `check_injection()` | Guardian / SENTINEL | :11338 | Injection Defense |
| `check_tool_safety()` | Guardian / VIGIL | :11338 | Tool CIA Check |
| `enhance_prompt()` | Guardian / SHIELD | :11338 | Prompt Safety |
| `redact_pii()` | Gateway | :11337 | PII Redaction |
| `check_privacy_budget()` | Governance | :11339 | DSGVO Privacy Budget |
| `check_policy()` | Governance | :11339 | Policy Engine Check |

Alle Methoden haben Graceful Degradation — wenn NSS offline ist, wird auf SAFE defaulted.

**echo_log Client (`echoLog_client.py`):**

| Methode | Endpoint | Funktion |
|---------|----------|----------|
| `chat()` | POST /chat | Chat mit optionalen Tools + RAG |
| `execute_tool()` | POST /chat | Spezifisches Tool ausfuehren |
| `get_tools()` | GET /tools | Verfuegbare Tools auflisten |
| `memory_store()` | POST /memory/store | Wissen speichern |
| `memory_recall()` | POST /memory/recall | Wissen abrufen (RAG) |
| `health()` | GET /health | Health Check |
| `status()` | GET /status | Detaillierter Status |

**Mattermost Bridge (`mm_bridge.py`):**
- WebSocket-basierte Echtzeit-Verbindung (Jak Bot Pattern)
- Automatischer Reconnect (5s Backoff)
- Auth via Bearer Token (aus Vault)
- Message-Handler Registration via `on_message()`
- `send_message()` + `send_to_home()` fuer Antworten
- Filtert eigene Nachrichten und unmonitored Channels

### 2.3 Killswitch System (`killswitch/`)

**3-Wege Notaus:**

| Weg | Trigger | Implementierung |
|-----|---------|-----------------|
| **Terminal** | Ctrl+K in TUI | SIGTERM → `KillswitchHandler.kill()` |
| **Mattermost** | `/killswitch <agent>` | Webhook → `killswitch_router` |
| **REST API** | `POST /killswitch/agent/{name}/kill` | HTTP → `KillswitchHandler.kill()` |

**Audit Trail:**
- SHA-256 Hash-Chain (tamper-evident)
- Jeder Kill wird in `killswitch_audit.log` protokolliert
- KillEvent: agent_name, reason, triggered_by, timestamp, hash

**Autorisierung:**
- Nur `killswitch_owners` (default: `["joe"]`) duerfen killen
- Unauthorized Attempts werden geloggt

**Revive:**
- `POST /killswitch/agent/{name}/revive` oder TUI `r`-Taste
- Nur autorisierte User

### 2.4 Agent Config (`config/`)

**AGENT.yaml Schema:**

```yaml
agent:
  name: "lisa01"
  role: "Infrastructure Specialist"
  description: "Docker, Server, Monitoring, Backups"

llm:
  planner: "opus-4.6"           # Cloud LLM fuer Planung
  executor: "mistral-small3.2"  # Ollama fuer Ausfuehrung
  fallback: ["llama3.1:8b"]
  local_only: false             # true = nur lokale Modelle
  ollama_url: "http://10.40.10.90:11434"

communication:
  mattermost:
    token_vault_path: "lisa01/mattermost/MM_TOKEN"
    channels: ["echo_log", "infra-alerts"]
    home_channel: "infra-alerts"
    url: "http://10.40.10.83:8065"

security:
  nss_enabled: true
  mars_threshold: 0.7
  approval_level: "RISKY"       # SAFE=auto, RISKY=fragen, BLOCKED=nie
  killswitch_owners: ["joe"]

tools:
  allowed: ["docker_mcp", "file", "system", "knowledge"]
  blocked: ["cli_bridges"]

memory:
  rag_enabled: true
  persist_learnings: true
  context_max_tokens: 8192
```

**Vordefinierte Templates:**

| Template | Rolle | Erlaubte Tools |
|----------|-------|----------------|
| `lisa01.yaml` | Infrastructure Specialist | docker_mcp, file, system, knowledge |
| `jim01.yaml` | Web & DevOps Specialist | file, system, git, deploy, http_request |
| `john01.yaml` | Research Specialist | knowledge, http_request, file |

### 2.5 PhantomAgent (`agent.py`)

**Hauptklasse die alles zusammenfuegt:**

```python
agent = PhantomAgent.from_config("config/templates/lisa01.yaml")
await agent.start()    # MM Bridge, Killswitch, Announce
result = await agent.handle_task("Deploy new container")
await agent.stop()     # Graceful Shutdown
```

**Task-Processing Pipeline:**

```
handle_task(description)
  |
  1. killswitch.check_alive()        → RuntimeError wenn killed
  |
  2. nss.check_injection(text)       → SENTINEL Injection Check
  |   → Blocked bei Injection
  |
  3. nss.check_risk(text)            → MARS Risk Scoring
  |   → Blocked bei Tier 0-1
  |
  4. hrm_router.assess_complexity()  → Score + Level
  |
  5a. HIGH → planner.create_plan()   → Plan Steps
  |   → executor.execute_plan()      → Step-by-Step via echo_log
  |   → Bei Failure: planner.refine_plan() → Retry
  |
  5b. LOW → echoLog.chat()           → Direkt via echo_log Tools
  |
  6. mm_bridge.send_to_home()        → Status-Notification
  |
  → Return Result
```

### 2.6 TUI Terminal — Kommandozentrale (`kommandozentrale/`)

**Go Binary mit Charm (Bubble Tea + Lip Gloss)**

| Taste | Funktion |
|-------|----------|
| `Ctrl+K` | Killswitch fuer ausgewaehlten Agent |
| `r` | Revive (Agent wiederbeleben) |
| `j/k` oder Pfeiltasten | Agent auswaehlen |
| `q` / `Esc` | Beenden |

**Features:**
- Live Agent-Liste mit Status (ALIVE/KILLED)
- Task Counter pro Agent
- Gateway Health Status (ONLINE/OFFLINE)
- Scrollbarer Log-Feed
- Auto-Refresh alle 2 Sekunden

**Build:**
```bash
cd kommandozentrale
go mod tidy
go build -o phantom-tui ./cmd/
./phantom-tui --pnc http://localhost:18789
```

---

## 3. API Endpoints (PNC Gateway :18789)

### Agent Management

| Method | Endpoint | Funktion |
|--------|----------|----------|
| POST | `/agent/{name}/task` | Task an Agent senden |
| GET | `/agent/{name}/status` | Agent-Status abfragen |
| GET | `/agents` | Alle Agents auflisten |

### Killswitch

| Method | Endpoint | Funktion |
|--------|----------|----------|
| POST | `/killswitch/agent/{name}/kill` | Agent killen |
| POST | `/killswitch/agent/{name}/revive` | Agent wiederbeleben |
| GET | `/killswitch/agent/{name}/status` | Kill-Status |
| POST | `/killswitch/webhook/killswitch` | MM Slash-Command Webhook |
| GET | `/killswitch/agents` | Alle Kill-Status |

### Bestehend (PNC)

| Method | Endpoint | Funktion |
|--------|----------|----------|
| GET | `/health` | Health Check |
| GET | `/sessions` | Aktive Sessions |
| POST | `/sessions/{id}/close` | Session schliessen |
| WS | Socket.IO | WebSocket Events |

---

## 4. Deployment

### Schnellstart (Standalone)

```bash
# 1. Agent Config erstellen
./agent-setup.sh

# 2. Agent starten (ohne Gateway)
python run_agent.py --config agents/lisa01/AGENT.yaml

# 3. Agent mit Gateway starten
python run_agent.py --config agents/lisa01/AGENT.yaml --gateway
```

### Docker Compose

```bash
# Alle Services starten
docker compose up -d

# Services:
#   pnc-gateway    :18789  — PNC + Agent Management
#   nss-gateway    :11337  — NSS Cognitive Gateway
#   nss-guardian   :11338  — NSS Guardian Shield
#   nss-governance :11339  — NSS Governance Plane
#   postgres       :5432   — PostgreSQL
#   redis          :6379   — Redis Cache
#   prometheus     :9090   — Metrics
#   grafana        :3000   — Dashboards
```

### Agent-Setup Script

```bash
./agent-setup.sh
# Interaktiv:
#   1. Agent Name (z.B. lisa01)
#   2. Rolle (Infra/DevOps/Research/Custom)
#   3. LLM Config (Planner/Executor)
#   4. Mattermost Token (Vault-Pfad)
#   5. Killswitch Owners
# Erstellt: agents/{name}/AGENT.yaml + rules/ + skills/
```

---

## 5. Sicherheit (NSS Integration)

### Layered Security

| Layer | Komponente | Funktion | Automatisch |
|-------|-----------|----------|-------------|
| 1 | SENTINEL | Injection Detection | Ja, vor jedem Task |
| 2 | MARS | Risk Scoring (0-1) | Ja, vor jedem Task |
| 3 | VIGIL | Tool Safety (CIA) | Ja, vor jedem Step |
| 4 | SHIELD | Prompt Enhancement | Optional |
| 5 | PII Redaction | Persoenliche Daten entfernen | Optional |
| 6 | Privacy Budget | DSGVO Epsilon-Tracking | Optional |

### Approval Engine (echo_log)

| Level | Verhalten | Beispiel-Tools |
|-------|-----------|----------------|
| SAFE | Auto-approved | knowledge_search, mattermost_send |
| RISKY | Benoetigt Genehmigung | http_request, restart_docker |
| BLOCKED | Immer blockiert | file_delete, deploy_service |

### DSGVO + EU AI Act Compliance

- **PII Redaction** vor LLM-Verarbeitung
- **Privacy Budget** (Epsilon-basiert) pro Datensubjekt
- **DPIA Auto-Generation** via Governance Plane
- **Audit Trail** mit SHA-256 Hash-Chain
- **Art. 17 Unlearning** — Recht auf Vergessenwerden
- **`local_only: true`** — Kein Cloud-LLM wenn gewuenscht

---

## 6. Dateien-Referenz

### Neue Dateien (Phase 1.0)

```
phantom-neural-cortex/
├── agent.py                           # PhantomAgent Hauptklasse
├── run_agent.py                       # CLI Entry Point
├── agent-setup.sh                     # Interaktives Setup
├── Dockerfile                         # Docker Image
├── requirements.txt                   # Python Dependencies
├── .gitmodules                        # NSS + echo_log Submodules
├── hrm/
│   ├── __init__.py
│   ├── router.py                      # HRM Komplexitaets-Router
│   ├── planner.py                     # Cloud LLM Planner
│   └── executor.py                    # Ollama Executor
├── integrations/
│   ├── __init__.py
│   ├── nss_client.py                  # NSS HTTP Client (3 Services)
│   ├── echoLog_client.py              # echo_log HTTP Client
│   └── mm_bridge.py                   # Mattermost WebSocket Bridge
├── killswitch/
│   ├── __init__.py
│   ├── handler.py                     # Kill Logic + Audit
│   └── api.py                         # REST + MM Webhook
├── config/
│   ├── __init__.py
│   ├── schema.py                      # AGENT.yaml Pydantic Schema
│   └── templates/
│       ├── lisa01.yaml                # Infra-Spezialist
│       ├── jim01.yaml                 # Web/DevOps
│       └── john01.yaml               # Research
└── kommandozentrale/                  # Go TUI Terminal
    ├── go.mod
    ├── cmd/main.go
    └── internal/
        ├── tui/app.go                 # Bubble Tea UI
        ├── client/pnc.go             # PNC API Client
        └── config/config.go          # YAML Config
```

### Modifizierte Dateien

```
gateway/server.py                      # +Agent Registry, +REST Endpoints
docker-compose.yml                     # +PNC Gateway, +3 NSS Services
```

---

## 7. Verifikation

### Test 1: HRM Routing
```python
from hrm.router import HRMRouter
router = HRMRouter()
# Simple Task → LOW
a = router.assess_complexity("Check docker status")
assert a.level.value == "low"
# Complex Task → HIGH
a = router.assess_complexity("Architect and refactor the security pipeline with multi-step migration")
assert a.level.value == "high"
```

### Test 2: Killswitch
```bash
# Kill via API
curl -X POST http://localhost:18789/killswitch/agent/lisa01/kill \
  -H "Content-Type: application/json" \
  -d '{"triggered_by": "joe", "details": "test"}'
# → {"status": "killed", "event": {...}}

# Status check
curl http://localhost:18789/killswitch/agent/lisa01/status
# → {"agent": "lisa01", "killed": true, "active_tasks": 0}

# Revive
curl -X POST http://localhost:18789/killswitch/agent/lisa01/revive \
  -H "Content-Type: application/json" \
  -d '{"triggered_by": "joe"}'
```

### Test 3: Task Submission
```bash
curl -X POST http://localhost:18789/agent/lisa01/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Check all docker services health"}'
```

### Test 4: MM Killswitch
```
# In Mattermost:
/killswitch lisa01
# → "KILLSWITCH ACTIVATED for lisa01 by @joe"
```

---

## 8. Microservice-Architektur

```
┌──────────────────────────────────────────────────────┐
│  DOCKER COMPOSE / SWARM                              │
│                                                      │
│  ┌──────────────┐     ┌──────────────────┐           │
│  │ PNC Gateway   │     │ TUI Terminal     │           │
│  │ :18789        │◄────│ (Go Binary,      │           │
│  │ + HRM         │     │  lokal)          │           │
│  │ + Killswitch  │     └──────────────────┘           │
│  │ + Agent Mgmt  │                                    │
│  └──────┬────────┘                                    │
│         │ HTTP                                        │
│  ┌──────▼────────┐  ┌──────────────────┐              │
│  │ NSS Gateway    │  │ NSS Guardian     │              │
│  │ :11337         │  │ :11338           │              │
│  │ PII + STEER    │  │ MARS + SENTINEL  │              │
│  └───────────────┘  │ + VIGIL + SHIELD │              │
│                      └──────────────────┘              │
│  ┌───────────────┐  ┌──────────────────┐              │
│  │ NSS Governance │  │ echo_log VG      │              │
│  │ :11339         │  │ :8085            │              │
│  │ Policy + DPIA  │  │ 42 Tools + RAG   │              │
│  └───────────────┘  └──────────────────┘              │
│                                                      │
│  ┌───────────────┐  ┌──────────────────┐              │
│  │ Ollama         │  │ Mattermost       │              │
│  │ :11434         │  │ :8065            │              │
│  │ GPU: .90/.99   │  │ .83              │              │
│  └───────────────┘  └──────────────────┘              │
└──────────────────────────────────────────────────────┘
```

---

## 9. Zukunft

### Kurzfristig
- Submodules (`git submodule add`) fuer NSS + echo_log
- TUI `go mod tidy` + Build
- Integration Tests gegen laufende Services

### Mittelfristig
- Phantom Link (verschluesselte Agent-zu-Agent Kommunikation)
- Training Pipeline Integration (Wissen ins Modell backen)
- Agent-Marketplace (vordefinierte Rollen-Templates)

### Langfristig
- `local_only: true` — Alles lokal sobald Hardware + Modelle gut genug
- P9 Produkt: "AI Employee as a Service" (EUR 2.500 + EUR 299/mo)
- Multi-Tenant Deployment
