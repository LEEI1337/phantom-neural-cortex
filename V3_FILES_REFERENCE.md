# v3.0 Files Reference

Quick reference guide to all new files in v3.0 implementation.

## Gateway Module (`gateway/`)

All gateway-related code for centralized control plane.

| File | Purpose | LOC |
|------|---------|-----|
| `__init__.py` | Package exports | 20 |
| `config.py` | Configuration management | 50 |
| `server.py` | WebSocket gateway server | 250 |
| `session.py` | Session management & persistence | 280 |
| `router.py` | Message routing & queues | 145 |
| `health.py` | Health monitoring | 165 |

**Total:** ~910 LOC

## Skills Module (`skills/`)

Hot-reloadable plugin system.

| File | Purpose | LOC |
|------|---------|-----|
| `__init__.py` | Package exports | 18 |
| `base.py` | Base Skill class | 120 |
| `registry.py` | Skill discovery & management | 155 |
| `loader.py` | Dynamic skill loading | 50 |
| `sandbox.py` | Safe execution environment | 65 |
| `community/__init__.py` | Community skills package | 2 |
| `community/github_automation.py` | Example GitHub skill | 85 |

**Total:** ~495 LOC

## Context Module (`dashboard/backend/context/`)

Context window management (pre-existing, verified).

| File | Purpose | LOC |
|------|---------|-----|
| `__init__.py` | Package exports | 57 |
| `models.py` | Pydantic data models | 110 |
| `tracker.py` | Token tracking | 334 |
| `pruner.py` | Pruning strategies | 294 |
| `compactor.py` | AI compaction | 257 |
| `inspector.py` | CLI commands | 274 |
| `utils.py` | Token counting | 163 |

**Total:** ~1,489 LOC

## Modified Core Files

| File | Changes | Purpose |
|------|---------|---------|
| `dashboard/backend/main.py` | Gateway & skills startup | Integration |
| `.env.example` | 15+ new variables | Configuration |
| `README.md` | v3.0 announcement | Documentation |
| `CHANGELOG.md` | v3.0 release notes | Documentation |

## New Documentation

| File | Purpose | Size |
|------|---------|------|
| `docs/V3_FEATURES.md` | Feature guide | 7.3 KB |
| `V3_IMPLEMENTATION_COMPLETE.md` | Implementation report | 8.8 KB |
| `V3_FILES_REFERENCE.md` | This file | - |
| `dashboard/backend/demo_v3_features.py` | Working demo | 7.2 KB |

## Directory Structure

```
phantom-neural-cortex/
├── gateway/                          # NEW - Phase 2
│   ├── __init__.py
│   ├── config.py
│   ├── server.py
│   ├── session.py
│   ├── router.py
│   └── health.py
│
├── skills/                           # NEW - Phase 3
│   ├── __init__.py
│   ├── base.py
│   ├── registry.py
│   ├── loader.py
│   ├── sandbox.py
│   └── community/
│       ├── __init__.py
│       └── github_automation.py
│
├── dashboard/backend/
│   ├── context/                      # Phase 1 (pre-existing)
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── tracker.py
│   │   ├── pruner.py
│   │   ├── compactor.py
│   │   ├── inspector.py
│   │   └── utils.py
│   │
│   ├── main.py                       # UPDATED
│   └── demo_v3_features.py          # NEW
│
├── docs/
│   └── V3_FEATURES.md               # NEW
│
├── .env.example                      # UPDATED
├── README.md                         # UPDATED
├── CHANGELOG.md                      # UPDATED
├── V3_IMPLEMENTATION_COMPLETE.md    # NEW
└── V3_FILES_REFERENCE.md            # NEW (this file)
```

## Import Paths

### Gateway
```python
from gateway import GatewayServer, GatewayConfig
from gateway.session import SessionManager, Session
from gateway.router import MessageRouter, Message
from gateway.health import HealthMonitor
```

### Skills
```python
from skills import SkillRegistry, SkillLoader, SkillSandbox
from skills.base import Skill, SkillContext
```

### Context
```python
from dashboard.backend.context import ContextTracker
from dashboard.backend.context import ContextPruner
from dashboard.backend.context import ContextCompactor
```

## Configuration Files

### Environment Variables
- `.env.example` - Template with all v3.0 variables

### Docker
- `docker-compose.yml` - Redis service (already exists)

## Testing Files

### Demo Script
- `dashboard/backend/demo_v3_features.py` - Demonstrates all features

### Test Structure (for future)
```
dashboard/backend/
├── tests/
│   ├── test_gateway.py         # Future
│   ├── test_skills.py          # Future
│   └── context/
│       ├── test_tracker.py     # Existing
│       ├── test_pruner.py      # Existing
│       └── test_compactor.py   # Existing
```

## Size Summary

| Component | Files | LOC | Status |
|-----------|-------|-----|--------|
| Gateway | 6 | ~910 | ✅ New |
| Skills | 7 | ~495 | ✅ New |
| Context | 7 | ~1,489 | ✅ Existing |
| **Total** | **20** | **~2,894** | ✅ Complete |

## Quick Access Commands

```bash
# View gateway code
ls -la gateway/

# View skills code
ls -la skills/

# View context code
ls -la dashboard/backend/context/

# View documentation
ls -la docs/ | grep V3

# Run demo
python dashboard/backend/demo_v3_features.py

# View configuration
cat .env.example | grep -A 5 "GATEWAY\|SKILLS\|CONTEXT"
```

---

**Reference Version:** v3.0.0  
**Last Updated:** 2026-02-04  
**Status:** Complete
