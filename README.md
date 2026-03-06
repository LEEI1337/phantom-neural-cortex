# Phantom Neural Cortex v4.0 — Phantom Agent System

> Deployable AI Employee — PNC + NSS + echo_log + Mattermost unified

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-4.0.0-brightgreen.svg)](CHANGELOG.md)

**A unified AI agent system that combines orchestration (PNC), security (NSS), tool execution (echo_log), and team communication (Mattermost) into a single deployable AI employee.**

## What's New in v4.0 — Phantom Agent System

v4.0 integrates four production systems into one agent that can plan, execute, communicate, and be controlled:

### Core v4.0 Features

- **HRM Controller** — Cloud LLMs plan (Opus/Codex), local models execute (Ollama)
- **NSS Security** — 6-layer defense in every task pipeline (SENTINEL, MARS, VIGIL, SHIELD)
- **echo_log Integration** — 42 tools, RAG memory, 4-phase reasoning via HTTP
- **Mattermost Bridge** — Real-time WebSocket communication (Jak Bot pattern)
- **3-Way Killswitch** — Terminal (Ctrl+K), Mattermost (`/killswitch`), REST API
- **AGENT.yaml Config** — Pydantic-validated agent configuration with role templates
- **Go TUI Terminal** — Bubble Tea Kommandozentrale with live agent monitoring
- **DSGVO + EU AI Act** — Compliance via NSS (PII redaction, privacy budget, audit trail)

### Previous Features (v3.x)

- **Intelligent Swarm Routing (Phase 5)** — Score-based agent selection (IntelligenceEngine)
- **Impact Prediction (Dry Run)** — Simulate cost, quality, and speed before execution
- **Autonomous Feedback Loops** — Automatic re-routing if quality thresholds aren't met
- **Advanced CLI & Dashboard (Phase 6)** — Interactive Socket.IO CLI
- **Persistent Multi-Backend Memory (Phase 4)** — SQL + Redis
- **Sandbox Hardening (Phase 7)** — Docker-based isolated execution

---

## Architecture

```
Task -> PhantomAgent.handle_task()
         |
         1. Killswitch Check
         2. NSS SENTINEL (Injection Defense)
         3. NSS MARS (Risk Scoring)
         4. HRM Router (Complexity Assessment)
         |                    |
     HIGH (>= 0.6)       LOW (< 0.6)
         |                    |
     Planner              echo_log
     (Cloud LLM)          /chat API
     -> Plan Steps        (42 Tools)
     -> Executor
     (Ollama)
         |
     Feedback Loop
     (on failure -> refine plan)
         |
     MM Notification
```

### Service Architecture

```
PNC Gateway :18789     -- Orchestration + Agent Management + Killswitch
NSS Gateway :11337     -- PII Redaction, STEER
NSS Guardian :11338    -- MARS, SENTINEL, VIGIL, SHIELD
NSS Governance :11339  -- Policy Engine, Privacy Budget, DPIA
echo_log VG :8085      -- 42 Tools, RAG, Reasoning
Ollama :11434          -- Local LLM Inference (GPU)
Mattermost :8065       -- Team Communication
```

---

## Quick Start

### Deploy an Agent (5 minutes)

```bash
# 1. Clone
git clone https://github.com/LEEI1337/phantom-neural-cortex
cd phantom-neural-cortex
pip install -r requirements.txt

# 2. Interactive Setup
./agent-setup.sh
# -> Creates agents/<name>/AGENT.yaml

# 3. Start Agent with Gateway
python run_agent.py --config agents/lisa01/AGENT.yaml --gateway
# -> Gateway on :18789, Agent listening on Mattermost
```

### Docker Compose (Full Stack)

```bash
docker compose up -d
# Starts: PNC Gateway, 3x NSS, PostgreSQL, Redis, Prometheus, Grafana
```

### Submit a Task

```bash
curl -X POST http://localhost:18789/agent/lisa01/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Check all docker services and report unhealthy ones"}'
```

### TUI Terminal (Kommandozentrale)

```bash
cd kommandozentrale
go mod tidy && go build -o phantom-tui ./cmd/
./phantom-tui --pnc http://localhost:18789
# Ctrl+K = Killswitch | r = Revive | j/k = Navigate | q = Quit
```

### Legacy CLI

```bash
python cli.py
# /status, /swarm-status, /preview <task>, /context
```

---

## Key Components

