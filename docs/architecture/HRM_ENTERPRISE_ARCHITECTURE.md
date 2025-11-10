# HRM System - Enterprise-Grade Architektur & Implementierungs-Plan

**Phantom Neural Cortex - Hierarchical Recursive Model System**
**Version:** 3.0.0
**Datum:** 2025-11-10
**Autor:** Claude (Phantom Neural Cortex Team)

---

## Executive Summary

Das HRM (Hierarchical Recursive Model) System ist eine hochmoderne Enterprise-Plattform für AI-gesteuerte Entwicklung mit ML/RL-Optimierungen, Multi-Agenten-Orchestrierung und intelligenter Konfigurationsverwaltung.

**Key Features:**
- 12 ML/RL-Optimierungen (Latent Reasoning, Smart Agent Switching, Deep Supervision, etc.)
- Multi-AI-Agent-System (Claude, Gemini, Copilot, Cursor, Windsurf, OpenHands)
- Hierarchisches Layer-Guideline-System (Universal Standards → Agent-spezifisch)
- Real-time HRM Configuration Control mit Impact Simulation
- Docker-basierte Multi-Platform-Deployment (Windows, Linux, macOS)
- 14 MCP Server-Integrationen
- WebSocket-basierte Real-time Updates
- Prometheus Monitoring & Grafana Dashboards

**Performance Metriken:**
- -60% Deploy Time
- -52% Cost Reduction
- +34% Quality Improvement
- 40% Token Reduction durch Latent Reasoning

---

## Table of Contents

