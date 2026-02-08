# v3.0.0 Features Documentation

## Overview

Phantom Neural Cortex v3.5 introduces deep orchestration logic and autonomous swarm intelligence alongside OpenClaw-inspired features:

1. **Advanced Context Window Management** (Phase 1) ✅
2. **Gateway Architecture** (Phase 2) ✅  
3. **Skills System** (Phase 3) ✅
4. **Persistent Memory Manager** (Phase 4) ✅
5. **Intelligent Swarm Routing** (Phase 5) ✅
6. **Unified CLI & Visualization** (Phase 6) ✅
7. **Sandbox Hardening** (Phase 7) 🛡️ *In Progress*

---

## 1. Context Window Management

Real-time token tracking with intelligent pruning and compaction.

### Features

- **Token Tracking**: Precise counting using tiktoken
- **Auto-Pruning**: Remove old/unimportant messages automatically
- **AI Compaction**: Summarize long conversations
- **CLI Commands**: Interactive inspection

### Usage

```python
from dashboard.backend.context import ContextTracker, ModelType

# Create tracker
tracker = ContextTracker(
    session_id="session_123",
    model=ModelType.CLAUDE
)

# Add messages
tracker.add_system_prompt("System instructions")
tracker.add_user_message("User question")
tracker.add_assistant_message("AI response")

# Get status
status = tracker.get_status()
print(f"Using {status.total_tokens}/{status.max_tokens} tokens")
```

### API Endpoints

- `GET /api/context/status?session_id=xyz` - Get status
- `GET /api/context/inspection?session_id=xyz` - Detailed view
- `POST /api/context/prune` - Trigger pruning
- `POST /api/context/compact` - Trigger compaction

---

## 2. Gateway Architecture

Centralized WebSocket gateway on port 18789.

### Features

- **Session Management**: Persistent sessions across restarts
- **Message Routing**: Intelligent distribution
- **Health Monitoring**: Real-time system status

### Usage

```python
from gateway import GatewayServer, GatewayConfig

# Create gateway
config = GatewayConfig.from_env()
gateway = GatewayServer(config)

# Start gateway
await gateway.start()

# Gateway runs on port 18789
```

### Configuration

```bash
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=18789
GATEWAY_SESSION_TIMEOUT=3600
GATEWAY_MAX_SESSIONS=1000
GATEWAY_STORAGE_BACKEND=redis  # Options: memory, redis
```

**Note:** Currently supports `memory` and `redis` backends. Database backend (PostgreSQL/SQLite) will be added in a future update.

### WebSocket Events

**Connect**: Automatic session creation

```javascript
socket.on('connected', (data) => {
  console.log('Session ID:', data.session_id);
});
```

**Send Message**:

```javascript
socket.emit('message', {
  type: 'user_message',
  content: 'Hello!',
  metadata: {}
});
```

**Get Status**:

```javascript
socket.emit('get_status');
socket.on('status', (data) => {
  console.log('Health:', data);
});
```

---

## 3. Skills System

Hot-reloadable plugin system for extending functionality.

### Features

- **Hot-Reload**: Update skills without restart
- **Sandboxed**: Safe execution with resource limits
- **Extensible**: Easy to create new skills

### Creating a Skill

```python
from skills import Skill, SkillContext

class MySkill(Skill):
    def __init__(self):
        super().__init__(
            name="my_skill",
            version="1.0.0",
            author="me",
            description="My awesome skill",
            tags=["automation"]
        )
    
    async def execute(self, action: str, context: SkillContext, **kwargs):
        if action == "do_something":
            return {"result": "done", "data": kwargs}
        raise ValueError(f"Unknown action: {action}")
```

### Using Skills

```python
from skills import SkillRegistry, SkillLoader, SkillContext

# Initialize registry
registry = SkillRegistry("skills/community")

# Load skills
loader = SkillLoader(registry)
await loader.load_all_skills()

# Execute skill
skill = registry.get_skill("github_automation")
context = SkillContext(session_id="xyz", workspace=".")
result = await skill.execute("create_issue", context, 
    title="Bug report",
    body="Description here"
)
```

