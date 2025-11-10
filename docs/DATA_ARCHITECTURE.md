# Data Architecture - Complete System Overview

**Version:** 2.0.0
**Last Updated:** 2025-11-10

This document explains how ALL data flows through the system - database, state management, real-time updates, analytics, feedback loops, guidelines, and caching.

---

## Table of Contents

1. [Database Schema](#1-database-schema)
2. [Data Flow Patterns](#2-data-flow-patterns)
3. [State Management](#3-state-management)
4. [Real-time Synchronization](#4-real-time-synchronization)
5. [Analytics Pipeline](#5-analytics-pipeline)
6. [Feedback Loop System](#6-feedback-loop-system)
7. [Guidelines Management](#7-guidelines-management)
8. [Caching Strategy](#8-caching-strategy)
9. [Subagent Coordination](#9-subagent-coordination)
10. [Implementation Guide](#10-implementation-guide)

---

## 1. Database Schema

### Overview

```
Database: SQLite (Dev) / PostgreSQL (Prod)
Engine: SQLAlchemy 2.0 Async (2.5x faster than sync)
Driver: aiosqlite (Dev) / asyncpg (Prod)
Pool Size: 20 connections + 10 overflow
```

### Core Tables (14 Total)

#### 1.1 Projects Table

**Stores project metadata and configuration**

```sql
CREATE TABLE projects (
    id VARCHAR PRIMARY KEY,                    -- UUID
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,                     -- ENUM: python, typescript, react, node, general
    status VARCHAR DEFAULT 'active',           -- ENUM: active, paused, archived
    github_repo VARCHAR NULL,
    slot VARCHAR NOT NULL,                     -- "Projekt-A", "Projekt-B", "Projekt-C"

    -- 5-Dimension Configuration (JSON)
    config JSON NOT NULL,

    -- Statistics (Aggregated)
    total_tasks INTEGER DEFAULT 0,
    successful_tasks INTEGER DEFAULT 0,
    avg_quality FLOAT DEFAULT 0.0,
    total_cost FLOAT DEFAULT 0.0,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW()
);
```

**Config Structure:**
```json
{
  "priority": {
    "mode": "balanced",
    "custom_weights": null
  },
  "timeframe": {
    "max_minutes": 30,
    "preset": "standard"
  },
  "risk_tolerance": {
    "level": 50,
    "allow_experimental": false,
    "ml_features_enabled": true
  },
  "deployment": {
    "targets": ["windows"],
    "docker_enabled": false,
    "kubernetes_enabled": false
  },
  "ml_components": {
    "adaptive_iterations": true,
    "quality_weight_learning": true,
    "latent_reasoning": true,
    "agent_switching": true,
    "inference_time_scaling": true
  }
}
```

#### 1.2 Tasks Table

**Stores individual task execution data**

```sql
CREATE TABLE tasks (
    id VARCHAR PRIMARY KEY,                    -- UUID
    project_id VARCHAR NOT NULL,               -- FK: projects.id
    issue_number INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR NULL,
    labels JSON DEFAULT '[]',                  -- List of strings
    status VARCHAR DEFAULT 'pending',          -- ENUM: pending, in_progress, completed, failed

    -- Agent Assignment
    assigned_agent VARCHAR NOT NULL,           -- ENUM: claude, gemini, copilot, cursor, etc.
    agent_switches INTEGER DEFAULT 0,

    -- Progress Tracking
    current_iteration INTEGER DEFAULT 0,
    max_iterations INTEGER DEFAULT 5,
    current_quality FLOAT DEFAULT 0.0,

    -- Results
    final_quality FLOAT NULL,
    tests_passing BOOLEAN DEFAULT FALSE,
    security_issues INTEGER DEFAULT 0,

    -- Timing
    started_at DATETIME NULL,
    completed_at DATETIME NULL,
    duration_seconds FLOAT NULL,

    -- Cost
    estimated_cost FLOAT DEFAULT 0.0,
    actual_cost FLOAT NULL,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),

    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

#### 1.3 Quality Snapshots Table

**Stores quality metrics at each iteration**

```sql
CREATE TABLE quality_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id VARCHAR NOT NULL,                  -- FK: tasks.id
    iteration INTEGER NOT NULL,

    -- Quality Metrics
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
    failing_test_count INTEGER NULL,

    -- Timestamp
    created_at DATETIME DEFAULT NOW(),

    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
```

#### 1.4 Cost Tracking Table

**Tracks per-agent cost and token usage**

```sql
CREATE TABLE cost_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id VARCHAR NULL,                   -- FK: projects.id
    task_id VARCHAR NULL,                      -- FK: tasks.id
    agent VARCHAR NOT NULL,                    -- ENUM: claude, gemini, copilot, etc.

    -- Cost Details
    tokens_used INTEGER DEFAULT 0,
    cost FLOAT NOT NULL,

    -- Timestamp
    created_at DATETIME DEFAULT NOW(),

    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
);
```

#### 1.5 Agent Switch Table

**Logs agent switching events**

```sql
CREATE TABLE agent_switches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id VARCHAR NOT NULL,                  -- FK: tasks.id
    from_agent VARCHAR NOT NULL,               -- ENUM: claude, gemini, copilot, etc.
    to_agent VARCHAR NOT NULL,
    reason VARCHAR NOT NULL,
    trigger VARCHAR NOT NULL,
    cost_impact FLOAT DEFAULT 0.0,

    -- Timestamp
    created_at DATETIME DEFAULT NOW(),

    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
```

#### 1.6 HRM Config Table

**Stores HRM configurations per project/task**

```sql
CREATE TABLE hrm_configs (
    id VARCHAR PRIMARY KEY,                    -- UUID
    project_id VARCHAR NULL,                   -- FK: projects.id
    task_id VARCHAR NULL,                      -- FK: tasks.id

    -- Core Fields
    name VARCHAR NULL,
    config JSON NOT NULL,                      -- Complete HRM config object
    created_by VARCHAR NULL,

    -- Legacy Fields (Backward Compat)
    dimension_config JSON NULL,
    agent_preferences JSON NULL,

    -- Resource Constraints
    max_iterations INTEGER DEFAULT 5,
    max_cost FLOAT NULL,
    max_duration_seconds FLOAT NULL,

    -- Quality Thresholds
    quality_threshold FLOAT DEFAULT 0.8,
    test_coverage_threshold FLOAT DEFAULT 0.8,
    security_threshold FLOAT DEFAULT 0.9,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_preset BOOLEAN DEFAULT FALSE,
    preset_name VARCHAR NULL,

    -- Usage Tracking
    total_executions INTEGER DEFAULT 0,
    successful_executions INTEGER DEFAULT 0,
    total_tokens_used INTEGER DEFAULT 0,
    total_cost FLOAT DEFAULT 0.0,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),

    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
```

**HRM Config Structure:**
```json
{
  "latent_reasoning": {
    "enabled": true,
    "dimensionality": 512,
    "compression_ratio_target": 3.8,
    "auto_adjust": false
  },
  "ml_iteration_prediction": {
    "mode": "auto",
    "max_iterations": 7,
    "confidence_threshold": 0.80
  },
  "agent_switching": {
    "strategy": "adaptive",
    "quality_drop_threshold": 0.20,
    "cost_ceiling": 5.00,
    "max_switches_per_task": 3
  },
  "deep_supervision": {
    "enabled": true,
    "checkpoints": [0.33, 0.66, 1.00],
    "quality_gate_threshold": 0.75
  },
  "parallel_evaluation": {
    "enabled": true,
    "worker_count": 4,
    "timeout_seconds": 60
  },
  "caching": {
    "memory": true,
    "disk": true,
    "remote": false,
    "aggressive_mode": true,
    "max_size_mb": 500
  },
  "bayesian_optimization": {
    "enabled": false,
    "iterations": 30
  },
  "rl_refinement": {
    "enabled": true,
    "epsilon": 0.1,
    "learning_rate": 0.001
  },
  "prometheus_metrics": {
    "enabled": true,
    "export_interval": 15
  },
  "multi_repo": {
    "enabled": true
  }
}
```

#### 1.7 HRM Config History Table

**Audit log for HRM configuration changes**

```sql
CREATE TABLE hrm_config_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_id VARCHAR NOT NULL,                -- FK: hrm_configs.id

    -- Change Tracking
    changed_by VARCHAR NOT NULL,
    change_type VARCHAR NOT NULL,              -- created, updated, deleted, preset_applied

    -- Router-Compatible Fields
    old_config JSON NULL,
    new_config JSON NOT NULL,
    task_id VARCHAR NULL,                      -- FK: tasks.id
    impact_metrics JSON NULL,

    -- Legacy Fields
    changes JSON NULL,
    reason VARCHAR NULL,
    config_snapshot JSON NULL,

    -- Timestamp
    created_at DATETIME DEFAULT NOW(),

    FOREIGN KEY (config_id) REFERENCES hrm_configs(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
);
```

#### 1.8 HRM Presets Table

**Built-in and custom HRM presets**

```sql
CREATE TABLE hrm_presets (
    id VARCHAR PRIMARY KEY,                    -- UUID
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR NULL,

    -- UI Metadata
    icon VARCHAR NULL,                         -- Emoji or icon identifier
    color VARCHAR NULL,                        -- Hex color code
    visibility VARCHAR DEFAULT 'private',      -- private, shared, public

    -- Preset Type
    is_builtin BOOLEAN DEFAULT FALSE,
    created_by VARCHAR NULL,

    -- Preset Configuration
    config JSON NOT NULL,

    -- Usage Stats
    usage_count INTEGER DEFAULT 0,
    total_cost_saved FLOAT DEFAULT 0.0,

    -- Detailed Stats (Calculated)
    avg_quality FLOAT NULL,
    avg_cost FLOAT NULL,
    avg_duration_seconds FLOAT NULL,
    last_used_at DATETIME NULL,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW()
);
```

**Built-in Presets:**
1. `balanced` - Balanced performance, cost, quality
2. `cost_optimized` - Minimize cost (prefer Gemini)
3. `quality_first` - Maximize quality (prefer Claude)
4. `speed` - Maximize speed

#### 1.9 API Keys Table

**Secure storage for provider API keys**

```sql
CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Provider Info
    provider VARCHAR NOT NULL,                 -- claude, gemini, copilot, etc.
    key_name VARCHAR NOT NULL,

    -- Encrypted Key Storage
    encrypted_key VARCHAR NOT NULL,

    -- Key Metadata
    is_active BOOLEAN DEFAULT TRUE,
    last_used DATETIME NULL,
    created_by VARCHAR NOT NULL,

    -- Rate Limits and Quotas
    daily_requests INTEGER DEFAULT 0,
    monthly_requests INTEGER DEFAULT 0,
    current_usage INTEGER DEFAULT 0,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW()
);
```

#### 1.10 Load Balancing Config Table

**Load balancing configuration per provider**

```sql
CREATE TABLE load_balancing_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Provider Identification
    provider VARCHAR NOT NULL,
    project_id VARCHAR NULL,                   -- FK: projects.id

    -- Load Balancing Strategy
    strategy VARCHAR DEFAULT 'round_robin',    -- round_robin, least_busy, cost_optimized

    -- Provider Weights (JSON)
    provider_weights JSON NOT NULL,

    -- Queue Settings
    max_concurrent_tasks INTEGER DEFAULT 5,
    queue_timeout_seconds INTEGER DEFAULT 300,

    -- Circuit Breaker Settings
    failure_threshold FLOAT DEFAULT 0.5,
    recovery_timeout_seconds INTEGER DEFAULT 300,

    -- Performance Tracking
    total_requests INTEGER DEFAULT 0,
    successful_requests INTEGER DEFAULT 0,
    failed_requests INTEGER DEFAULT 0,
    avg_response_time_ms FLOAT DEFAULT 0.0,

    -- Status
    is_enabled BOOLEAN DEFAULT TRUE,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),

    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

#### 1.11 Swarm Config Table

**Swarm orchestration configurations**

```sql
CREATE TABLE swarm_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Swarm Identification
    name VARCHAR NOT NULL,
    project_id VARCHAR NOT NULL,               -- FK: projects.id

    -- Swarm Composition (JSON)
    agents_config JSON NOT NULL,

    -- Coordination Strategy
    coordination_mode VARCHAR DEFAULT 'hierarchical',  -- hierarchical, peer, delegator
    leader_agent VARCHAR NULL,

    -- Communication Settings (JSON)
    communication_config JSON NOT NULL,

    -- Swarm Parameters
    swarm_size INTEGER DEFAULT 3,
    consensus_threshold FLOAT DEFAULT 0.66,
    max_parallel_tasks INTEGER DEFAULT 5,

    -- Performance Metrics
    total_swarm_executions INTEGER DEFAULT 0,
    successful_swarm_executions INTEGER DEFAULT 0,
    consensus_agreements INTEGER DEFAULT 0,
    consensus_disagreements INTEGER DEFAULT 0,

    -- Status
    is_active BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),

    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

#### 1.12 SpecKit Features Table

**Spec-Kit feature tracking**

```sql
CREATE TABLE speckit_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Feature Identification
    feature_name VARCHAR NOT NULL UNIQUE,
    feature_version VARCHAR DEFAULT '1.0',

    -- Feature Description
    description VARCHAR NULL,
    feature_config JSON NOT NULL,

    -- Integration Info
    integration_points JSON NOT NULL,
    dependencies JSON DEFAULT '[]',

    -- Feature Status
    is_enabled BOOLEAN DEFAULT TRUE,
    is_beta BOOLEAN DEFAULT FALSE,

    -- Performance Tracking
    usage_count INTEGER DEFAULT 0,
    total_executions INTEGER DEFAULT 0,
    successful_executions INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    avg_execution_time_ms FLOAT DEFAULT 0.0,

    -- Optimization Metrics
    optimization_potential FLOAT DEFAULT 0.0,

    -- Timestamps
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW()
);
```

#### 1.13 System Metrics Table

**System-wide metrics and monitoring**

```sql
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Metric Timestamp
    metric_timestamp DATETIME NOT NULL DEFAULT NOW(),

    -- CPU and Memory
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

    -- Timestamp
    created_at DATETIME DEFAULT NOW()
);
```

### 1.14 Database Relationships

```
projects (1) ─────┬───── (N) tasks
                  │
                  └───── (N) cost_tracking
                  │
                  └───── (N) hrm_configs
                  │
                  └───── (N) load_balancing_configs
                  │
                  └───── (N) swarm_configs

tasks (1) ────────┬───── (N) quality_snapshots
                  │
                  └───── (N) agent_switches
                  │
                  └───── (N) cost_tracking
                  │
                  └───── (N) hrm_configs
                  │
                  └───── (N) hrm_config_history

hrm_configs (1) ── (N) hrm_config_history

hrm_presets ────── (independent, referenced by config)
api_keys ─────────  (independent)
speckit_features ─  (independent)
system_metrics ───  (independent, time-series)
```

---

## 2. Data Flow Patterns

### 2.1 Task Execution Flow

```
1. CREATE Task
   └─> POST /api/orchestration/execute
       ├─> Create Task record (status: pending)
       ├─> Get HRM Config (project-level or task-level)
       ├─> Smart Agent Selection (based on task_type)
       ├─> Update Task (status: in_progress, assigned_agent)
       └─> WebSocket: Emit "task_update"

2. EXECUTE Task
   └─> Orchestrator.execute_task()
       ├─> Circuit Breaker Check
       ├─> Langfuse Trace Start (if enabled)
       ├─> Execute Agent CLI (claude/gemini/copilot)
       ├─> Parse Response
       ├─> Create Quality Snapshot (iteration)
       ├─> Create Cost Tracking record
       ├─> WebSocket: Emit "feedback_loop"
       └─> Check Quality Gate (Deep Supervision)
           ├─> If passed: Continue
           └─> If failed: Agent Switch or Retry

3. AGENT SWITCH (if needed)
   └─> Orchestrator._select_agent()
       ├─> Calculate Reward Scores
       ├─> Select New Agent
       ├─> Create Agent Switch record
       ├─> Update Task (assigned_agent, agent_switches++)
       └─> WebSocket: Emit "agent_switch"

4. ITERATION Loop
   └─> While current_iteration < max_iterations:
       ├─> Execute Agent
       ├─> Create Quality Snapshot
       ├─> Check Quality Threshold
       └─> If quality >= threshold: COMPLETE

5. COMPLETE Task
   └─> Update Task
       ├─> status: completed (or failed)
       ├─> final_quality
       ├─> actual_cost
       ├─> duration_seconds
       ├─> completed_at
       └─> WebSocket: Emit "task_update" (completed)

6. UPDATE Project Stats
   └─> Aggregate from tasks:
       ├─> total_tasks++
       ├─> successful_tasks++ (if completed)
       ├─> avg_quality = AVG(final_quality)
       ├─> total_cost += actual_cost
       └─> updated_at = NOW()
```

### 2.2 HRM Config Update Flow

```
1. UPDATE HRM Config
   └─> POST /api/hrm/config
       ├─> Get Current Config (if exists)
       ├─> Calculate Impact Estimate
       │   ├─> Cost Change (%)
       │   ├─> Speed Change (%)
       │   ├─> Quality Change (%)
       │   └─> Token Reduction (%)
       ├─> Create/Update HRM Config record
       ├─> Create HRM Config History record
       └─> WebSocket: Emit "hrm_config_update"

2. SIMULATE Impact (Optional)
   └─> POST /api/hrm/simulate
       ├─> Compare Current vs Proposed Config
       ├─> ML Model Prediction (impact_analysis)
       ├─> Generate Recommendations
       └─> Return Warnings

3. APPLY Preset
   └─> POST /api/hrm/config/presets/{id}/apply
       ├─> Get Preset Config
       ├─> Calculate Impact vs Current
       ├─> Create/Update HRM Config
       ├─> Update Preset Usage Stats
       │   ├─> usage_count++
       │   └─> last_used_at = NOW()
       └─> WebSocket: Emit "hrm_preset_applied"

4. REAL-TIME Impact (During Task)
   └─> While task running:
       ├─> Calculate current metrics
       ├─> Predict final cost/quality
       └─> WebSocket: Emit "hrm_impact_update"

5. CHECKPOINT Reached
   └─> At Deep Supervision checkpoints (0.33, 0.66, 1.00):
       ├─> Calculate quality at checkpoint
       ├─> Compare to quality_gate_threshold
       ├─> If failed: Trigger Quality Gate Action
       └─> WebSocket: Emit "hrm_checkpoint_reached"
```

### 2.3 Analytics Aggregation Flow

```
1. DASHBOARD Stats
   └─> GET /api/metrics/dashboard
       ├─> SELECT COUNT(*) FROM projects
       ├─> SELECT COUNT(*) FROM tasks WHERE status = 'in_progress'
       ├─> SELECT COUNT(*) FROM tasks WHERE DATE(completed_at) = TODAY
       ├─> SELECT SUM(cost) FROM cost_tracking WHERE DATE(created_at) = TODAY
       ├─> Calculate Performance Metrics
       │   ├─> AVG(duration_seconds)
       │   ├─> AVG(current_iteration)
       │   ├─> AVG(final_quality)
       │   └─> success_rate
       └─> Calculate Cost Metrics
           ├─> total_cost
           ├─> cost_by_agent (GROUP BY agent)
           ├─> avg_cost_per_task
           └─> savings_vs_all_claude

2. QUALITY Metrics
   └─> GET /api/metrics/quality
       ├─> SELECT FROM quality_snapshots
       │   GROUP BY DATE(created_at)
       │   AVG(overall_quality, test_coverage, security_score)
       └─> Return time-series data

3. AGENT Performance
   └─> GET /api/metrics/agents
       ├─> For each agent:
       │   ├─> total_tasks
       │   ├─> success_rate
       │   ├─> avg_quality
       │   ├─> avg_cost
       │   └─> avg_time
       └─> Return per-agent stats

4. SYSTEM Metrics Collection (Background Task)
   └─> Every 15 seconds:
       ├─> Collect CPU/Memory
       ├─> Count agents (active, idle, busy)
       ├─> Count tasks (pending, running, completed)
       ├─> Calculate costs (hourly, daily, monthly)
       ├─> Calculate throughput
       ├─> INSERT INTO system_metrics
       └─> Trim old records (keep last 7 days)
```

---

## 3. State Management

### 3.1 Backend State (Redis)

**Redis is used for:**
- Session Management (agent CLI sessions)
- Real-time Cache (hot data)
- Distributed State (multi-instance)
- WebSocket Connection Tracking

**Redis Keys:**

```
# Session Storage
session:{session_id} → JSON {agent, project_id, last_activity}
TTL: 1 hour

# Agent State
agent:{agent_id}:state → JSON {status, current_task, last_heartbeat}
TTL: 5 minutes

# Circuit Breaker State
circuit:{agent}:state → JSON {state, failure_count, last_failure}
TTL: Never (persistent)

# Task Queue
queue:pending → LIST [task_id, task_id, ...]
queue:in_progress → LIST [task_id, task_id, ...]

# Cache (Hot Data)
cache:hrm_config:{project_id} → JSON {config}
TTL: 15 minutes

cache:project:{project_id}:stats → JSON {stats}
TTL: 1 minute

cache:metrics:dashboard → JSON {metrics}
TTL: 30 seconds
```

**Redis Operations:**

```python
# Set Session
await redis_manager.set(f"session:{session_id}", json.dumps(session_data), ex=3600)

# Get Session
session_json = await redis_manager.get(f"session:{session_id}")
session_data = json.loads(session_json) if session_json else None

# Circuit Breaker
await redis_manager.hset(f"circuit:{agent}", mapping={
    "state": "open",
    "failure_count": 5,
    "last_failure": datetime.utcnow().isoformat()
})

# Cache
await redis_manager.setex(f"cache:metrics:dashboard", 30, json.dumps(metrics))
```

### 3.2 Frontend State (Zustand/Jotai)

**State Stores:**

```typescript
// 1. Project Store
interface ProjectStore {
  projects: Project[];
  currentProject: Project | null;
  loading: boolean;
  error: string | null;

  // Actions
  fetchProjects: () => Promise<void>;
  selectProject: (id: string) => void;
  createProject: (data: ProjectCreate) => Promise<Project>;
  updateProject: (id: string, data: ProjectUpdate) => Promise<Project>;
  deleteProject: (id: string) => Promise<void>;
}

// 2. Task Store
interface TaskStore {
  tasks: Task[];
  currentTask: Task | null;
  filters: TaskFilters;
  pagination: Pagination;

  // Actions
  fetchTasks: (filters?: TaskFilters) => Promise<void>;
  selectTask: (id: string) => void;
  retryTask: (id: string) => Promise<void>;
  cancelTask: (id: string) => Promise<void>;

  // Real-time Updates
  updateTaskFromWebSocket: (task: Partial<Task>) => void;
}

// 3. HRM Store
interface HRMStore {
  config: HRMConfig | null;
  presets: HRMPreset[];
  history: HRMConfigHistory[];
  impactEstimate: ImpactEstimate | null;

  // Actions
  fetchConfig: (projectId?: string, taskId?: string) => Promise<void>;
  updateConfig: (config: HRMConfig) => Promise<void>;
  simulateImpact: (current: HRMConfig, proposed: HRMConfig) => Promise<ImpactAnalysis>;
  applyPreset: (presetId: string) => Promise<void>;

  // Real-time Updates
  updateConfigFromWebSocket: (config: HRMConfig, impact: ImpactEstimate) => void;
}

// 4. Metrics Store
interface MetricsStore {
  dashboardStats: DashboardStats | null;
  qualityMetrics: QualityTrendData[];
  agentPerformance: AgentPerformanceData[];

  // Actions
  fetchDashboardStats: () => Promise<void>;
  fetchQualityMetrics: (filters?: MetricsFilters) => Promise<void>;
  fetchAgentPerformance: (filters?: MetricsFilters) => Promise<void>;
}

// 5. WebSocket Store
interface WebSocketStore {
  connected: boolean;
  subscriptions: Set<string>;
  lastMessage: WebSocketMessage | null;

  // Actions
  connect: () => void;
  disconnect: () => void;
  subscribe: (channel: string) => void;
  unsubscribe: (channel: string) => void;
  send: (message: WebSocketMessage) => void;
}

// 6. Agent Store (ReactFlow Nodes)
interface AgentStore {
  nodes: Node[];
  edges: Edge[];
  agentStates: Map<string, AgentState>;

  // Actions
  updateNode: (nodeId: string, data: Partial<Node>) => void;
  updateEdge: (edgeId: string, data: Partial<Edge>) => void;
  updateAgentState: (agentId: string, state: AgentState) => void;

  // Real-time Updates
  handleTaskUpdate: (taskId: string, data: TaskUpdate) => void;
  handleAgentSwitch: (data: AgentSwitchEvent) => void;
}
```

**State Synchronization:**

```typescript
// WebSocket → State Store Sync
websocket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "task_update":
      taskStore.updateTaskFromWebSocket(data);
      agentStore.handleTaskUpdate(data.task_id, data);
      break;

    case "hrm_config_update":
      hrmStore.updateConfigFromWebSocket(data.config, data.impact);
      break;

    case "agent_switch":
      agentStore.handleAgentSwitch(data);
      break;

    case "system_alert":
      notificationStore.addAlert(data);
      break;
  }
};

// Poll for Updates (Fallback if WebSocket fails)
setInterval(async () => {
  if (!websocketStore.connected) {
    await taskStore.fetchTasks();
    await metricsStore.fetchDashboardStats();
  }
}, 5000);
```

---

## 4. Real-time Synchronization

### 4.1 WebSocket Event System

**Event Types:**

```typescript
// 1. Task Events
type TaskUpdateEvent = {
  type: "task_update";
  task_id: string;
  status: TaskStatus;
  current_iteration: number;
  current_quality: number;
  timestamp: string;
};

type FeedbackLoopEvent = {
  type: "feedback_loop";
  task_id: string;
  iteration: number;
  quality_score: number;
  suggestions: string[];
  timestamp: string;
};

type AgentSwitchEvent = {
  type: "agent_switch";
  task_id: string;
  from_agent: string;
  to_agent: string;
  reason: string;
  timestamp: string;
};

// 2. HRM Events
type HRMConfigUpdateEvent = {
  type: "hrm_config_update";
  project_id: string;
  config_id: string;
  config: HRMConfig;
  impact: ImpactEstimate;
  timestamp: string;
};

type HRMImpactUpdateEvent = {
  type: "hrm_impact_update";
  task_id: string;
  metrics: {
    current_cost: number;
    predicted_final_cost: number;
    tokens_used: number;
    quality_trajectory: number;
  };
  timestamp: string;
};

type HRMCheckpointEvent = {
  type: "hrm_checkpoint_reached";
  task_id: string;
  checkpoint: {
    progress: number;
    quality: number;
    passed: boolean;
    suggestions: string[];
  };
  timestamp: string;
};

type HRMPresetAppliedEvent = {
  type: "hrm_preset_applied";
  project_id: string;
  preset_name: string;
  config: HRMConfig;
  timestamp: string;
};

// 3. System Events
type SystemAlertEvent = {
  type: "system_alert";
  message: string;
  severity: "info" | "success" | "warning" | "error";
  timestamp: string;
};

type ConnectionStatusEvent = {
  type: "connection_status";
  connected: boolean;
  channel: string;
  timestamp: string;
};
```

**Event Emission (Backend):**

```python
# Task Update
await websocket_manager.broadcast({
    "type": "task_update",
    "task_id": task_id,
    "status": "in_progress",
    "current_iteration": 2,
    "current_quality": 0.75,
    "timestamp": datetime.utcnow().isoformat()
}, channel=f"task_{task_id}")

# HRM Config Update
await websocket_manager.broadcast({
    "type": "hrm_config_update",
    "project_id": project_id,
    "config_id": config_id,
    "config": config_dict,
    "impact": impact.dict(),
    "timestamp": datetime.utcnow().isoformat()
}, channel=f"project_{project_id}")

# System Alert
await websocket_manager.broadcast({
    "type": "system_alert",
    "message": "Circuit breaker OPEN for agent 'copilot'",
    "severity": "warning",
    "timestamp": datetime.utcnow().isoformat()
}, channel="global")
```

**Event Handling (Frontend):**

```typescript
// Subscribe to channels
ws.send(JSON.stringify({
  type: "subscribe",
  channel: "project_123"
}));

// Handle events
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  // Update UI
  switch (data.type) {
    case "task_update":
      // Update task card
      updateTaskCard(data.task_id, {
        status: data.status,
        iteration: data.current_iteration,
        quality: data.current_quality
      });
      break;

    case "hrm_config_update":
      // Show notification
      toast.info("HRM configuration updated", {
        description: `Cost: ${data.impact.cost_change*100}%, Quality: ${data.impact.quality_change*100}%`
      });
      // Update HRM panel
      updateHRMPanel(data.config);
      break;

    case "agent_switch":
      // Animate node transition
      animateAgentSwitch(data.from_agent, data.to_agent);
      // Show notification
      toast.warning(`Agent switched: ${data.from_agent} → ${data.to_agent}`, {
        description: data.reason
      });
      break;
  }
};
```

---

## 5. Analytics Pipeline

### 5.1 Metrics Collection

**Background Task (runs every 15 seconds):**

```python
async def collect_system_metrics():
    """Collect and store system metrics"""

    # 1. Count agents by state
    agents_active = await count_agents_by_state("active")
    agents_idle = await count_agents_by_state("idle")
    agents_busy = await count_agents_by_state("busy")

    # 2. Count tasks by status
    tasks_pending = await count_tasks_by_status("pending")
    tasks_running = await count_tasks_by_status("in_progress")
    tasks_completed_today = await count_tasks_completed_today()

    # 3. Calculate costs
    hourly_cost = await calculate_cost_since(datetime.utcnow() - timedelta(hours=1))
    daily_cost = await calculate_cost_since(datetime.utcnow() - timedelta(days=1))
    monthly_cost = await calculate_cost_since(datetime.utcnow() - timedelta(days=30))

    # 4. Calculate quality metrics
    avg_quality = await calculate_avg_quality()
    test_pass_rate = await calculate_test_pass_rate()
    security_score = await calculate_security_score()

    # 5. Calculate API metrics
    api_calls_total, api_calls_failed, api_avg_latency = await calculate_api_metrics()

    # 6. Calculate throughput
    throughput_tasks_per_hour = await calculate_throughput_tasks()
    throughput_tokens_per_second = await calculate_throughput_tokens()

    # 7. Get system resources
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    # 8. Get cache stats
    cache_hit_rate = await redis_manager.get_cache_hit_rate()

    # 9. Get queue depth
    queue_depth = await redis_manager.llen("queue:pending")

    # 10. Store metrics
    metric = SystemMetrics(
        metric_timestamp=datetime.utcnow(),
        cpu_usage_percent=cpu_usage,
        memory_usage_percent=memory_usage,
        agents_active=agents_active,
        agents_idle=agents_idle,
        agents_busy=agents_busy,
        tasks_pending=tasks_pending,
        tasks_running=tasks_running,
        tasks_completed=tasks_completed_today,
        hourly_cost=hourly_cost,
        daily_cost=daily_cost,
        monthly_cost=monthly_cost,
        avg_quality_score=avg_quality,
        test_pass_rate=test_pass_rate,
        security_score=security_score,
        api_calls_total=api_calls_total,
        api_calls_failed=api_calls_failed,
        api_avg_latency_ms=api_avg_latency,
        throughput_tasks_per_hour=throughput_tasks_per_hour,
        throughput_tokens_per_second=throughput_tokens_per_second,
        queue_depth=queue_depth,
        cache_hit_rate=cache_hit_rate
    )

    db.add(metric)
    await db.commit()

    # 11. Trim old records (keep last 7 days)
    await trim_old_metrics(days=7)
```

### 5.2 Analytics Queries

**Dashboard Stats:**

```python
# Aggregate from last 30 days
stats = await db.execute(
    select(
        func.count(Task.id).label("total_tasks"),
        func.sum(case((Task.status == TaskStatus.COMPLETED, 1), else_=0)).label("successful_tasks"),
        func.avg(Task.final_quality).label("avg_quality"),
        func.sum(CostTracking.cost).label("total_cost")
    )
    .outerjoin(CostTracking, Task.id == CostTracking.task_id)
    .where(Task.created_at >= datetime.utcnow() - timedelta(days=30))
)
```

**Quality Trend:**

```python
# Group by date
quality_trend = await db.execute(
    select(
        func.date(QualitySnapshot.created_at).label("date"),
        func.avg(QualitySnapshot.overall_quality).label("overall_quality"),
        func.avg(QualitySnapshot.test_coverage).label("test_coverage"),
        func.avg(QualitySnapshot.security_score).label("security_score")
    )
    .group_by(func.date(QualitySnapshot.created_at))
    .order_by(func.date(QualitySnapshot.created_at).desc())
    .limit(30)
)
```

**Agent Performance:**

```python
# Per-agent statistics
agent_perf = await db.execute(
    select(
        Task.assigned_agent,
        func.count(Task.id).label("total_tasks"),
        func.avg(Task.final_quality).label("avg_quality"),
        func.avg(Task.duration_seconds).label("avg_duration"),
        func.avg(CostTracking.cost).label("avg_cost"),
        func.sum(case((Task.status == TaskStatus.COMPLETED, 1), else_=0)).label("successful")
    )
    .outerjoin(CostTracking, Task.id == CostTracking.task_id)
    .group_by(Task.assigned_agent)
)
```

---

## 6. Feedback Loop System

### 6.1 UltraThink Feedback Loop

**Location:** `lazy-bird/feedback/`

**Components:**

```
lazy-bird/feedback/
├── feedback_loop.py         # Main feedback loop engine
├── quality_evaluator.py     # Quality assessment
├── iteration_optimizer.py   # Iteration optimization
└── suggestions_generator.py # Improvement suggestions
```

**Flow:**

```
1. Task Execution
   └─> Agent produces output
       └─> feedback_loop.evaluate()
           ├─> quality_evaluator.assess()
           │   ├─> Test Coverage
           │   ├─> Security Score
           │   ├─> Code Quality
           │   ├─> Type Safety
           │   └─> Documentation
           ├─> suggestions_generator.generate()
           │   ├─> Analyze output
           │   ├─> Compare to best practices
           │   └─> Generate improvement suggestions
           └─> iteration_optimizer.should_continue()
               ├─> Quality >= threshold? → STOP
               ├─> Iteration >= max? → STOP
               └─> Else → CONTINUE with suggestions

2. Quality Gate Check (Deep Supervision)
   └─> At checkpoints (0.33, 0.66, 1.00):
       ├─> Calculate quality
       ├─> If quality < quality_gate_threshold:
       │   ├─> Generate detailed feedback
       │   ├─> Consider agent switch
       │   └─> Adjust parameters
       └─> WebSocket: Emit "hrm_checkpoint_reached"

3. Agent Switch Decision
   └─> If quality not improving:
       ├─> Calculate reward scores
       ├─> Select better agent
       ├─> Transfer context
       └─> Continue with new agent
```

**Feedback Data Stored:**

```sql
-- In quality_snapshots table
INSERT INTO quality_snapshots (
    task_id,
    iteration,
    overall_quality,
    test_coverage,
    security_score,
    code_quality_score,
    type_safety,
    documentation,
    vulnerabilities,
    type_errors,
    complexity,
    failing_test_count
) VALUES (...);
```

**WebSocket Events:**

```python
# Feedback loop update
await emit_feedback_loop_update(task_id, {
    "iteration": 2,
    "quality_score": 0.85,
    "suggestions": [
        "Add error handling in authentication module",
        "Improve test coverage for edge cases",
        "Add JSDoc comments to exported functions"
    ],
    "quality_breakdown": {
        "test_coverage": 0.78,
        "security_score": 0.92,
        "code_quality": 0.88,
        "type_safety": 0.85,
        "documentation": 0.75
    }
})
```

---

## 7. Guidelines Management

### 7.1 Layer-2 Prompts

**Location:** `lazy-bird/guidelines/layers/`

```
lazy-bird/guidelines/layers/
├── LAYER-2-CLAUDE.md       # Claude-specific instructions
├── LAYER-2-GEMINI.md       # Gemini-specific instructions
└── LAYER-2-COPILOT.md      # Copilot-specific instructions
```

**Storage:**

- **File System** (primary) - Markdown files
- **Database** (cache) - `api/agents/files` endpoint

**Loading:**

```python
def load_guideline(agent: AgentType) -> str:
    """Load agent-specific guideline"""

    guideline_path = f"lazy-bird/guidelines/layers/LAYER-2-{agent.upper()}.md"

    if os.path.exists(guideline_path):
        with open(guideline_path, 'r') as f:
            return f.read()

    return DEFAULT_GUIDELINE
```

**Injection:**

```python
# Method 1: Custom Instructions (Claude Desktop)
# .claude/guidelines.md → Contains LAYER-2-CLAUDE.md content

# Method 2: Prompt Engineering (Gemini/Copilot)
full_prompt = f"""
{load_guideline(AgentType.GEMINI)}

---

Task: {user_prompt}
"""

# Method 3: System Message (API)
messages = [
    {"role": "system", "content": load_guideline(agent)},
    {"role": "user", "content": user_prompt}
]
```

### 7.2 Guidelines API

```http
# Get all guidelines
GET /api/agents/files?file_type=instruction

# Get specific guideline
GET /api/agents/files/lazy-bird/guidelines/layers/LAYER-2-CLAUDE.md

# Update guideline
PUT /api/agents/files/lazy-bird/guidelines/layers/LAYER-2-CLAUDE.md
Content-Type: application/json
{
  "content": "# Updated guideline..."
}

# Create new guideline
POST /api/agents/files
Content-Type: application/json
{
  "file_path": "lazy-bird/guidelines/custom-guideline.md",
  "file_type": "instruction",
  "content": "# Custom guideline..."
}
```

---

## 8. Caching Strategy

### 8.1 Three-Layer Cache

**Layer 1: Memory Cache (Fastest)**

```python
from functools import lru_cache

# Function-level cache
@lru_cache(maxsize=128)
def get_hrm_preset(preset_id: str) -> HRMPreset:
    """Cached preset retrieval"""
    return db.query(HRMPreset).filter(HRMPreset.id == preset_id).first()

# Class-level cache
class ProjectCache:
    def __init__(self):
        self._cache: Dict[str, Project] = {}
        self._expiry: Dict[str, datetime] = {}

    def get(self, project_id: str) -> Optional[Project]:
        if project_id in self._cache:
            if self._expiry[project_id] > datetime.utcnow():
                return self._cache[project_id]
            else:
                del self._cache[project_id]
                del self._expiry[project_id]
        return None

    def set(self, project_id: str, project: Project, ttl_seconds: int = 300):
        self._cache[project_id] = project
        self._expiry[project_id] = datetime.utcnow() + timedelta(seconds=ttl_seconds)
```

**Layer 2: Redis Cache (Fast, Distributed)**

```python
async def get_cached_config(project_id: str) -> Optional[dict]:
    """Get HRM config from Redis cache"""

    cache_key = f"cache:hrm_config:{project_id}"
    cached = await redis_manager.get(cache_key)

    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    config = await db.query(HRMConfig).filter(
        HRMConfig.project_id == project_id
    ).first()

    if config:
        # Store in cache (15 min TTL)
        await redis_manager.setex(
            cache_key,
            900,  # 15 minutes
            json.dumps(config.config)
        )
        return config.config

    return None

async def invalidate_config_cache(project_id: str):
    """Invalidate config cache on update"""
    await redis_manager.delete(f"cache:hrm_config:{project_id}")
```

**Layer 3: Database (Source of Truth)**

```python
async def get_project_stats(project_id: str) -> dict:
    """Get project stats with caching"""

    # Try Layer 1 (Memory)
    cached = memory_cache.get(f"stats_{project_id}")
    if cached:
        return cached

    # Try Layer 2 (Redis)
    cache_key = f"cache:project:{project_id}:stats"
    cached_json = await redis_manager.get(cache_key)
    if cached_json:
        stats = json.loads(cached_json)
        memory_cache.set(f"stats_{project_id}", stats, ttl_seconds=60)
        return stats

    # Layer 3 (Database)
    result = await db.execute(
        select(
            func.count(Task.id).label("total_tasks"),
            func.sum(case((Task.status == TaskStatus.COMPLETED, 1), else_=0)).label("successful"),
            func.avg(Task.final_quality).label("avg_quality"),
            func.sum(Task.actual_cost).label("total_cost")
        )
        .where(Task.project_id == project_id)
    )

    stats = result.first()._asdict()

    # Store in Layer 2 (1 min TTL)
    await redis_manager.setex(cache_key, 60, json.dumps(stats))

    # Store in Layer 1 (1 min TTL)
    memory_cache.set(f"stats_{project_id}", stats, ttl_seconds=60)

    return stats
```

### 8.2 Cache Invalidation

```python
# On Project Update
async def update_project(project_id: str, data: dict):
    """Update project and invalidate caches"""

    # Update database
    await db.execute(
        update(Project)
        .where(Project.id == project_id)
        .values(**data)
    )
    await db.commit()

    # Invalidate caches
    memory_cache.delete(f"project_{project_id}")
    memory_cache.delete(f"stats_{project_id}")
    await redis_manager.delete(f"cache:project:{project_id}:stats")

# On Task Completion
async def complete_task(task_id: str):
    """Complete task and invalidate project caches"""

    task = await get_task(task_id)

    # Update task
    task.status = TaskStatus.COMPLETED
    await db.commit()

    # Invalidate project caches (stats changed)
    memory_cache.delete(f"stats_{task.project_id}")
    await redis_manager.delete(f"cache:project:{task.project_id}:stats")
```

### 8.3 Cache Warming

```python
async def warm_cache_on_startup():
    """Pre-load frequently accessed data"""

    # Load all active projects
    projects = await db.execute(
        select(Project).where(Project.status == ProjectStatus.ACTIVE)
    )

    for project in projects.scalars():
        # Pre-calculate stats
        stats = await get_project_stats(project.id)

        # Pre-load HRM configs
        config = await get_hrm_config(project.id)

        # Pre-load agent connections
        connections = await load_agent_connections()
```

---

## 9. Subagent Coordination

### 9.1 Multi-Agent Orchestration

**Orchestrator:** `dashboard/backend/orchestration/orchestrator.py`

**Agent Selection Algorithm:**

```python
def _select_agent(self, task: Task) -> AgentType:
    """Smart agent selection based on task type and context"""

    # 1. Check if security-critical
    if task.requires_security:
        return AgentType.CLAUDE

    # 2. Task-type based routing
    if task.task_type == TaskType.SECURITY:
        return AgentType.CLAUDE
    elif task.task_type == TaskType.ARCHITECTURE:
        return AgentType.CLAUDE
    elif task.task_type == TaskType.GITHUB_WORKFLOW:
        return AgentType.COPILOT
    elif task.task_type == TaskType.BULK_ANALYSIS:
        return AgentType.GEMINI

    # 3. File size check
    if len(task.files) > 10 or any(get_file_size(f) > 100_000 for f in task.files):
        return AgentType.GEMINI

    # 4. RL-based reward calculation
    rewards = {
        AgentType.CLAUDE: 0.9,
        AgentType.GEMINI: 0.3,
        AgentType.COPILOT: 0.2
    }

    # Adjust based on circuit breaker state
    for agent, breaker in self.circuit_breakers.items():
        if breaker.state == CircuitState.OPEN:
            rewards[agent] = 0.0

    # Adjust based on historical performance
    for agent in rewards:
        perf = await get_agent_performance(agent, task.project_id)
        rewards[agent] *= perf.success_rate

    # Select agent with highest reward
    return max(rewards.items(), key=lambda x: x[1])[0]
```

**Agent Switching:**

```python
async def _handle_agent_switch(self, task: Task, reason: str):
    """Switch to different agent mid-task"""

    old_agent = task.assigned_agent

    # Select new agent
    new_agent = self._select_agent(task)

    if new_agent == old_agent:
        # No better agent available
        return False

    # Log agent switch
    switch = AgentSwitch(
        task_id=task.id,
        from_agent=old_agent,
        to_agent=new_agent,
        reason=reason,
        trigger="quality_threshold_not_met"
    )
    db.add(switch)

    # Update task
    task.assigned_agent = new_agent
    task.agent_switches += 1
    await db.commit()

    # Emit WebSocket event
    await emit_agent_switch(
        task_id=task.id,
        from_agent=old_agent.value,
        to_agent=new_agent.value,
        reason=reason
    )

    return True
```

### 9.2 Swarm Coordination

**Swarm Config Example:**

```json
{
  "name": "Code Review Swarm",
  "coordination_mode": "hierarchical",
  "leader_agent": "claude",
  "agents_config": [
    {
      "agent": "claude",
      "role": "lead_reviewer",
      "responsibilities": ["architecture", "security", "best_practices"]
    },
    {
      "agent": "gemini",
      "role": "code_analyzer",
      "responsibilities": ["complexity", "duplication", "documentation"]
    },
    {
      "agent": "copilot",
      "role": "test_reviewer",
      "responsibilities": ["test_coverage", "test_quality"]
    }
  ],
  "consensus_threshold": 0.66,
  "communication_config": {
    "mode": "sequential",
    "handoff_data": ["analysis_results", "issues_found", "suggestions"]
  }
}
```

**Swarm Execution:**

```python
async def execute_swarm(swarm_config: SwarmConfig, task: Task):
    """Execute task with swarm of agents"""

    results = []

    # 1. Leader analyzes first
    leader_result = await execute_agent(
        agent=swarm_config.leader_agent,
        task=task
    )
    results.append(leader_result)

    # 2. Other agents process in parallel
    worker_tasks = []
    for agent_cfg in swarm_config.agents_config:
        if agent_cfg["agent"] != swarm_config.leader_agent:
            worker_tasks.append(
                execute_agent(
                    agent=agent_cfg["agent"],
                    task=task,
                    context=leader_result.analysis
                )
            )

    worker_results = await asyncio.gather(*worker_tasks)
    results.extend(worker_results)

    # 3. Aggregate results
    consensus = calculate_consensus(results, swarm_config.consensus_threshold)

    # 4. Final decision by leader
    if consensus.agreement >= swarm_config.consensus_threshold:
        final_result = consensus.agreed_result
    else:
        # Leader makes final decision
        final_result = await leader_review(
            leader_agent=swarm_config.leader_agent,
            all_results=results,
            disagreements=consensus.disagreements
        )

    return final_result
```

---

## 10. Implementation Guide

### 10.1 Frontend Implementation Checklist

**Step 1: Setup State Management**

```bash
npm install zustand @tanstack/react-query
```

```typescript
// stores/projectStore.ts
import create from 'zustand';

export const useProjectStore = create<ProjectStore>((set, get) => ({
  projects: [],
  currentProject: null,
  loading: false,
  error: null,

  fetchProjects: async () => {
    set({ loading: true, error: null });
    try {
      const response = await fetch('http://localhost:1336/api/projects');
      const projects = await response.json();
      set({ projects, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  selectProject: (id) => {
    const project = get().projects.find(p => p.id === id);
    set({ currentProject: project });
  },

  // ... other actions
}));
```

**Step 2: Setup WebSocket Client**

```typescript
// services/websocket.ts
class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect() {
    this.ws = new WebSocket('ws://localhost:1336/ws');

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.reconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 30000);
      setTimeout(() => this.connect(), delay);
    }
  }

  private handleMessage(data: WebSocketMessage) {
    // Route to appropriate store
    switch (data.type) {
      case 'task_update':
        useTaskStore.getState().updateTaskFromWebSocket(data);
        break;
      case 'hrm_config_update':
        useHRMStore.getState().updateConfigFromWebSocket(data.config, data.impact);
        break;
      // ... other events
    }
  }

  subscribe(channel: string) {
    this.ws?.send(JSON.stringify({ type: 'subscribe', channel }));
  }

  send(message: any) {
    this.ws?.send(JSON.stringify(message));
  }
}

export const wsClient = new WebSocketClient();
```

**Step 3: Create API Client**

```typescript
// services/api.ts
class APIClient {
  private baseURL = 'http://localhost:1336';

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`);
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  }

  // ... put, delete methods
}

export const api = new APIClient();

// Usage
export const projectAPI = {
  getAll: () => api.get<Project[]>('/api/projects'),
  getById: (id: string) => api.get<Project>(`/api/projects/${id}`),
  create: (data: ProjectCreate) => api.post<Project>('/api/projects', data),
  update: (id: string, data: ProjectUpdate) => api.put<Project>(`/api/projects/${id}`, data),
  delete: (id: string) => api.delete(`/api/projects/${id}`)
};
```

**Step 4: Implement Polling Fallback**

```typescript
// hooks/usePolling.ts
export function usePolling(callback: () => void, interval: number, enabled: boolean) {
  useEffect(() => {
    if (!enabled) return;

    const id = setInterval(callback, interval);
    return () => clearInterval(id);
  }, [callback, interval, enabled]);
}

// Usage
const wsConnected = useWebSocketStore(state => state.connected);
const fetchTasks = useTaskStore(state => state.fetchTasks);

usePolling(fetchTasks, 5000, !wsConnected);
```

### 10.2 Backend Implementation Checklist

**Step 1: Initialize Database**

```python
# main.py
from database import init_db_async

@app.on_event("startup")
async def startup_event():
    await init_db_async()
```

**Step 2: Setup Redis**

```python
# routers/redis_manager.py
from redis import asyncio as aioredis

class RedisManager:
    def __init__(self):
        self.redis = None

    async def connect(self):
        try:
            self.redis = await aioredis.from_url(
                "redis://localhost:6379",
                decode_responses=True
            )
            await self.redis.ping()
            print("Redis connected")
        except Exception as e:
            print(f"Redis connection failed: {e}")

    async def get(self, key: str):
        if not self.redis:
            return None
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ex: int = None):
        if not self.redis:
            return
        await self.redis.set(key, value, ex=ex)

redis_manager = RedisManager()

@app.on_event("startup")
async def startup_redis():
    await redis_manager.connect()
```

**Step 3: Setup Metrics Collection**

```python
# background_tasks.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', seconds=15)
async def collect_metrics():
    await collect_system_metrics()

@app.on_event("startup")
async def start_scheduler():
    scheduler.start()
```

**Step 4: Configure Langfuse (Optional)**

```bash
# .env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

```python
# orchestration/langfuse_integration.py
observer = get_langfuse_observer()

# In orchestrator
async with observer.trace_agent_execution(
    task_id=task.id,
    agent=agent.value,
    prompt=task.prompt
) as trace:
    response = await execute_agent()
    trace.update(
        output=response.content,
        tokens=response.tokens,
        cost=response.cost
    )
```

---

## 11. Production Enhancements

### Overview

This section covers critical production requirements that ensure system reliability, security, and maintainability.

**Production-Ready Checklist:**
- [x] Database Schema Migrations (Alembic)
- [x] API Key Encryption (Fernet)
- [x] Error Handling & Retry Strategy
- [x] Comprehensive Testing Strategy
- [x] WebSocket Reliability (Acknowledgements)
- [x] LLM Observability (Langfuse)

### 11.1 Schema Migrations with Alembic

**Why:** Track database schema changes, enable rollbacks, maintain consistency across environments.

**Documentation:** `docs/SCHEMA_MIGRATIONS.md`

**Key Features:**
- Version-controlled schema changes
- Automatic migration generation
- Safe rollback capability
- Production deployment workflow

**Setup:**
```bash
# Install
pip install alembic==1.13.1

# Initialize
alembic init migrations

# Generate migration
alembic revision --autogenerate -m "add priority to tasks"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Migration Example:**
```python
"""add priority to tasks

Revision ID: 001_add_priority
Revises: initial_schema
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.add_column('tasks', sa.Column('priority', sa.Integer(), server_default='5'))
    op.create_index('idx_tasks_priority', 'tasks', ['priority', 'created_at'])

def downgrade() -> None:
    op.drop_index('idx_tasks_priority', table_name='tasks')
    op.drop_column('tasks', 'priority')
```

**Best Practices:**
- Small, incremental migrations
- Always review auto-generated migrations
- Test in development before production
- Backup database before production migrations
- Version control all migration files

### 11.2 API Key Encryption

**Why:** Protect sensitive credentials from database breaches, pass security audits.

**Documentation:** `docs/API_KEY_ENCRYPTION.md`

**Implementation:**
```python
# utils/encryption.py
from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self, key: str):
        self.cipher = Fernet(key.encode())

    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()

# Usage in models
class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True)
    provider = Column(String, nullable=False)
    encrypted_key = Column(Text, nullable=False)

    def set_api_key(self, plaintext_key: str):
        self.encrypted_key = encrypt_api_key(plaintext_key)

    def get_api_key(self) -> str:
        return decrypt_api_key(self.encrypted_key)
```

**Environment Setup:**
```bash
# Generate key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Add to .env
FERNET_KEY=XpW8rVj3K9mN2qB7fH5cT1yU6zD4sA0oE8wL3xG9vM4=
```

**Security Checklist:**
- [ ] FERNET_KEY stored in secrets manager (Azure Key Vault, AWS Secrets Manager)
- [ ] FERNET_KEY never committed to git
- [ ] API key access logged and audited
- [ ] Decryption endpoints rate-limited
- [ ] No plaintext keys in logs or API responses

### 11.3 Error Handling & Retry Strategy

**Why:** Graceful degradation, automatic recovery from transient failures, clear error messages.

**Documentation:** `docs/ERROR_HANDLING_RETRY_STRATEGY.md`

**Error Classification:**

```python
# Transient Errors (Retriable)
TRANSIENT_HTTP_CODES = {408, 429, 500, 502, 503, 504}

def is_transient_error(e: Exception) -> bool:
    return isinstance(e, (TimeoutError, ConnectionError, TransientError)) or \
           (isinstance(e, HTTPException) and e.status_code in TRANSIENT_HTTP_CODES)

# Permanent Errors (Non-Retriable)
PERMANENT_HTTP_CODES = {400, 401, 403, 404, 405, 410}

def is_permanent_error(e: Exception) -> bool:
    return isinstance(e, (ValidationError, ValueError, PermanentError)) or \
           (isinstance(e, HTTPException) and e.status_code in PERMANENT_HTTP_CODES)
```

**Retry Pattern:**

```python
async def retry_with_exponential_backoff(
    func: Callable,
    *args,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    **kwargs
) -> Any:
    """Retry with exponential backoff."""
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if is_permanent_error(e):
                raise  # Don't retry permanent errors

            last_exception = e

            if attempt == max_retries:
                raise

            delay = min(initial_delay * (exponential_base ** (attempt - 1)), max_delay)
            logger.warning(f"Attempt {attempt}/{max_retries} failed: {e}. Retrying in {delay:.2f}s")
            await asyncio.sleep(delay)

    raise last_exception
```

**Circuit Breaker Integration:**

```python
# Already implemented in orchestration/circuit_breaker.py
claude_breaker = CircuitBreaker(
    failure_threshold=5,
    timeout_duration=60
)

async def execute_with_circuit_breaker(task: Task):
    """Execute with circuit breaker + retry."""
    return await claude_breaker.call_async(
        retry_with_exponential_backoff,
        execute_agent,
        task,
        max_retries=3
    )
```

**Standard Error Response:**

```json
{
    "error": "Service temporarily unavailable",
    "error_code": "AGENT_UNAVAILABLE",
    "details": {
        "code": "CIRCUIT_BREAKER_OPEN",
        "message": "Claude agent circuit breaker is open",
        "details": {
            "agent": "claude",
            "failure_count": 5,
            "retry_after": 45
        }
    },
    "timestamp": "2025-11-10T12:00:00Z",
    "request_id": "req_abc123",
    "retry_after": 60
}
```

### 11.4 Testing Strategy

**Why:** Catch bugs early, deploy with confidence, safe refactoring, fast feedback.

**Documentation:** `docs/TESTING_STRATEGY.md`

**Test Structure:**

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_circuit_breaker.py
│   ├── test_encryption.py
│   └── orchestration/
│       └── test_agent_selection.py
├── integration/             # Real dependencies
│   ├── test_database.py
│   ├── test_api_endpoints.py
│   └── test_orchestrator_flow.py
└── e2e/                     # Full system
    └── test_task_execution.py
```

**Example Tests:**

```python
# Unit Test
@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_threshold():
    breaker = CircuitBreaker(failure_threshold=3)

    for i in range(3):
        try:
            breaker.call(lambda: (_ for _ in ()).throw(Exception("Test")))
        except:
            pass

    assert breaker.state == CircuitState.OPEN

# Integration Test
@pytest.mark.asyncio
async def test_orchestrator_switches_agent_on_failure(sample_task):
    orchestrator = CLIOrchestrator()

    with patch.object(orchestrator, "_execute_claude", side_effect=NetworkError()):
        response = await orchestrator.execute_task(sample_task, "session_1")

    assert response.agent == "gemini"  # Switched to fallback

# E2E Test
@pytest.mark.asyncio
async def test_full_task_execution_flow(test_client):
    project_response = await test_client.post("/api/projects", json={
        "name": "Test Project",
        "status": "active"
    })

    task_response = await test_client.post("/api/orchestration/execute", json={
        "prompt": "Write hello world",
        "project_id": project_response.json()["id"]
    })

    assert task_response.status_code == 200
    assert "task_id" in task_response.json()
```

**Coverage Goals:**
- Overall: 80% minimum
- Critical paths (orchestrator, circuit breaker): 95% minimum
- Models, schemas: 70% minimum

**CI/CD Integration:**

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
      redis:
        image: redis:7

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov

      - name: Run tests
        run: pytest --cov=. --cov-fail-under=80

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### 11.5 WebSocket Reliability

**Why:** Guaranteed message delivery, prevent lost updates, handle network interruptions.

**Documentation:** Referenced in research notes

**Implementation:**

```python
# routers/websocket.py
import uuid
from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "global": set(),
            "projects": {},
            "tasks": {}
        }
        self.message_queue: Dict[str, List[dict]] = {}  # Per-connection queues
        self.pending_acks: Dict[str, dict] = {}  # Pending acknowledgements

    async def send_with_ack(self, channel: str, message: dict, timeout: int = 60):
        """Send message with acknowledgement requirement."""
        message_id = str(uuid.uuid4())
        message["message_id"] = message_id
        message["requires_ack"] = True

        # Store for retry
        self.pending_acks[message_id] = {
            "message": message,
            "channel": channel,
            "sent_at": datetime.utcnow(),
            "timeout": timeout
        }

        # Send to all connections in channel
        for connection in self.active_connections.get(channel, set()):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message: {e}")

    async def handle_ack(self, message_id: str, connection_id: str):
        """Handle acknowledgement from client."""
        if message_id in self.pending_acks:
            logger.info(f"Message {message_id} acknowledged by {connection_id}")
            del self.pending_acks[message_id]

    async def retry_unacked_messages(self):
        """Retry messages that haven't been acknowledged."""
        now = datetime.utcnow()

        for message_id, pending in list(self.pending_acks.items()):
            elapsed = (now - pending["sent_at"]).total_seconds()

            if elapsed > pending["timeout"]:
                logger.warning(f"Message {message_id} timed out, removing")
                del self.pending_acks[message_id]
            elif elapsed > 10:  # Retry after 10s
                logger.info(f"Retrying message {message_id}")
                await self.send_with_ack(
                    pending["channel"],
                    pending["message"],
                    pending["timeout"]
                )

# Client-side acknowledgement
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, channel: str = "global"):
    await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_json()

            # Handle acknowledgements
            if data.get("type") == "ack":
                await manager.handle_ack(
                    data["message_id"],
                    data["connection_id"]
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
```

**Client Implementation:**

```typescript
// Frontend WebSocket with acknowledgements
class ReliableWebSocket {
    private ws: WebSocket;
    private messageQueue: Map<string, any> = new Map();

    connect(url: string) {
        this.ws = new WebSocket(url);

        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);

            // Send acknowledgement if required
            if (message.requires_ack) {
                this.ws.send(JSON.stringify({
                    type: "ack",
                    message_id: message.message_id,
                    connection_id: this.connectionId
                }));
            }

            // Process message
            this.handleMessage(message);
        };
    }
}
```

### 11.6 LLM Observability (Langfuse)

**Status:** ✅ REQUIRED - No Compromises

**Why:** Complete visibility into agent execution, cost tracking, quality metrics, debugging.

**Documentation:** `docs/LANGFUSE_SETUP.md`

**What Langfuse Tracks:**

```
Task Execution:
  ├─> Agent Selection (logged with reasoning)
  ├─> Prompt sent to Agent (with metadata)
  ├─> Agent Response (with tokens + cost)
  ├─> Quality Assessment (logged)
  └─> Agent Switch (if needed, with reason)

All visible in Langfuse Dashboard!
```

**Setup:**

```bash
# 1. Get keys from cloud.langfuse.com
# 2. Add to .env
LANGFUSE_PUBLIC_KEY=pk-lf-your-key
LANGFUSE_SECRET_KEY=sk-lf-your-key
LANGFUSE_HOST=https://cloud.langfuse.com

# 3. Install
pip install langfuse==2.59.0

# 4. Test
python test_langfuse.py
```

**Integration (Already Implemented):**

```python
# orchestration/orchestrator.py
from orchestration.langfuse_integration import get_langfuse_observer

observer = get_langfuse_observer()

async def execute_task(self, task: Task, session_id: str):
    async with observer.trace_agent_execution(
        task_id=task.id,
        agent=selected_agent.value,
        prompt=task.prompt,
        metadata={
            "task_type": task.task_type.value,
            "requires_security": task.requires_security
        }
    ) as trace:
        response = await self._execute_agent(task, session_id)

        trace.update(
            output=response.content,
            tokens=response.tokens,
            cost=response.cost,
            metadata={"duration": response.duration}
        )

    # Track agent selection
    observer.track_agent_selection(
        task_id=task.id,
        selected_agent=selected_agent.value,
        reason="Task type: security",
        all_rewards={"claude": 0.9, "gemini": 0.3}
    )
```

**Benefits:**

- **Cost Tracking:** Per-agent, per-task costs with monthly projections
- **Quality Metrics:** Correlate quality scores with agent performance
- **Debugging:** Replay failed tasks, see exact prompts/responses
- **Agent Selection Analysis:** Why was Claude chosen over Gemini?
- **Token Usage:** Input/output tokens for billing analysis
- **Performance Monitoring:** Response times, success rates

**Grafana Integration:**

Combine Langfuse (LLM metrics) with Prometheus (system metrics) in unified Grafana dashboard:

```python
# routers/metrics.py
@router.get("/langfuse/summary")
async def get_langfuse_summary():
    """Fetch LLM metrics from Langfuse for Grafana."""
    observer = get_langfuse_observer()

    traces = observer.langfuse.get_traces(
        from_timestamp=datetime.utcnow() - timedelta(hours=1)
    )

    return {
        "total_tasks": len(traces),
        "total_cost": sum(t.cost for t in traces),
        "avg_quality": mean(t.metadata.get("quality", 0) for t in traces),
        "agent_breakdown": {
            "claude": len([t for t in traces if t.metadata.get("agent") == "claude"]),
            "gemini": len([t for t in traces if t.metadata.get("agent") == "gemini"]),
        }
    }
```

### 11.7 Production Deployment Checklist

**Before Production:**

- [ ] Database migrations tested and versioned
- [ ] FERNET_KEY stored in secrets manager
- [ ] All API keys encrypted in database
- [ ] Error handling implemented for all endpoints
- [ ] Circuit breakers configured for all agents
- [ ] Test coverage above 80%
- [ ] CI/CD pipeline running successfully
- [ ] WebSocket acknowledgements implemented
- [ ] Langfuse configured and tested
- [ ] Monitoring and alerting set up
- [ ] Backup and recovery procedures documented
- [ ] Load testing completed
- [ ] Security audit passed

**Production Environment:**

```bash
# .env.production
DATABASE_URL=postgresql+asyncpg://user:password@prod-db:5432/lazy_bird
REDIS_URL=redis://prod-redis:6379
FERNET_KEY=${AZURE_KEY_VAULT_FERNET_KEY}  # From secrets manager
LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
LANGFUSE_HOST=https://cloud.langfuse.com

LOG_LEVEL=INFO
CORS_ORIGINS=https://phantom-neural-cortex.com

# Error tracking
SENTRY_DSN=https://...@sentry.io/project

# Monitoring
PROMETHEUS_PORT=9090
```

**Health Check Endpoint:**

```python
@router.get("/api/health")
async def health_check():
    """Comprehensive health check."""
    return {
        "status": "healthy",
        "database": await check_db_health(),
        "redis": await check_redis_health(),
        "langfuse": observer.enabled,
        "circuit_breakers": {
            "claude": claude_breaker.get_state(),
            "gemini": gemini_breaker.get_state(),
            "copilot": copilot_breaker.get_state()
        },
        "version": "2.0.0"
    }
```

---

## 12. Documentation Index

**Architecture:**
- `docs/SYSTEM_ARCHITECTURE_SUMMARY.md` - System overview
- `docs/DATA_ARCHITECTURE.md` - This document
- `docs/BACKEND_API_REQUIREMENTS.md` - Complete API reference

**Production Enhancements:**
- `docs/LANGFUSE_SETUP.md` - LLM observability (REQUIRED)
- `docs/SCHEMA_MIGRATIONS.md` - Database migrations with Alembic
- `docs/API_KEY_ENCRYPTION.md` - Secure credential management
- `docs/ERROR_HANDLING_RETRY_STRATEGY.md` - Resilience patterns
- `docs/TESTING_STRATEGY.md` - Comprehensive testing guide

**Quick Start:**
- `.env.example` - Environment configuration template
- `docs/INDEX.md` - Documentation index

---

**Last Updated:** 2025-11-10
**Maintainer:** LEEI1337
**Version:** 2.1.0