1. [System-Architektur-Übersicht](#system-architektur-übersicht)
2. [Komponenten-Hierarchie](#komponenten-hierarchie)
3. [HRM Backend-Architektur](#hrm-backend-architektur)
4. [Database Schema & Tables](#database-schema--tables)
5. [API Routes & Endpoints](#api-routes--endpoints)
6. [Guidelines & Configurations System](#guidelines--configurations-system)
7. [Docker & Container-Orchestrierung](#docker--container-orchestrierung)
8. [Multi-AI-Agent Integration](#multi-ai-agent-integration)
9. [MCP Server-Integration](#mcp-server-integration)
10. [Datenflüsse & State Management](#datenflüsse--state-management)
11. [Real-time Updates (WebSocket)](#real-time-updates-websocket)
12. [Monitoring & Observability](#monitoring--observability)
13. [Enterprise Deployment Guide](#enterprise-deployment-guide)
14. [Best Practices & Patterns](#best-practices--patterns)

---

## System-Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHANTOM NEURAL CORTEX UI                            │
│                    Hierarchical Recursive Model System                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
         ┌──────▼──────┐      ┌─────▼──────┐     ┌──────▼──────┐
         │  Frontend   │      │  Backend   │     │  Database   │
         │  (React)    │      │  (FastAPI) │     │ (PostgreSQL)│
         │  Port: 1337 │      │ Port: 1336 │     │ Port: 5432  │
         └─────────────┘      └────────────┘     └─────────────┘
                │                    │                    │
                │              ┌─────▼─────┐              │
                │              │ WebSocket │              │
                │              │  (Socket  │              │
                │              │    .IO)   │              │
                │              └─────┬─────┘              │
                │                    │                    │
         ┌──────▼────────────────────▼────────────────────▼──────┐
         │              HRM Configuration Layer                  │
         │  ┌────────────────────────────────────────────────┐  │
         │  │ 12 ML/RL Optimizations (ADR-001 bis ADR-012)   │  │
         │  │ - Latent Reasoning (40% token reduction)       │  │
         │  │ - Smart Agent Switching (52% cost savings)     │  │
         │  │ - Deep Supervision (quality gates)             │  │
         │  │ - Parallel Evaluation (30-40% speed up)        │  │
         │  │ - Bayesian Optimization (weight tuning)        │  │
         │  │ - RL Refinement Chain (PPO-based)              │  │
         │  │ - Multi-Repo Coordination                      │  │
         │  │ - Prometheus Metrics Export                    │  │
         │  └────────────────────────────────────────────────┘  │
         └───────────────────────────┬───────────────────────────┘
                                     │
         ┌───────────────────────────▼───────────────────────────┐
         │              Multi-AI Agent Orchestration             │
         │  ┌──────────┬──────────┬──────────┬──────────────┐   │
         │  │  Claude  │  Gemini  │ Copilot  │  OpenHands   │   │
         │  │  (Pro)   │  (Free)  │  (Pro)   │ (Autonomous) │   │
         │  └──────────┴──────────┴──────────┴──────────────┘   │
         │  ┌──────────┬──────────┬──────────┐                  │
         │  │  Cursor  │ Windsurf │   Rover  │                  │
         │  └──────────┴──────────┴──────────┘                  │
         └───────────────────────────┬───────────────────────────┘
                                     │
         ┌───────────────────────────▼───────────────────────────┐
         │           Guidelines & Configurations Layer           │
         │  ┌────────────────────────────────────────────────┐   │
         │  │ Hierarchical Layer System:                     │   │
         │  │ - LAYER-0: Universal Standards (NO EMOJIS!)    │   │
         │  │ - LAYER-1: MCP Server Usage                    │   │
         │  │ - LAYER-2: AI CLI Agent-Specific               │   │
         │  │   ├─ LAYER-2-CLAUDE.md (Security, Quality)     │   │
         │  │   ├─ LAYER-2-COPILOT.md (GitHub, Boilerplate)  │   │
         │  │   └─ LAYER-2-GEMINI.md (Bulk, 2M context)      │   │
         │  └────────────────────────────────────────────────┘   │
         └───────────────────────────┬───────────────────────────┘
                                     │
         ┌───────────────────────────▼───────────────────────────┐
         │              MCP Server Integration Layer             │
         │  ┌────────────────────────────────────────────────┐   │
         │  │ 14 MCP Servers:                                │   │
         │  │ - filesystem, memory, github, brave-search     │   │
         │  │ - sequential-thinking, gemini-cli, perplexity  │   │
         │  │ - browser-tools, studentofjs, mcp-inspector    │   │
         │  │ - copilot-cli, docs, sqlite, postgres, time    │   │
         │  │ - postmancer (API testing)                     │   │
         │  └────────────────────────────────────────────────┘   │
         └───────────────────────────┬───────────────────────────┘
                                     │
         ┌───────────────────────────▼───────────────────────────┐
         │           LazyBird Python Module Layer                │
         │  ┌────────────────────────────────────────────────┐   │
         │  │ Core Modules:                                  │   │
         │  │ - feedback/ (Refinement Loop, Quality Eval)    │   │
         │  │ - ml/ (Iteration Predictor, Weight Optimizer)  │   │
         │  │ - cache/ (3-Layer Caching)                     │   │
         │  │ - monitoring/ (Prometheus Exporter)            │   │
         │  │ - speckit/ (GitHub Spec-Kit Integration)       │   │
         │  │ - multi-repo/ (Dependency Analyzer)            │   │
         │  │ - scripts/ (Orchestrators, Adapters)           │   │
         │  └────────────────────────────────────────────────┘   │
         └───────────────────────────────────────────────────────┘
```

---

## Komponenten-Hierarchie

### Layer-Struktur (Top-Down)

**LAYER 4: Phantom Neural Cortex UI (Dashboard)**
- **Frontend:** React + Vite + TypeScript + TailwindCSS + ReactFlow
- **Backend:** FastAPI + SQLAlchemy + WebSocket (Socket.IO)
- **Database:** PostgreSQL 16 + Redis 7
- **Zweck:** User Interface, Real-time Config Control, Monitoring

**LAYER 3: LazyBird Orchestration**
- **Kern:** Python Module mit ML/RL-Optimierungen
- **Komponenten:** Feedback Loop, Iteration Predictor, Smart Agent Switcher
- **Zweck:** Task Execution, Quality Evaluation, Agent Orchestration

**LAYER 2: AI Agents (Multi-Agent System)**
- **Claude:** Security, Architecture, Complex Problems ($20/mo)
- **Gemini:** Bulk Operations, Large Context (FREE, 2M tokens)
- **Copilot:** GitHub Workflows, Quick Fixes ($10/mo)
- **OpenHands:** Autonomous E2E Implementation
- **Rover:** CLI-based Task Orchestration
- **Cursor/Windsurf:** IDE Integration

**LAYER 1: MCP Server Integration**
- **14 MCP Servers:** filesystem, github, memory, etc.
- **Zweck:** Tool Access, API Integration, Memory Management

**LAYER 0: Guidelines & Standards**
- **Universal Standards:** NO EMOJIS, Clean Code, Security First
- **Agent-Specific:** Layer-2-Claude, Layer-2-Copilot, Layer-2-Gemini
- **Zweck:** Consistent Behavior, Quality Standards

---

## HRM Backend-Architektur

### Core Backend-Struktur

```
dashboard/backend/
├── main.py                 # FastAPI App Entry Point
├── database.py             # Database Configuration & Session Management
├── models.py               # SQLAlchemy ORM Models
├── routers/
│   ├── hrm.py             # HRM Configuration API (12 ML/RL Optimizations)
│   ├── agents.py          # Agent Connection Management
│   ├── projects.py        # Project CRUD Operations
│   ├── tasks.py           # Task Orchestration
│   ├── metrics.py         # Quality & Cost Metrics
│   ├── config.py          # System Configuration
│   ├── websocket.py       # Real-time WebSocket Updates
│   ├── prometheus.py      # Prometheus Metrics Endpoint
│   ├── speckit.py         # GitHub Spec-Kit Integration
│   ├── api_keys.py        # Multi-Provider API Key Management
│   ├── swarm.py           # Swarm Orchestration
│   └── templates.py       # Project Templates
├── Dockerfile
└── requirements.txt
```

### HRM Configuration Router (`routers/hrm.py`)

**Zweck:** Real-time Control der 12 ML/RL-Optimierungen mit Impact Simulation

**Hauptfunktionen:**
1. **HRM Config Management:** CRUD für HRM-Konfigurationen (Project/Task-spezifisch)
2. **Preset System:** Built-in + Custom Presets (balanced, cost-optimized, quality-first, etc.)
3. **Impact Simulation:** Vorhersage von Cost/Speed/Quality-Änderungen
4. **Config History:** Audit Log für alle Konfigurations-Änderungen
5. **Real-time Updates:** WebSocket Events bei Config-Änderungen

**HRM Configuration Schema:**
```python
HRMConfigSchema:
  latent_reasoning:           # ADR-001: Token Compression
    enabled: bool
    dimensionality: int (128-1024)
    compression_ratio_target: float
    auto_adjust: bool

  ml_iteration_prediction:    # ADR-002: Iteration Count Prediction
    mode: "auto" | "manual" | "fixed"
    max_iterations: int (2-20)
    confidence_threshold: float

  agent_switching:             # ADR-005: Smart Agent Switching
    strategy: "cost_optimized" | "quality_first" | "speed_optimized" |
              "adaptive" | "round_robin" | "manual"
    quality_drop_threshold: float
    cost_ceiling: float
    max_switches_per_task: int

  deep_supervision:            # ADR-004: Quality Gates
    enabled: bool
    checkpoints: [0.33, 0.66, 1.00]
    quality_gate_threshold: float

  parallel_evaluation:         # ADR-006: Parallel Quality Eval
    enabled: bool
    worker_count: int (1-16)
    timeout_seconds: int

  caching:                     # ADR-007: 3-Layer Caching
    memory: bool
    disk: bool
    remote: bool
    aggressive_mode: bool
    max_size_mb: int

  bayesian_optimization:       # ADR-008: Weight Optimization
    enabled: bool
    iterations: int

  rl_refinement:               # ADR-011: PPO-based Refinement
    enabled: bool
    epsilon: float
    learning_rate: float

  prometheus_metrics:          # ADR-010: Metrics Export
    enabled: bool
    export_interval: int

  multi_repo:                  # ADR-009: Multi-Repo Coordination
    enabled: bool
```

**Impact Estimation:**
- Berechnet **cost_change**, **speed_change**, **quality_change**, **token_reduction**
- Basiert auf historischen Daten und ML-Modellen
- Liefert Confidence Score und Recommendations

---

## Database Schema & Tables

### Vollständiges Database Schema

```sql
-- ============================================================================
-- CORE TABLES (Projects & Tasks)
-- ============================================================================

CREATE TABLE projects (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    type ENUM('python', 'typescript', 'react', 'node', 'general') NOT NULL,
    status ENUM('active', 'paused', 'archived') DEFAULT 'active',
    github_repo VARCHAR,
    slot VARCHAR NOT NULL,  -- "Projekt-A", "Projekt-B", etc.

    -- 5-Dimension Configuration (JSON)
    config JSON NOT NULL,

    -- Statistics
    total_tasks INTEGER DEFAULT 0,
    successful_tasks INTEGER DEFAULT 0,
    avg_quality FLOAT DEFAULT 0.0,
    total_cost FLOAT DEFAULT 0.0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tasks (
    id VARCHAR PRIMARY KEY,
    project_id VARCHAR REFERENCES projects(id),
    issue_number INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    labels JSON,  -- Array of strings
    status ENUM('pending', 'in_progress', 'completed', 'failed') DEFAULT 'pending',

    -- Agent Info
    assigned_agent ENUM('claude', 'gemini', 'copilot', 'cursor', 'windsurf',
                       'openai', 'anthropic', 'google') NOT NULL,
    agent_switches INTEGER DEFAULT 0,

    -- Progress
    current_iteration INTEGER DEFAULT 0,
    max_iterations INTEGER DEFAULT 5,
    current_quality FLOAT DEFAULT 0.0,

    -- Results
    final_quality FLOAT,
    tests_passing BOOLEAN DEFAULT FALSE,
    security_issues INTEGER DEFAULT 0,

    -- Timing
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds FLOAT,

    -- Cost
    estimated_cost FLOAT DEFAULT 0.0,
    actual_cost FLOAT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- QUALITY & METRICS TABLES
-- ============================================================================

CREATE TABLE quality_snapshots (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR REFERENCES tasks(id),
    iteration INTEGER NOT NULL,

    -- Quality Metrics (7 Dimensions)
    overall_quality FLOAT NOT NULL,
    test_coverage FLOAT DEFAULT 0.0,
    tests_passing BOOLEAN DEFAULT FALSE,
    security_score FLOAT DEFAULT 0.0,
    code_quality_score FLOAT DEFAULT 0.0,
    type_safety FLOAT DEFAULT 0.0,
    documentation FLOAT DEFAULT 0.0,

    -- Details
    vulnerabilities INTEGER DEFAULT 0,
    type_errors INTEGER DEFAULT 0,
    complexity FLOAT DEFAULT 0.0,
    failing_test_count INTEGER,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cost_tracking (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR REFERENCES projects(id),
    task_id VARCHAR REFERENCES tasks(id),
    agent ENUM('claude', 'gemini', 'copilot', etc.) NOT NULL,

    tokens_used INTEGER DEFAULT 0,
    cost FLOAT NOT NULL,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE agent_switches (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR REFERENCES tasks(id),
    from_agent ENUM(...) NOT NULL,
    to_agent ENUM(...) NOT NULL,
    reason VARCHAR NOT NULL,
    trigger VARCHAR NOT NULL,  -- "quality_drop", "checkpoint_fail", etc.
    cost_impact FLOAT DEFAULT 0.0,

    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- HRM CONFIGURATION TABLES
-- ============================================================================

CREATE TABLE hrm_configs (
    id VARCHAR PRIMARY KEY,  -- UUID
    project_id VARCHAR REFERENCES projects(id),
    task_id VARCHAR REFERENCES tasks(id),

    -- Core fields
    name VARCHAR,
    config JSON NOT NULL,  -- Complete HRM configuration
    created_by VARCHAR,

    -- Legacy/Metadata
    dimension_config JSON,
    agent_preferences JSON,

    -- Resource Constraints
    max_iterations INTEGER DEFAULT 5,
    max_cost FLOAT,
    max_duration_seconds FLOAT,

    -- Quality Thresholds
    quality_threshold FLOAT DEFAULT 0.8,
    test_coverage_threshold FLOAT DEFAULT 0.8,
    security_threshold FLOAT DEFAULT 0.9,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_preset BOOLEAN DEFAULT FALSE,
    preset_name VARCHAR,

    -- Usage Tracking
    total_executions INTEGER DEFAULT 0,
    successful_executions INTEGER DEFAULT 0,
    total_tokens_used INTEGER DEFAULT 0,
    total_cost FLOAT DEFAULT 0.0,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE hrm_config_history (
    id SERIAL PRIMARY KEY,
    config_id VARCHAR REFERENCES hrm_configs(id),

    changed_by VARCHAR NOT NULL,
    change_type VARCHAR NOT NULL,  -- 'created', 'updated', 'deleted', 'preset_applied'

    old_config JSON,
    new_config JSON NOT NULL,
    task_id VARCHAR REFERENCES tasks(id),
    impact_metrics JSON,  -- Predicted impact

    -- Legacy
    changes JSON,
    reason VARCHAR,
    config_snapshot JSON,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE hrm_presets (
    id VARCHAR PRIMARY KEY,  -- UUID
    name VARCHAR UNIQUE NOT NULL,
    description TEXT,

    -- UI Metadata
    icon VARCHAR,  -- Emoji or icon identifier
    color VARCHAR,  -- Hex color code
    visibility VARCHAR DEFAULT 'private',  -- 'private', 'shared', 'public'

    is_builtin BOOLEAN DEFAULT FALSE,
    created_by VARCHAR,

    config JSON NOT NULL,

    -- Usage Stats
    usage_count INTEGER DEFAULT 0,
    total_cost_saved FLOAT DEFAULT 0.0,
    avg_quality FLOAT,
    avg_cost FLOAT,
    avg_duration_seconds FLOAT,
    last_used_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- API KEYS & LOAD BALANCING
-- ============================================================================

CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,

    provider VARCHAR NOT NULL,  -- 'claude', 'gemini', 'copilot', etc.
    key_name VARCHAR NOT NULL,
    encrypted_key VARCHAR NOT NULL,

    is_active BOOLEAN DEFAULT TRUE,
    last_used TIMESTAMP,
    created_by VARCHAR NOT NULL,

    -- Rate Limits
    daily_requests INTEGER DEFAULT 0,
    monthly_requests INTEGER DEFAULT 0,
    current_usage INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE load_balancing_configs (
    id SERIAL PRIMARY KEY,

    provider VARCHAR NOT NULL,
    project_id VARCHAR REFERENCES projects(id),

    strategy VARCHAR DEFAULT 'round_robin',  -- 'round_robin', 'least_busy', 'cost_optimized'
    provider_weights JSON NOT NULL,

    max_concurrent_tasks INTEGER DEFAULT 5,
    queue_timeout_seconds INTEGER DEFAULT 300,

    -- Circuit Breaker
    failure_threshold FLOAT DEFAULT 0.5,
    recovery_timeout_seconds INTEGER DEFAULT 300,

    -- Performance Tracking
    total_requests INTEGER DEFAULT 0,
    successful_requests INTEGER DEFAULT 0,
    failed_requests INTEGER DEFAULT 0,
    avg_response_time_ms FLOAT DEFAULT 0.0,

    is_enabled BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- SWARM & ORCHESTRATION
-- ============================================================================

CREATE TABLE swarm_configs (
    id SERIAL PRIMARY KEY,

    name VARCHAR NOT NULL,
    project_id VARCHAR REFERENCES projects(id),

    agents_config JSON NOT NULL,
    coordination_mode VARCHAR DEFAULT 'hierarchical',  -- 'hierarchical', 'peer', 'delegator'
    leader_agent ENUM(...),

    communication_config JSON NOT NULL,

    swarm_size INTEGER DEFAULT 3,
    consensus_threshold FLOAT DEFAULT 0.66,
    max_parallel_tasks INTEGER DEFAULT 5,

    -- Performance
    total_swarm_executions INTEGER DEFAULT 0,
    successful_swarm_executions INTEGER DEFAULT 0,
    consensus_agreements INTEGER DEFAULT 0,
    consensus_disagreements INTEGER DEFAULT 0,

    is_active BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- SPECKIT & FEATURES
-- ============================================================================

CREATE TABLE speckit_features (
    id SERIAL PRIMARY KEY,

    feature_name VARCHAR UNIQUE NOT NULL,
    feature_version VARCHAR DEFAULT '1.0',
    description TEXT,
    feature_config JSON NOT NULL,

    integration_points JSON NOT NULL,
    dependencies JSON DEFAULT '[]',

    is_enabled BOOLEAN DEFAULT TRUE,
    is_beta BOOLEAN DEFAULT FALSE,

    -- Usage & Performance
    usage_count INTEGER DEFAULT 0,
    total_executions INTEGER DEFAULT 0,
    successful_executions INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    avg_execution_time_ms FLOAT DEFAULT 0.0,

    optimization_potential FLOAT DEFAULT 0.0,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- SYSTEM METRICS
-- ============================================================================

CREATE TABLE system_metrics (
    id SERIAL PRIMARY KEY,

    metric_timestamp TIMESTAMP NOT NULL,

    -- CPU & Memory
    cpu_usage_percent FLOAT DEFAULT 0.0,
    memory_usage_percent FLOAT DEFAULT 0.0,

    -- Agent Performance
    agents_active INTEGER DEFAULT 0,
    agents_idle INTEGER DEFAULT 0,
    agents_busy INTEGER DEFAULT 0,

    -- Task Metrics
    tasks_pending INTEGER DEFAULT 0,
    tasks_running INTEGER DEFAULT 0,
    tasks_completed INTEGER DEFAULT 0,
    avg_task_duration_seconds FLOAT DEFAULT 0.0,

    -- Cost Metrics
    hourly_cost FLOAT DEFAULT 0.0,
    daily_cost FLOAT DEFAULT 0.0,
    monthly_cost FLOAT DEFAULT 0.0,

    -- Quality Metrics
    avg_quality_score FLOAT DEFAULT 0.0,
    test_pass_rate FLOAT DEFAULT 0.0,
    security_score FLOAT DEFAULT 0.0,

    -- Network & API
    api_calls_total INTEGER DEFAULT 0,
    api_calls_failed INTEGER DEFAULT 0,
    api_avg_latency_ms FLOAT DEFAULT 0.0,

    -- Throughput
    throughput_tasks_per_hour FLOAT DEFAULT 0.0,
    throughput_tokens_per_second FLOAT DEFAULT 0.0,

    -- Resource Utilization
    queue_depth INTEGER DEFAULT 0,
    cache_hit_rate FLOAT DEFAULT 0.0,

    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Routes & Endpoints

### Vollständige API-Übersicht

```
BASE URL: http://localhost:1336/api

=== HRM Configuration (/api/hrm) ===
POST   /hrm/config                    # Update HRM configuration
GET    /hrm/config                    # Get current HRM configuration
GET    /hrm/config/presets            # Get all HRM presets
POST   /hrm/config/presets            # Create custom preset
PUT    /hrm/config/presets/:id        # Update preset
DELETE /hrm/config/presets/:id        # Delete preset
POST   /hrm/config/presets/:id/apply  # Apply preset to project
POST   /hrm/simulate                  # Simulate config impact
GET    /hrm/config/history/:id        # Get config change history

=== Agent Configuration (/api/agents) ===
GET    /agents/connections            # Get all agent connections
GET    /agents/connections/:id        # Get specific agent connection
POST   /agents/connections            # Create agent connection
PUT    /agents/connections/:id        # Update agent connection
DELETE /agents/connections/:id        # Delete agent connection
GET    /agents/files                  # Get all agent config files
GET    /agents/files/:path            # Get specific config file
PUT    /agents/files/:path            # Update config file
POST   /agents/files                  # Create new config file
DELETE /agents/files/:path            # Delete config file

=== Projects (/api/projects) ===
GET    /projects                      # List all projects
GET    /projects/:id                  # Get project details
POST   /projects                      # Create new project
PUT    /projects/:id                  # Update project
DELETE /projects/:id                  # Delete project
GET    /projects/:id/tasks            # Get project tasks
POST   /projects/:id/sync-issues      # Sync GitHub issues

=== Tasks (/api/tasks) ===
GET    /tasks                         # List all tasks
GET    /tasks/:id                     # Get task details
POST   /tasks                         # Create new task
PUT    /tasks/:id                     # Update task
DELETE /tasks/:id                     # Delete task
POST   /tasks/:id/start               # Start task execution
POST   /tasks/:id/retry               # Retry failed task
GET    /tasks/:id/quality-history     # Get quality snapshots

=== Metrics (/api/metrics) ===
GET    /metrics/dashboard             # Dashboard overview stats
GET    /metrics/quality-trends        # Quality trends over time
GET    /metrics/cost-analytics        # Cost analysis
GET    /metrics/agent-performance     # Agent performance comparison
GET    /metrics/task-distribution     # Task distribution by status

=== Configuration (/api/config) ===
GET    /config/defaults               # Get default configurations
GET    /config/validate               # Validate configuration
POST   /config/reset                  # Reset to defaults

=== Prometheus (/api/prometheus) ===
GET    /prometheus/metrics            # Prometheus metrics endpoint

=== SpecKit (/api/speckit) ===
POST   /speckit/generate-spec         # Generate spec from issue
GET    /speckit/features              # List SpecKit features
POST   /speckit/execute               # Execute spec-driven workflow

=== API Keys (/api/api-keys) ===
GET    /api-keys                      # List all API keys
GET    /api-keys/:id                  # Get API key details
POST   /api-keys                      # Create new API key
PUT    /api-keys/:id                  # Update API key
DELETE /api-keys/:id                  # Delete API key
POST   /api-keys/:id/rotate           # Rotate API key

=== Swarm (/api/swarm) ===
GET    /swarm/configs                 # List swarm configurations
GET    /swarm/configs/:id             # Get swarm config
POST   /swarm/configs                 # Create swarm config
PUT    /swarm/configs/:id             # Update swarm config
DELETE /swarm/configs/:id             # Delete swarm config
POST   /swarm/execute                 # Execute swarm task

=== Templates (/api/templates) ===
GET    /templates                     # List project templates
GET    /templates/:id                 # Get template details
POST   /templates/:id/apply           # Apply template to project

=== System Health (/api/health) ===
GET    /health                        # System health check
GET    /cache-stats                   # Cache statistics
POST   /clear-cache                   # Clear cache layers

=== WebSocket (ws://localhost:1336) ===
EVENT  hrm:config:update              # HRM config changed
EVENT  hrm:preset:applied             # Preset applied
EVENT  task:progress                  # Task progress update
EVENT  task:completed                 # Task completed
EVENT  task:failed                    # Task failed
EVENT  system:alert                   # System alert
EVENT  quality:update                 # Quality metrics update
```

---

## Guidelines & Configurations System

### Hierarchisches Layer-System

```
Guidelines-Hierarchie:
├── LAYER-0: Universal Standards (CRITICAL-NO-EMOJIS.md)
│   ├── NO EMOJIS IN CODE, DOCS, COMMITS
│   ├── Clean Code Principles
│   ├── Security First
│   └── Type Safety
│
├── LAYER-1: MCP Server Usage
│   ├── filesystem, memory, github
│   ├── sequential-thinking, perplexity
│   └── browser-tools, postmancer
│
└── LAYER-2: AI CLI Agent-Specific
    ├── LAYER-2-CLAUDE.md (Claude-spezifisch)
    │   ├── Security First Mindset
    │   ├── Comprehensive Error Handling
    │   ├── Strong Type Safety
    │   ├── Architectural Thinking
    │   ├── Documentation Excellence
    │   └── Quality Targets (≥90% type coverage, ≥80% test coverage)
    │
    ├── LAYER-2-COPILOT.md (Copilot-spezifisch)
    │   ├── GitHub Actions & CI/CD
    │   ├── Pull Request Automation
    │   ├── Issue Management
    │   ├── Code Completion & Refactoring
    │   └── Boilerplate Generation
    │
    └── LAYER-2-GEMINI.md (Gemini-spezifisch)
        ├── Bulk Documentation Generation
        ├── Large-Scale Analysis (2M context)
        ├── Data Processing
        ├── Code Migration
        └── Cost Optimization (FREE tier, 1000 req/day)
```

### Agent-Spezifische Guidelines

**Claude (LAYER-2-CLAUDE.md):**
- **Use Cases:** Security, Architecture, Complex Problems
- **Cost:** $20/mo (Claude Pro)
- **Strengths:** Code Quality, Security Awareness, Best Practices
- **Quality Targets:**
  - Type Coverage: ≥90%
  - Test Coverage: ≥80%
  - Cyclomatic Complexity: ≤10 per function
  - Security: Bandit/Semgrep passing (no high/critical issues)
- **When to Use:** Security-critical, architecture decisions, complex debugging

**Gemini (LAYER-2-GEMINI.md):**
- **Use Cases:** Bulk Docs, Large-Scale Analysis, High-Volume Tasks
- **Cost:** FREE (1000 requests/day, 2M token context)
- **Strengths:** Massive Context, Cost-Free, Fast Processing
- **Optimal For:**
  - Documentation: ⭐⭐⭐⭐⭐
  - Bulk Refactoring: ⭐⭐⭐⭐⭐
  - Data Analysis: ⭐⭐⭐⭐⭐
  - Security Audit: ⭐⭐⭐ (use Claude if critical)
- **When to Use:** Cost optimization, bulk ops, large codebase analysis

**Copilot (LAYER-2-COPILOT.md):**
- **Use Cases:** GitHub Workflows, Quick Fixes, Boilerplate
- **Cost:** FREE (Individual) / $10/mo (Pro)
- **Strengths:** GitHub Integration, Real-time IDE Assistance
- **Optimal For:**
  - GitHub Workflows: ⭐⭐⭐⭐⭐
  - Boilerplate Code: ⭐⭐⭐⭐⭐
  - Quick Fixes: ⭐⭐⭐⭐
  - Complex Architecture: ⭐⭐ (use Claude instead)
- **When to Use:** GitHub-specific ops, quick iterations, IDE integration

### Guideline-Datei-Speicherorte

```
lazy-bird/guidelines/
├── CRITICAL-NO-EMOJIS.md        # LAYER-0 (Universal)
├── claude-guidelines.md         # DEPRECATED (migrated to layers/)
├── copilot-guidelines.md        # DEPRECATED
├── gemini-guidelines.md         # DEPRECATED
├── __init__.py
├── tools/
│   └── guideline-injector.py   # Automatic Injection into Agent Context
└── layers/
    ├── LAYER-0.md              # Universal Standards
    ├── LAYER-1.md              # MCP Server Usage
    ├── LAYER-2.md              # AI CLI General
    ├── LAYER-2-CLAUDE.md       # Claude-Specific
    ├── LAYER-2-COPILOT.md      # Copilot-Specific
    └── LAYER-2-GEMINI.md       # Gemini-Specific
```

### Guideline Injection Process

```python
# guideline-injector.py
class GuidelineInjector:
    """Automatically inject guidelines into agent context"""

    def inject_guidelines(self, agent: str, context: str) -> str:
        """
        Inject hierarchical guidelines into agent context

        Order:
        1. LAYER-0: Universal Standards (CRITICAL-NO-EMOJIS)
        2. LAYER-1: MCP Server Usage
        3. LAYER-2: Agent-specific guidelines
        """
        guidelines = []

        # Layer 0: Universal
        guidelines.append(self.load_guideline("LAYER-0.md"))

        # Layer 1: MCP
        guidelines.append(self.load_guideline("LAYER-1.md"))

        # Layer 2: Agent-specific
        if agent == "claude":
            guidelines.append(self.load_guideline("LAYER-2-CLAUDE.md"))
        elif agent == "gemini":
            guidelines.append(self.load_guideline("LAYER-2-GEMINI.md"))
        elif agent == "copilot":
            guidelines.append(self.load_guideline("LAYER-2-COPILOT.md"))

        # Combine guidelines + context
        full_context = "\n\n".join(guidelines) + "\n\n" + context
        return full_context
```

---

## Docker & Container-Orchestrierung

### Docker-Compose Struktur

**Zwei Docker-Compose-Setups:**

1. **Dashboard (`dashboard/docker-compose.yml`)**
   - Frontend (React, Port 1337)
   - Backend (FastAPI, Port 1336)
   - PostgreSQL (Port 5432)
   - Redis (Port 6379)
   - Prometheus (Port 9090)
   - Grafana (Port 1338)
   - Exporters (postgres-exporter, redis-exporter, node-exporter)

2. **LazyBird (`lazy-bird/docker-compose.multiplatform.yml`)**
   - LazyBird App (Python, Port 8000)
   - PostgreSQL (Port 5432)
   - Redis (Port 6379)
   - Prometheus (Port 9090)
   - Grafana (Port 3001)
   - Multi-Platform Support (linux/amd64, linux/arm64)

### Volume Mounts & Data Persistence

```yaml
# dashboard/docker-compose.yml
volumes:
  - ./backend:/app                    # Backend Code (Hot Reload)
  - ../lazy-bird:/lazy-bird          # LazyBird Module (Mounted)
  - postgres_data:/var/lib/postgresql/data
  - redis_data:/data
  - prometheus_data:/prometheus
  - grafana_data:/var/lib/grafana
```

### Netzwerk-Topologie

```
phantom-cortex-network (Dashboard)
├── backend (phantom-cortex-backend)     → Port 1336 (exposed)
├── frontend (phantom-cortex-frontend)   → Port 1337 (exposed)
├── database (phantom-cortex-db)         → Port 5432 (exposed)
├── redis (phantom-cortex-redis)         → Port 6379 (exposed)
├── prometheus (phantom-cortex-prometheus) → Port 9090 (exposed)
└── grafana (phantom-cortex-grafana)     → Port 1338 (exposed)

lazy-bird-network (LazyBird)
├── lazy-bird-app                        → Port 8000 (exposed)
├── database (lazy-bird-db)              → Port 5432 (exposed)
├── redis (lazy-bird-redis)              → Port 6379 (exposed)
├── prometheus (lazy-bird-prometheus)    → Port 9090 (exposed)
└── grafana (lazy-bird-grafana)          → Port 3001 (exposed)
```

### Config-Datei-Routing im Docker

**Problem:** Wie greifen Container auf Host-Config-Dateien zu?

**Lösung 1: Volume Mounts (Aktuell)**
```yaml
backend:
  volumes:
    - ./backend:/app
    - ../lazy-bird:/lazy-bird
    - ../.claude:/config/.claude
    - ../.mcp.json:/config/.mcp.json
```

**Lösung 2: Environment Variables**
```yaml
backend:
  environment:
    CLAUDE_CONFIG_DIR: /config/.claude
    MCP_CONFIG_FILE: /config/.mcp.json
    GUIDELINE_DIR: /lazy-bird/guidelines
```

**Zugriff im Backend:**
```python
# dashboard/backend/routers/agents.py
def get_config_root() -> Path:
    """Get config root - works in Docker and local"""
    # In Docker: /config
    # Local: ../
    config_root = os.getenv("CONFIG_ROOT", Path.cwd().parent)
    return Path(config_root)

# Usage
guideline_path = get_config_root() / "lazy-bird" / "guidelines" / "layers" / "LAYER-2-CLAUDE.md"
mcp_config_path = get_config_root() / ".mcp.json"
```

---

## Multi-AI-Agent Integration

### Agent Connections Management

**Gespeichert in:** `lazy-bird/agent_connections.json`

```json
{
  "connections": [
    {
      "agent_id": "claude-code",
      "agent_name": "Claude Code",
      "connection_type": "api",
      "endpoint": "https://api.anthropic.com/v1",
      "api_key_id": "api_key_1",
      "enabled": true
    },
    {
      "agent_id": "gemini-ai",
      "agent_name": "Google Gemini",
      "connection_type": "api",
      "endpoint": "https://generativelanguage.googleapis.com/v1",
      "api_key_id": "api_key_2",
      "enabled": true
    },
    {
      "agent_id": "copilot",
      "agent_name": "GitHub Copilot",
      "connection_type": "api",
      "endpoint": "https://api.github.com",
      "api_key_id": "api_key_3",
      "enabled": true
    },
    {
      "agent_id": "openhands",
      "agent_name": "OpenHands",
      "connection_type": "local",
      "endpoint": "http://localhost:3000",
      "enabled": true
    }
  ]
}
```

### Smart Agent Switching Logic (ADR-005)

**Entscheidungsbaum:**
```
Issue Created
   │
   ▼
Classify Task Complexity
   ├── SIMPLE (<150 LOC, no arch)
   │   └─► Gemini (FREE, fast)
   │
   ├── MEDIUM (150-500 LOC, standard)
   │   └─► Copilot ($10/mo, good balance)
   │
   └── COMPLEX (>500 LOC, arch, security)
       └─► Claude ($20/mo, best quality)

Mid-Task Checkpoints (33%, 66%, 100%)
   │
   ▼
Evaluate Quality
   ├── Quality >= Target
   │   └─► Continue with current agent
   │
   └── Quality < Target (by 20%+)
       └─► Switch Agent
           ├── Gemini → Copilot or Claude
           ├── Copilot → Claude
           └── Claude → Claude (already best)
```

**Cost-Benefit Analysis:**
```python
def should_switch_agent(current: str, proposed: str,
                       quality_gap: float, remaining_budget: float) -> bool:
    """
    Switch if: Quality Improvement > Cost Increase (relative)

    Example:
    - Current: Gemini ($0.001/call, 0.65 quality)
    - Proposed: Claude ($0.08/call, 0.95 quality)
    - Quality Improvement: 46%
    - Cost Increase: 8000%
    - Quality per $ Ratio: 46% / 8000% = 0.00575
    - Threshold: 0.8 (configurable)
    - Decision: SWITCH if quality_gap > 20%
    """
    cost_delta = agent_costs[proposed] - agent_costs[current]
    quality_improvement = agent_quality[proposed] - agent_quality[current]

    if quality_improvement > 0 and cost_delta < remaining_budget:
        cost_ratio = cost_delta / agent_costs[current]
        quality_ratio = quality_improvement / agent_quality[current]

        if quality_ratio > (cost_ratio * 0.8):
            return True
    return False
```

### Integration mit Rover CLI

**Rover Adapter (`lazy-bird/scripts/rover-adapter.py`):**
```python
class RoverAdapter:
    """Bridge zwischen LazyBird und Rover CLI"""

    def create_task(self, issue_data, project_config, agent):
        """
        GitHub Issue → Rover Task

        cmd: ["rover", "task", description, "--agent", agent,
              "--project", path, "--issue", number]
        """
        pass

    def monitor_task(self, rover_task_id):
        """Poll Rover task status"""
        pass

    def get_test_results(self, rover_task_id):
        """Extract test results from Rover workspace"""
        pass

    def merge_or_retry(self, rover_task_id, test_status):
        """Decision: merge PR or retry with different agent"""
        if all_tests_passed:
            return self._merge_task(rover_task_id)
        elif should_retry:
            return self._retry_task_with_better_agent(rover_task_id)
        else:
            return "failed"
```

### Integration mit OpenHands

**OpenHands Config (`.openhands/config.toml`):**
```toml
[security]
confirmation_mode = "disabled"
auto_approve = true
allow_shell_execute = true
allow_git_operations = true

[agent]
autonomous_mode = true
max_iterations = 20
enable_web_browsing = true
auto_commit = true
auto_push = true

[sandbox]
enable_sandbox = true
allow_workspace_access = true
allow_network_access = true
```

**Collaboration Pattern:**
```
1. GitHub Issue Created
   ↓
2. LazyBird Routes to OpenHands (for autonomous implementation)
   ↓
3. OpenHands Implements Feature
   ↓
4. OpenHands Creates PR
   ↓
5. Claude Reviews (@code-expert via MCP)
   ↓
6. Copilot Applies Review Feedback
   ↓
7. CI/CD Auto-Merge (if tests pass)
```

---

## MCP Server-Integration

### 14 Verfügbare MCP Server

**`.mcp.json`:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx -y @modelcontextprotocol/server-filesystem",
      "args": ["C:\\Users\\Thomas\\Desktop\\claude config"]
    },
    "memory": {
      "command": "npx -y @modelcontextprotocol/server-memory"
    },
    "github": {
      "command": "npx -y @modelcontextprotocol/server-github",
      "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    },
    "brave-search": {
      "command": "npx -y @modelcontextprotocol/server-brave-search",
      "env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"}
    },
    "sequential-thinking": {
      "command": "npx -y @modelcontextprotocol/server-sequential-thinking"
    },
    "gemini-cli": {
      "command": "npx -y gemini-mcp-tool",
      "env": {"GOOGLE_API_KEY": "${GOOGLE_API_KEY}"}
    },
    "perplexity": {
      "command": "npx -y @perplexity-ai/mcp-server",
      "env": {"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}
    },
    "browser-tools": {
      "command": "npx -y @executeautomation/playwright-mcp-server"
    },
    "sqlite": {
      "command": "npx -y @modelcontextprotocol/server-sqlite",
      "args": ["--db-path", "C:\\Users\\Thomas\\Desktop\\claude config\\data.db"]
    },
    "postgres": {
      "command": "npx -y @modelcontextprotocol/server-postgres",
      "env": {"POSTGRES_URL": "${DATABASE_URL}"}
    },
    "time": {
      "command": "npx -y mcp-server-time"
    },
    "postmancer": {
      "command": "npx -y postmancer"
    },
    "docs": {
      "command": "npx -y docs-mcp-server"
    },
    "copilot-cli": {
      "command": "npx -y copilot-mcp-server",
      "env": {
        "COPILOT_MODEL": "claude-sonnet-4.5",
        "COPILOT_ALLOW_ALL_TOOLS": "false"
      }
    }
  }
}
```

### MCP Server Usage Patterns

**filesystem:**
- Read/Write config files
- Access guideline markdown files
- Manage agent connections JSON

**memory:**
- Store architectural decisions
- Remember HRM config changes
- Track task context across sessions

**github:**
- Fetch issues
- Create PRs
- Sync repository state

**sequential-thinking:**
- Multi-step architectural planning
- Complex algorithm design
- Security analysis with attack trees

**gemini-cli:**
- Direct Gemini API access
- Bulk operations
- Large-scale analysis

**perplexity:**
- Web search for documentation
- Up-to-date tech info
- Best practices lookup

**browser-tools (Playwright):**
- E2E testing
- UI validation
- Screenshot capture

**postmancer:**
- API testing
- Integration tests
- Endpoint validation

**postgres:**
- Database schema inspection
- Query execution
- Data analysis

---

## Datenflüsse & State Management

### HRM Config Update Flow

```
User Changes HRM Config in UI
   │
   ▼
Frontend: POST /api/hrm/config
   │
   ▼
Backend: hrm.update_hrm_config()
   │
   ├─► Calculate Impact (cost, speed, quality, tokens)
   │   └─► calculate_impact_estimate(old_config, new_config)
   │
   ├─► Save to Database (hrm_configs table)
   │   └─► HRMConfig.update(config=new_config)
   │
   ├─► Log History (hrm_config_history table)
   │   └─► HRMConfigHistory.create(old_config, new_config, impact)
   │
   ├─► Emit WebSocket Event
   │   └─► emit_hrm_config_update(project_id, config_id, impact)
   │
   └─► Return Response
       └─► {status, config_id, impact_estimate, active_tasks_affected}
```

### Task Execution Flow mit Agent Switching

```
GitHub Issue Created (#42)
   │
   ▼
Backend: POST /api/tasks
   │
   ├─► Classify Task Complexity
   │   └─► classify_task_complexity(issue, code) → MEDIUM
   │
   ├─► Route to Agent (Smart Agent Switcher)
   │   └─► decide_initial_agent(task) → Copilot
   │
   ├─► Get HRM Config for Project
   │   └─► HRMConfig.get_for_project(project_id)
   │
   ├─► Execute Task with Agent
   │   │
   │   ├─► Iteration 1: Copilot.refine(code, issue)
   │   │   └─► Quality: 72%
   │   │
   │   ├─► Iteration 2: Copilot.refine(code, issue)
   │   │   └─► Quality: 75%
   │   │
   │   ├─► CHECKPOINT @ Iteration 3 (33%)
   │   │   ├─► Evaluate Quality: 78% (below target 85%)
   │   │   ├─► Quality Gap: -7%
   │   │   └─► SWITCH AGENT: Copilot → Claude
   │   │
   │   ├─► Iteration 3: Claude.refine(code, issue)
   │   │   └─► Quality: 82%
   │   │
   │   ├─► Iteration 4: Claude.refine(code, issue)
   │   │   └─► Quality: 87%
   │   │
   │   └─► CHECKPOINT @ Iteration 6 (66%)
   │       ├─► Evaluate Quality: 87% (meets target)
   │       └─► Continue with Claude
   │
   ├─► Final Quality Evaluation
   │   └─► 87% quality, all tests passing, 0 security issues
   │
   ├─► Record Metrics
   │   ├─► QualitySnapshot(task_id, iteration, quality=87%)
   │   ├─► CostTracking(task_id, agent=Claude, cost=$0.10)
   │   └─► AgentSwitch(from=Copilot, to=Claude, reason=quality_drop)
   │
   ├─► Emit WebSocket Events
   │   ├─► emit("task:progress", {task_id, iteration, quality})
   │   └─► emit("task:completed", {task_id, quality, cost})
   │
   └─► Return Result
       └─► {status: "completed", quality: 87%, cost: $0.10}
```

### Real-time State Synchronization

```
Database Update
   │
   ▼
WebSocket Emit
   │
   ├─► Frontend receives event
   │   └─► Update React state (Zustand/Context)
   │       └─► Re-render components
   │
   └─► Monitoring Dashboard receives event
       └─► Update Grafana panels
```

---

## Real-time Updates (WebSocket)

### WebSocket Architecture

**Backend: `routers/websocket.py`**
```python
import socketio

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)

# Event emitters
async def emit_hrm_config_update(project_id, config_id, config_data, impact):
    await sio.emit('hrm:config:update', {
        'project_id': project_id,
        'config_id': config_id,
        'config': config_data,
        'impact': impact
    })

async def emit_task_progress(task_id, iteration, quality, status):
    await sio.emit('task:progress', {
        'task_id': task_id,
        'iteration': iteration,
        'quality': quality,
        'status': status
    })

async def emit_system_alert(message, severity):
    await sio.emit('system:alert', {
        'message': message,
        'severity': severity,
        'timestamp': datetime.utcnow().isoformat()
    })
```

**Frontend: `src/lib/api.ts`**
```typescript
import { io } from 'socket.io-client';

const socket = io('http://localhost:1336', {
  transports: ['websocket', 'polling']
});

// Listen for HRM config updates
socket.on('hrm:config:update', (data) => {
  console.log('HRM Config updated:', data);
  updateStore(data);  // Update Zustand store
});

// Listen for task progress
socket.on('task:progress', (data) => {
  updateTaskProgress(data.task_id, data.iteration, data.quality);
});

// Listen for system alerts
socket.on('system:alert', (data) => {
  showNotification(data.message, data.severity);
});
```

### WebSocket Events

| Event Name | Direction | Payload | Trigger |
|------------|-----------|---------|---------|
| `hrm:config:update` | Backend → Frontend | `{project_id, config_id, config, impact}` | HRM config changed |
| `hrm:preset:applied` | Backend → Frontend | `{project_id, preset_name, config}` | Preset applied |
| `task:progress` | Backend → Frontend | `{task_id, iteration, quality, status}` | Task iteration complete |
| `task:completed` | Backend → Frontend | `{task_id, quality, cost, duration}` | Task finished |
| `task:failed` | Backend → Frontend | `{task_id, error, iteration}` | Task failed |
| `quality:update` | Backend → Frontend | `{task_id, quality_scores}` | Quality snapshot |
| `agent:switched` | Backend → Frontend | `{task_id, from_agent, to_agent, reason}` | Agent switch occurred |
| `system:alert` | Backend → Frontend | `{message, severity, timestamp}` | System event |

---

## Monitoring & Observability

### Prometheus Metrics

**Exported Metrics (`lazy-bird/monitoring/prometheus_exporter.py`):**
```python
from prometheus_client import Counter, Histogram, Gauge

# Task Metrics
task_total = Counter('lazybird_task_total', 'Total tasks executed')
task_success = Counter('lazybird_task_success', 'Successful tasks')
task_failures = Counter('lazybird_task_failures', 'Failed tasks')
task_duration = Histogram('lazybird_task_duration_seconds', 'Task duration')

# Quality Metrics
quality_score = Gauge('lazybird_quality_score', 'Average quality score')
test_coverage = Gauge('lazybird_test_coverage', 'Test coverage percentage')
security_score = Gauge('lazybird_security_score', 'Security score')

# Cost Metrics
cost_total = Counter('lazybird_cost_total_usd', 'Total cost in USD')
tokens_used = Counter('lazybird_tokens_used', 'Total tokens consumed')
agent_cost = Counter('lazybird_agent_cost_usd', 'Cost per agent', ['agent'])

# Agent Switching Metrics
agent_switches = Counter('lazybird_agent_switches', 'Agent switches', ['from_agent', 'to_agent'])
agent_switch_savings = Gauge('lazybird_agent_switch_savings_usd', 'Cost savings from switching')
agent_routing_accuracy = Gauge('lazybird_agent_routing_accuracy', 'Routing accuracy %')

# HRM Config Metrics
hrm_config_changes = Counter('lazybird_hrm_config_changes', 'HRM config changes')
latent_reasoning_enabled = Gauge('lazybird_latent_reasoning_enabled', 'Latent reasoning active')
parallel_workers = Gauge('lazybird_parallel_workers', 'Parallel evaluation workers')

# Cache Metrics
cache_hits = Counter('lazybird_cache_hits', 'Cache hits', ['layer'])
cache_misses = Counter('lazybird_cache_misses', 'Cache misses', ['layer'])
cache_hit_rate = Gauge('lazybird_cache_hit_rate', 'Cache hit rate', ['layer'])
```

### Grafana Dashboards

**Dashboard Panels:**
1. **Task Overview**
   - Total tasks (today, this week, this month)
   - Success rate (%)
   - Average duration
   - Active tasks

2. **Quality Metrics**
   - Average quality score (line chart over time)
   - Test coverage (gauge)
   - Security score (gauge)
   - Quality distribution (histogram)

3. **Cost Analytics**
   - Total cost (today, this week, this month)
   - Cost per agent (pie chart)
   - Cost trend (line chart)
   - Savings from agent switching

4. **Agent Performance**
   - Agent usage distribution
   - Agent success rates
   - Agent switch frequency
   - Agent routing accuracy

5. **HRM Optimization**
   - Latent reasoning compression ratio
   - Token reduction (%)
   - Parallel evaluation speedup
   - Cache hit rates by layer

6. **System Health**
   - CPU usage
   - Memory usage
   - Database connections
   - WebSocket connections
   - API response times

---

## Enterprise Deployment Guide

### Production Deployment Checklist

**1. Environment Setup**
```bash
# Set environment variables
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
export REDIS_URL="redis://host:6379/0"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxx"
export GOOGLE_API_KEY="AIzaxxxxxxxxxxxx"

# Security
export SECRET_KEY="your-secret-key"
export JWT_SECRET="your-jwt-secret"
```

**2. Database Migration**
```bash
# Run migrations
cd dashboard/backend
python -c "from database import init_db; init_db()"

# Seed initial data
python seed_data.py
```

**3. Docker Deployment**
```bash
# Build images
docker-compose -f dashboard/docker-compose.yml build
docker-compose -f lazy-bird/docker-compose.multiplatform.yml build

# Start services
docker-compose -f dashboard/docker-compose.yml up -d
docker-compose -f lazy-bird/docker-compose.multiplatform.yml up -d

# Check health
curl http://localhost:1336/api/health
```

**4. Configure Monitoring**
```bash
# Prometheus: http://localhost:9090
# Grafana: http://localhost:1338 (user: admin, pass: admin)

# Import dashboards
# Dashboard JSON: dashboard/monitoring/grafana/provisioning/dashboards/
```

**5. Verify Integrations**
```bash
# Test MCP servers
curl http://localhost:1336/api/agents/files?file_type=mcp

# Test GitHub integration
curl http://localhost:1336/api/projects/{project_id}/sync-issues

# Test WebSocket
wscat -c ws://localhost:1336
```

### Kubernetes Deployment

**Helm Chart Structure:**
```yaml
phantom-neural-cortex/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml       # Backend/Frontend deployments
│   ├── service.yaml          # ClusterIP services
│   ├── ingress.yaml          # Ingress controller
│   ├── configmap.yaml        # Configuration
│   ├── secrets.yaml          # API keys, passwords
│   ├── pvc.yaml              # Persistent volumes
│   └── hpa.yaml              # Horizontal Pod Autoscaler
```

**Example Deployment:**
```bash
# Install Helm chart
helm install phantom-cortex ./phantom-neural-cortex \
  --set image.tag=latest \
  --set database.host=postgres.default.svc.cluster.local \
  --set redis.host=redis.default.svc.cluster.local

# Scale replicas
kubectl scale deployment phantom-cortex-backend --replicas=3
```

### High Availability (HA) Setup

**Database:**
- PostgreSQL with streaming replication
- PgBouncer for connection pooling
- Automated backups (WAL archiving)

**Redis:**
- Redis Cluster (3 masters, 3 replicas)
- Redis Sentinel for failover

**Backend:**
- 3+ replicas behind load balancer
- Health checks on /api/health
- Graceful shutdown handling

**Frontend:**
- CDN for static assets
- Nginx reverse proxy
- Gzip compression

---

## Best Practices & Patterns

### 1. HRM Configuration Best Practices

**Start with Balanced Preset:**
```python
balanced_config = {
    "latent_reasoning": {"enabled": True, "dimensionality": 512},
    "agent_switching": {"strategy": "adaptive"},
    "deep_supervision": {"enabled": True},
    "parallel_evaluation": {"enabled": True, "worker_count": 4},
    "caching": {"memory": True, "disk": True, "aggressive_mode": True}
}
```

**Tune for Cost Optimization:**
```python
cost_optimized_config = {
    "latent_reasoning": {"enabled": True, "dimensionality": 256},  # Lower dim = cheaper
    "agent_switching": {"strategy": "cost_optimized"},  # Use Gemini when possible
    "parallel_evaluation": {"worker_count": 2},  # Fewer workers
    "caching": {"aggressive_mode": True}  # Max caching
}
```

**Tune for Quality:**
```python
quality_first_config = {
    "latent_reasoning": {"dimensionality": 1024},  # Higher quality
    "agent_switching": {"strategy": "quality_first"},  # Use Claude liberally
    "deep_supervision": {"checkpoints": [0.25, 0.50, 0.75, 1.00]},  # More checks
    "parallel_evaluation": {"worker_count": 8}  # More parallel
}
```

### 2. Agent Selection Guidelines

**Decision Matrix:**
| Task Type | Complexity | Labels | Recommended Agent | Why |
|-----------|------------|--------|-------------------|-----|
| Bug Fix | Simple (<150 LOC) | `bug` | Gemini | Fast, free, sufficient |
| Feature | Medium (150-500 LOC) | `feature` | Copilot | Good balance |
| Security | Any | `security` | Claude | Security expertise |
| Architecture | Complex (>500 LOC) | `architecture` | Claude | Architectural thinking |
| Documentation | Bulk | `docs` | Gemini | 2M context, free |
| Refactor | Simple | `refactor-simple` | Gemini | Cost-effective |
| Refactor | Complex | `refactor` | Claude | Quality matters |

### 3. Guideline Management

**Adding New Guidelines:**
```bash
# Create new layer-specific guideline
touch lazy-bird/guidelines/layers/LAYER-2-CURSOR.md

# Update guideline injector
# Edit: lazy-bird/guidelines/tools/guideline-injector.py
```

**Guideline Validation:**
```python
def validate_guidelines():
    """Ensure all guidelines follow standards"""
    # 1. NO EMOJIS in any guideline
    # 2. Consistent structure (Context, Decision, Consequences)
    # 3. Layer hierarchy respected
    # 4. Agent-specific sections present
    pass
```

### 4. Database Optimization

**Indexes:**
```sql
-- Performance-critical indexes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_project_status ON tasks(project_id, status);
CREATE INDEX idx_quality_snapshots_task ON quality_snapshots(task_id, iteration);
CREATE INDEX idx_hrm_configs_project ON hrm_configs(project_id) WHERE is_active = TRUE;
CREATE INDEX idx_cost_tracking_project_agent ON cost_tracking(project_id, agent);
```

**Query Optimization:**
```python
# Use eager loading for relationships
tasks = db.query(Task).options(
    joinedload(Task.quality_snapshots),
    joinedload(Task.project)
).filter(Task.status == TaskStatus.IN_PROGRESS).all()
```

### 5. Error Handling & Resilience

**Retry Logic with Exponential Backoff:**
```python
import backoff

@backoff.on_exception(
    backoff.expo,
    (ConnectionError, TimeoutError),
    max_tries=5,
    max_time=300
)
def call_agent_api(agent: str, prompt: str):
    """Call agent API with automatic retry"""
    response = agent_clients[agent].refine(prompt)
    return response
```

**Circuit Breaker Pattern:**
```python
from pybreaker import CircuitBreaker

agent_breaker = CircuitBreaker(
    fail_max=5,
    timeout_duration=60,
    name="agent_api"
)

@agent_breaker
def call_agent(agent: str, prompt: str):
    return agent_clients[agent].refine(prompt)
```

### 6. Security Best Practices

**API Key Management:**
```python
from cryptography.fernet import Fernet

class APIKeyManager:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)

    def encrypt_key(self, api_key: str) -> str:
        return self.cipher.encrypt(api_key.encode()).decode()

    def decrypt_key(self, encrypted_key: str) -> str:
        return self.cipher.decrypt(encrypted_key.encode()).decode()
```

**Input Validation:**
```python
from pydantic import BaseModel, validator, Field

class HRMConfigRequest(BaseModel):
    project_id: Optional[str] = Field(None, regex=r'^[a-zA-Z0-9_-]+$')

    @validator('config')
    def validate_config(cls, v):
        # Validate dimensionality range
        if 'latent_reasoning' in v:
            dim = v['latent_reasoning']['dimensionality']
            if not 128 <= dim <= 1024:
                raise ValueError("Dimensionality must be 128-1024")
        return v
```

**Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/hrm/config")
@limiter.limit("100/hour")
async def update_hrm_config(request: Request, ...):
    pass
```

### 7. Testing Strategy

**Unit Tests:**
```python
# test_hrm_config.py
def test_calculate_impact_estimate():
    old_config = {"latent_reasoning": {"dimensionality": 512}}
    new_config = {"latent_reasoning": {"dimensionality": 256}}

    impact = calculate_impact_estimate(old_config, new_config)

    assert impact.cost_change < 0  # Cost reduced
    assert impact.token_reduction > 0  # Tokens reduced
```

**Integration Tests:**
```python
def test_hrm_config_update_flow():
    # 1. Update config via API
    response = client.post("/api/hrm/config", json={...})
    assert response.status_code == 200

    # 2. Verify database update
    config = db.query(HRMConfig).filter(...).first()
    assert config.config == new_config

    # 3. Verify history logged
    history = db.query(HRMConfigHistory).filter(...).first()
    assert history.change_type == "update"
```

**E2E Tests:**
```python
# test_task_execution_e2e.py
async def test_complete_task_flow():
    # 1. Create project
    project = await create_project(...)

    # 2. Create task
    task = await create_task(project_id=project.id, ...)

    # 3. Execute task with agent switching
    result = await execute_task(task.id)

    # 4. Verify quality metrics
    assert result.quality >= 0.8

    # 5. Verify agent switch occurred
    switches = await get_agent_switches(task.id)
    assert len(switches) > 0
```

---

## Zusammenfassung & Nächste Schritte

### Was wurde analysiert:

1. HRM Backend-Architektur (Routes, Models, Database)
2. Guidelines & Configurations System (Layer-Hierarchie)
3. Multi-AI-Agent Integration (Claude, Gemini, Copilot, OpenHands, Rover)
4. MCP Server-Integration (14 MCP Servers)
5. Docker & Container-Orchestrierung
6. Datenflüsse & State Management
7. Real-time Updates (WebSocket)
8. Monitoring & Observability (Prometheus, Grafana)

### Key Findings:

**Stärken:**
- Umfassende ML/RL-Optimierungen (12 ADRs)
- Hierarchisches Layer-System für Guidelines
- Smart Agent Switching (52% cost savings)
- Real-time Configuration Control
- WebSocket-basierte Updates
- Vollständige Monitoring-Integration

**Verbesserungspotenzial:**
- Agent Connection Management (aktuell nur JSON-Datei)
- Guideline Injection noch nicht vollständig automatisiert
- Rover Integration noch nicht vollständig implementiert
- Testing Coverage (Unit/Integration/E2E Tests fehlen teilweise)

### Enterprise Deployment Roadmap:

**Phase 1: Stabilisierung (Woche 1-2)**
- [ ] Vollständige Unit-Test-Coverage (≥80%)
- [ ] Integration Tests für alle API Routes
- [ ] E2E Tests für kritische Flows
- [ ] Security Audit (Bandit, Semgrep)
- [ ] Performance Benchmarks

**Phase 2: Production Readiness (Woche 3-4)**
- [ ] Kubernetes Helm Charts
- [ ] CI/CD Pipeline (GitHub Actions)
- [ ] Automated Backups (PostgreSQL WAL)
- [ ] High Availability Setup (Replicas, Load Balancing)
- [ ] Monitoring Dashboards (Grafana)

**Phase 3: Advanced Features (Woche 5-8)**
- [ ] Multi-Tenancy Support
- [ ] Role-Based Access Control (RBAC)
- [ ] API Rate Limiting per User
- [ ] Audit Logging
- [ ] Advanced Cost Analytics

**Phase 4: Scale & Optimize (Woche 9-12)**
- [ ] Horizontal Scaling Tests (10x load)
- [ ] Database Query Optimization
- [ ] Caching Strategy Refinement
- [ ] Cost Optimization Tuning
- [ ] Documentation & Onboarding

---

**Ende des HRM Enterprise-Architektur-Dokuments**

Für Fragen oder weitere Details, siehe:
- [ADR-Übersicht](./adr/README.md)
- [API-Referenz](./API-REFERENCE.md)
- [Deployment-Guide](../dashboard/DEPLOYMENT.md)
- [Best Practices](./BEST_PRACTICES.md)

**Version:** 3.0.0
**Maintainer:** Phantom Neural Cortex Team
**Lizenz:** MIT
