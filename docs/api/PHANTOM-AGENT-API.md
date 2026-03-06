# Phantom Agent System — API Reference

> **Base URL:** `http://<host>:18789`
> **Auth:** Derzeit keine (geplant: JWT via NSS)

---

## Agent Management

### POST /agent/{agent_name}/task
Sendet einen Task an einen registrierten Agent.

**Request:**
```json
{
  "task": "Check all docker services health",
  "context": {"priority": "high"}
}
```

**Response (200):**
```json
{
  "task_id": "lisa01-1-a3f2b1",
  "success": true,
  "response": "All 32 services running 1/1.",
  "tool_results": [...],
  "duration_s": 4.2,
  "complexity": {
    "level": "low",
    "score": 0.28,
    "reasoning": "Complexity score 0.28 (high_kw=0, low_kw=2, steps=0, words=5)",
    "requires_planner": false
  }
}
```

**Response (HIGH complexity):**
```json
{
  "task_id": "lisa01-2-b4c3d2",
  "success": true,
  "steps_completed": 4,
  "steps_failed": 0,
  "total_duration_ms": 12340.5,
  "step_results": [
    {"step_id": 1, "success": true, "output": "...", "duration_ms": 2100, "model_used": "mistral-small3.2"},
    {"step_id": 2, "success": true, "output": "...", "duration_ms": 3200, "model_used": "mistral-small3.2"}
  ],
  "duration_s": 12.3,
  "complexity": {"level": "high", "score": 0.72, "requires_planner": true}
}
```

### GET /agent/{agent_name}/status
Agent-Status abfragen.

**Response (200):**
```json
{
  "name": "lisa01",
  "role": "Infrastructure Specialist",
  "killed": false,
  "task_count": 42,
  "planner_model": "opus-4.6",
  "executor_model": "mistral-small3.2"
}
```

### GET /agents
Alle registrierten Agents auflisten.

**Response (200):**
```json
{
  "agents": {
    "lisa01": {"role": "Infrastructure Specialist", "killed": false, "task_count": 42},
    "jim01": {"role": "Web & DevOps Specialist", "killed": false, "task_count": 17}
  }
}
```

---

## Killswitch

### POST /killswitch/agent/{agent_name}/kill
Agent sofort stoppen. Bricht alle laufenden Tasks ab.

**Request:**
```json
{
  "triggered_by": "joe",
  "details": "Emergency stop — wrong deployment"
}
```

**Response (200):**
```json
{
  "status": "killed",
  "event": {
    "agent_name": "lisa01",
    "reason": "api",
    "triggered_by": "joe",
    "timestamp": 1741340000.0,
    "details": "Emergency stop — wrong deployment (cancelled 2 tasks)",
    "hash": "a3f2b1c4d5e6f7..."
  }
}
```

**Response (403):** Unauthorized user
**Response (404):** Agent not found

### POST /killswitch/agent/{agent_name}/revive
Gekillten Agent wiederbeleben.

**Request:**
```json
{"triggered_by": "joe"}
```

**Response (200):**
```json
{"status": "revived", "agent": "lisa01"}
```

### GET /killswitch/agent/{agent_name}/status

**Response (200):**
```json
{
  "agent": "lisa01",
  "killed": false,
  "active_tasks": 3
}
```

### POST /killswitch/webhook/killswitch
Mattermost Slash-Command Webhook. Konfiguriert als `/killswitch` in MM.

**Request (MM Webhook):**
```json
{
  "text": "lisa01",
  "user_name": "joe",
  "channel_name": "echo_log"
}
```

**Response:**
```json
{
  "response_type": "in_channel",
  "text": "**KILLSWITCH ACTIVATED** for `lisa01` by @joe\nHash: `a3f2b1c4d5e6f7...`"
}
```

### GET /killswitch/agents
Alle Agents mit Kill-Status.

**Response (200):**
```json
{
  "agents": {
    "lisa01": {"killed": false, "active_tasks": 3, "authorized_users": ["joe"]},
    "jim01": {"killed": true, "active_tasks": 0, "authorized_users": ["joe"]}
  }
}
```

---

## Health & Sessions (bestehend)

### GET /health
Gateway Health Check.

### GET /sessions
Aktive WebSocket Sessions.

### POST /sessions/{session_id}/close
Session beenden.

---

## WebSocket Events (Socket.IO)

| Event | Richtung | Daten |
|-------|----------|-------|
| `connect` | Server→Client | `{session_id, message}` |
| `message` | Client→Server | `{type, content, metadata}` |
| `message_received` | Server→Client | `{message_id, status}` |
| `command` | Client→Server | `{command: "/status"}` |
| `command_result` | Server→Client | `{command, result}` |
| `error` | Server→Client | `{error}` |

### Verfuegbare Commands
- `/status` — System Health
- `/swarm-status` — Swarm Intelligence Status
- `/preview <task>` — Impact Prediction (Dry Run)
- `/context` — Token-Usage der aktuellen Session