### PhantomAgent (`agent.py`)

The unified agent class. Load from AGENT.yaml, start, handle tasks, stop:

```python
agent = PhantomAgent.from_config("config/templates/lisa01.yaml")
await agent.start()     # Connect MM, register killswitch
result = await agent.handle_task("Deploy new monitoring stack")
await agent.stop()
```

### HRM Controller (`hrm/`)

Hierarchical Reasoning Model — routes by complexity:

| Complexity | Score | Model | Path |
|-----------|-------|-------|------|
| HIGH | >= 0.6 | Cloud LLM (Opus) | Planner -> Steps -> Executor |
| MEDIUM | >= 0.35 | Ollama | Direct via echo_log |
| LOW | < 0.35 | Ollama | Direct via echo_log |

### Killswitch (`killswitch/`)

3-way emergency stop with SHA-256 tamper-evident audit trail:

- **Terminal**: Ctrl+K in TUI
- **Mattermost**: `/killswitch lisa01`
- **REST API**: `POST /killswitch/agent/lisa01/kill`

### AGENT.yaml (`config/`)

```yaml
agent:
  name: "lisa01"
  role: "Infrastructure Specialist"
llm:
  planner: "opus-4.6"
  executor: "mistral-small3.2"
  local_only: false
security:
  nss_enabled: true
  approval_level: "RISKY"
  killswitch_owners: ["joe"]
```

Templates: `lisa01` (Infra), `jim01` (DevOps), `john01` (Research)

### NSS Security (via `integrations/nss_client.py`)

Every task passes through:
1. SENTINEL — Injection detection
2. MARS — Risk scoring (Tier 0-3)
3. VIGIL — Tool safety (before each step)

Graceful degradation: if NSS is offline, defaults to SAFE.

---

## Project Structure

```
phantom-neural-cortex/
├── agent.py                    # PhantomAgent main class
├── run_agent.py                # CLI entry point
├── agent-setup.sh              # Interactive agent setup
├── hrm/                        # HRM Controller
│   ├── router.py               # Complexity assessment
│   ├── planner.py              # Cloud LLM planning
│   └── executor.py             # Ollama execution
├── integrations/               # Service clients
│   ├── nss_client.py           # NSS (3 services)
│   ├── echoLog_client.py       # echo_log VG
│   └── mm_bridge.py            # Mattermost WebSocket
├── killswitch/                 # Emergency stop
│   ├── handler.py              # Kill logic + audit
│   └── api.py                  # REST + MM webhook
├── config/                     # Agent configuration
│   ├── schema.py               # AGENT.yaml schema
│   └── templates/              # Role templates
├── kommandozentrale/           # Go TUI Terminal
│   ├── cmd/main.go
│   └── internal/tui/app.go
├── gateway/                    # PNC Gateway (existing)
├── dashboard/                  # Dashboard (existing)
├── memory/                     # Memory backends (existing)
├── skills/                     # Skills system (existing)
├── docker-compose.yml          # Full stack
└── docs/
    ├── PHANTOM-AGENT-SYSTEM.md # Full technical docs
    └── api/PHANTOM-AGENT-API.md
```

## Roadmap

- [x] **Phase 1-3**: Base OpenClaw Modernization
- [x] **Phase 4**: Persistent Memory (SQL/Redis)
- [x] **Phase 5**: Swarm Routing & Impact Prediction
- [x] **Phase 6**: CLI & Dashboard
- [x] **Phase 7**: Sandbox Hardening
- [x] **Phase 8**: Phantom Agent System (PNC + NSS + echo_log + MM)
- [ ] **Phase 9**: Phantom Link (encrypted agent-to-agent communication)
- [ ] **Phase 10**: Training Pipeline integration (bake knowledge into models)

## Documentation

- [Phantom Agent System (Full)](docs/PHANTOM-AGENT-SYSTEM.md)
- [API Reference](docs/api/PHANTOM-AGENT-API.md)
- [System Architecture](docs/SYSTEM_ARCHITECTURE_SUMMARY.md)
- [Context Management](docs/CONTEXT_MANAGEMENT.md)
- [Sandbox Hardening](docs/architecture/SANDBOX_HARDENING.md)

---

**Maintained by:** [LEEI1337](https://github.com/LEEI1337) / [AI Engineering](https://www.ai-engineering.at)
**Version:** 4.0.0
**Last Updated:** March 2026