### Configuration

```bash
SKILLS_DIR=skills/community
SKILLS_AUTO_LOAD=true
SKILLS_HOT_RELOAD=true
SKILLS_MAX_EXECUTION_TIME=300
SKILLS_MAX_MEMORY_MB=512
SKILLS_SANDBOX_ENABLED=true
```

---

## 4. Intelligent Swarm Routing

Autonomous agent selection and refinement loops.

### Features

- **Score-Based Selection**: Intelligent engine selects best agent for task.
- **Impact Prediction**: Simulate results before execution.
- **Autonomous Feedback Loops**: Re-route and retry tasks if quality thresholds are not met.

---

## 5. Sandbox Hardening

Strictly isolated skill execution.

### Features

- **Docker-Based Execution**: Each skill runs in a transient container.
- **Resource Quotas**: Hard limits on CPU (0.5) and RAM (256MB).
- **Network Isolation**: By default, skills have no outbound internet access.
- **Secure Bridge**: Standardized communication between Host and Sandbox.

---

## Quick Start

### 1. Install Dependencies

```bash
cd dashboard/backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Start Services

```bash
# Start Redis (required for gateway)
docker-compose up -d redis

# Start backend (includes gateway and skills)
uvicorn main:app --host 0.0.0.0 --port 1336
```

### 4. Verify v3.0 Features

Check startup output for:

```
✓ Gateway started on 0.0.0.0:18789
✓ Skills system initialized: X skills loaded
```

---

## Testing

### Test Context Management

```bash
curl http://localhost:1336/api/context/status?session_id=test123
```

### Test Gateway

```bash
# Gateway health
curl http://localhost:18789/health

# List sessions
curl http://localhost:18789/sessions
```

### Test Skills

Access via API or use skills programmatically in Python.

---

## Migration from v2.x

### Breaking Changes

None! v3.0 is fully backward compatible.

### New Features to Adopt

1. Enable context management for token optimization
2. Connect clients to gateway (port 18789) for better session management
3. Create custom skills to extend functionality

### Optional Configuration

All v3.0 features are optional and have sensible defaults. The system works without explicit configuration.

---

## Troubleshooting

### Gateway not starting

- Check Redis is running: `docker-compose up -d redis`
- Verify REDIS_URL in .env
- Check port 18789 is available

### Skills not loading

- Verify SKILLS_DIR path exists
- Check skill files have correct structure
- Review logs for import errors

### Context management issues

- Ensure tiktoken is installed: `pip install tiktoken`
- Check CONTEXT_* environment variables
- Verify session_id is consistent

---

## Architecture

```
┌─────────────────────────────────────────┐
│     Phantom Neural Cortex v3.0          │
├─────────────────────────────────────────┤
│                                         │
│  Gateway (Port 18789) ✅                │
│  ├─ WebSocket Server                    │
│  ├─ Session Manager                     │
│  ├─ Message Router                      │
│  └─ Health Monitor                      │
│                                         │
│  Skills System ✅                        │
│  ├─ Registry                            │
│  ├─ Loader (Hot-reload)                 │
│  ├─ Sandbox                             │
│  └─ Community Skills                    │
│                                         │
│  Context Management ✅                   │
│  ├─ Token Tracker                       │
│  ├─ Auto-Pruner                         │
│  ├─ AI Compactor                        │
│  └─ Inspector                           │
│                                         │
│  Existing Features                      │
│  ├─ Multi-Agent Orchestration           │
│  ├─ Quality Assessment                  │
│  ├─ Guidelines Evolution                │
│  └─ Cost Optimization                   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Contributing

Want to add features or create skills?

1. Fork the repository
2. Create feature branch
3. For skills: Add to `skills/community/`
4. Submit pull request

---

## Support

- Documentation: [docs/](../docs/)
- Issues: [GitHub Issues](https://github.com/LEEI1337/phantom-neural-cortex/issues)
- Changelog: [CHANGELOG.md](../CHANGELOG.md)

---

**Version:** 3.5.0  
**Last Updated:** 2026-02-08  
**Maintained by:** LEEI1337
