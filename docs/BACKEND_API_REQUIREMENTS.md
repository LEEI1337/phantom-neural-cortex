# Backend API Requirements - Complete Reference

**Version:** 2.0.0
**Base URL:** `http://localhost:1336`
**Status:** Production Ready

This document contains ALL API endpoints, schemas, query parameters, and WebSocket events needed for frontend implementation.

---

## Table of Contents

1. [Orchestration API](#1-orchestration-api-multi-agent)
2. [Projects API](#2-projects-api)
3. [Tasks API](#3-tasks-api)
4. [Metrics API](#4-metrics-api)
5. [Agents API](#5-agents-configuration-api)
6. [HRM API](#6-hrm-hierarchical-reasoning-module-api)
7. [WebSocket API](#7-websocket-real-time-updates)
8. [Health & System](#8-health--system-endpoints)
9. [Data Models](#9-data-models-schemas)

---

## 1. Orchestration API (Multi-Agent)

### 1.1 Execute Task

**Execute a single task with smart agent selection**

```http
POST /api/orchestration/execute
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt": "Review code for security vulnerabilities",
  "task_type": "security",
  "files": ["src/**/*.py"],
  "workspace": "./project",
  "requires_security": true
}
```

**task_type Options:**
- `security` - Security analysis (→ Claude)
- `architecture` - Architecture design (→ Claude)
- `bulk_analysis` - Large file analysis (→ Gemini)
- `github_workflow` - GitHub operations (→ Copilot)
- `code_generation` - Generate code (→ Gemini)
- `debugging` - Debug issues (→ Adaptive)

**Response:**
```json
{
  "task_id": "uuid",
  "agent": "claude",
  "content": "Task output...",
  "tokens": 1523,
  "cost": 0.0046,
  "duration": 12.5,
  "session_id": "sess_xyz",
  "timestamp": "2025-11-10T12:00:00Z",
  "metadata": {}
}
```

### 1.2 Health Check

```http
GET /api/orchestration/health
```

**Response:**
```json
{
  "status": "healthy",
  "orchestrator": "initialized",
  "timestamp": "2025-11-10T12:00:00Z"
}
```

### 1.3 Circuit Breaker Status

```http
GET /api/orchestration/circuit-breaker-status
```

**Response:**
```json
{
  "timestamp": "2025-11-10T12:00:00Z",
  "circuit_breakers": {
    "claude": {
      "state": "closed",
      "failure_count": 0,
      "last_failure": null
    },
    "gemini": {
      "state": "closed",
      "failure_count": 0,
      "last_failure": null
    },
    "copilot": {
      "state": "open",
      "failure_count": 5,
      "last_failure": "2025-11-10T12:00:00Z"
    }
  }
}
```

**Circuit Breaker States:**
- `closed` - Healthy, accepting requests
- `open` - Failing, rejecting requests
- `half_open` - Testing recovery

---

## 2. Projects API

### 2.1 Get All Projects

```http
GET /api/projects
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "My Project",
    "type": "python",
    "status": "active",
    "github_repo": "https://github.com/user/repo",
    "slot": "Projekt-A",
    "config": {
      "priority": { "mode": "balanced" },
      "timeframe": { "max_minutes": 30, "preset": "standard" },
      "risk_tolerance": { "level": 50, "allow_experimental": false, "ml_features_enabled": true },
      "deployment": { "targets": ["windows"], "docker_enabled": false, "kubernetes_enabled": false },
      "ml_components": {
        "adaptive_iterations": true,
        "quality_weight_learning": true,
        "latent_reasoning": true,
        "agent_switching": true,
        "inference_time_scaling": true
      }
    },
    "total_tasks": 10,
    "successful_tasks": 8,
    "avg_quality": 0.87,
    "total_cost": 12.50,
    "created_at": "2025-11-10T12:00:00Z",
    "updated_at": "2025-11-10T12:00:00Z"
  }
]
```

**Project Types:**
- `python`
- `typescript`
- `react`
- `node`
- `general`

**Project Status:**
- `active`
- `paused`
- `archived`

### 2.2 Get Single Project

```http
GET /api/projects/{project_id}
```

### 2.3 Create Project

```http
POST /api/projects
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New Project",
  "type": "python",
  "github_repo": "https://github.com/user/repo",
  "config": {
    "priority": { "mode": "balanced" },
    "timeframe": { "max_minutes": 30, "preset": "standard" },
    "risk_tolerance": { "level": 50, "allow_experimental": false, "ml_features_enabled": true },
    "deployment": { "targets": ["windows"], "docker_enabled": false, "kubernetes_enabled": false },
    "ml_components": {
      "adaptive_iterations": true,
      "quality_weight_learning": true,
      "latent_reasoning": true,
      "agent_switching": true,
      "inference_time_scaling": true
    }
  }
}
```

**Note:** Max 3 projects (Projekt-A, Projekt-B, Projekt-C)

### 2.4 Update Project

```http
PUT /api/projects/{project_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "status": "paused",
  "github_repo": "https://github.com/user/new-repo",
  "config": { ... }
}
```

### 2.5 Delete Project

```http
DELETE /api/projects/{project_id}
```

### 2.6 Update Project Config

```http
PUT /api/projects/{project_id}/config
Content-Type: application/json
```

**Request Body:**
```json
{
  "priority": { "mode": "speed" },
  "timeframe": { "max_minutes": 15, "preset": "quick" },
  ...
}
```

---

## 3. Tasks API

### 3.1 Get Tasks (Paginated)

```http
GET /api/tasks?project_id={id}&status={status}&page={page}&page_size={size}
```

**Query Parameters:**
- `project_id` (optional) - Filter by project
- `status` (optional) - Filter by status (`pending`, `in_progress`, `completed`, `failed`)
- `page` (optional, default: 1) - Page number
- `page_size` (optional, default: 20, max: 100) - Items per page

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "project_id": "uuid",
      "issue_number": 123,
      "title": "Fix bug in authentication",
      "description": "...",
      "labels": ["bug", "security"],
      "status": "in_progress",
      "assigned_agent": "claude",
      "agent_switches": 1,
      "current_iteration": 2,
      "max_iterations": 5,
      "current_quality": 0.75,
      "final_quality": null,
      "tests_passing": false,
      "security_issues": 0,
      "started_at": "2025-11-10T12:00:00Z",
      "completed_at": null,
      "duration_seconds": null,
      "estimated_cost": 2.50,
      "actual_cost": null,
      "created_at": "2025-11-10T12:00:00Z",
      "updated_at": "2025-11-10T12:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 20,
  "total_pages": 3
}
```

### 3.2 Get Single Task

```http
GET /api/tasks/{task_id}
```

### 3.3 Retry Task

```http
POST /api/tasks/{task_id}/retry
```

### 3.4 Cancel Task

```http
POST /api/tasks/{task_id}/cancel
```

---

## 4. Metrics API

### 4.1 Dashboard Stats

```http
GET /api/metrics/dashboard
```

**Response:**
```json
{
  "total_projects": 3,
  "active_tasks": 5,
  "completed_today": 12,
  "total_cost_today": 8.75,
  "performance": {
    "avg_time_per_task": 1800.0,
    "avg_iterations": 3.5,
    "avg_quality": 0.87,
    "success_rate": 0.95,
    "token_reduction_percent": 65.0,
    "speed_improvement_factor": 3.8,
    "cost_savings_percent": 22.0
  },
  "cost": {
    "total_cost": 125.50,
    "cost_by_agent": {
      "claude": 45.00,
      "gemini": 0.00,
      "copilot": 30.00
    },
    "avg_cost_per_task": 2.50,
    "monthly_projection": 125.50,
    "savings_vs_all_claude": 35.14
  }
}
```

### 4.2 Quality Metrics

```http
GET /api/metrics/quality?project_id={id}&start_date={date}&end_date={date}
```

**Response:**
```json
[
  {
    "date": "2025-11-10T00:00:00Z",
    "overall_quality": 0.87,
    "test_coverage": 0.78,
    "security_score": 0.92
  }
]
```

### 4.3 Cost Metrics

```http
GET /api/metrics/cost?project_id={id}&period={period}
```

**Query Parameters:**
- `project_id` (optional)
- `period` (optional, default: 30d) - Options: `7d`, `30d`, `90d`

### 4.4 Agent Performance

```http
GET /api/metrics/agents?project_id={id}&period={period}
```

**Response:**
```json
[
  {
    "agent": "claude",
    "total_tasks": 25,
    "success_rate": 0.96,
    "avg_quality": 0.92,
    "avg_cost": 3.50,
    "avg_time": 1200.0
  },
  {
    "agent": "gemini",
    "total_tasks": 50,
    "success_rate": 0.88,
    "avg_quality": 0.85,
    "avg_cost": 0.00,
    "avg_time": 800.0
  }
]
```

### 4.5 Performance Metrics

```http
GET /api/metrics/performance?project_id={id}
```

---

## 5. Agents Configuration API

### 5.1 Get Agent Connections

```http
GET /api/agents/connections
```

**Response:**
```json
{
  "connections": [
    {
      "agent_id": "claude_main",
      "agent_name": "Claude Desktop",
      "connection_type": "local",
      "endpoint": null,
      "port": null,
      "api_key_id": null,
      "enabled": true
    }
  ]
}
```

**Connection Types:**
- `api` - Direct API connection
- `local` - Local CLI (claude.cmd)
- `remote` - Remote endpoint

### 5.2 Get Single Connection

```http
GET /api/agents/connections/{agent_id}
```

### 5.3 Create Agent Connection

```http
POST /api/agents/connections
Content-Type: application/json
```

**Request Body:**
```json
{
  "agent_id": "gemini_main",
  "agent_name": "Google Gemini",
  "connection_type": "api",
  "endpoint": "https://generativelanguage.googleapis.com",
  "port": null,
  "api_key_id": "key_123",
  "enabled": true
}
```

### 5.4 Update Agent Connection

```http
PUT /api/agents/connections/{agent_id}
Content-Type: application/json
```

### 5.5 Delete Agent Connection

```http
DELETE /api/agents/connections/{agent_id}
```

### 5.6 Get Config Files

```http
GET /api/agents/files?file_type={type}
```

**File Types:**
- `skill` - Claude skills (.claude/skills/*.md)
- `mcp` - MCP server configs
- `instruction` - Commands (.claude/commands/*.md)
- `config` - General configs

**Response:**
```json
{
  "files": [
    {
      "file_path": ".claude/skills/code-review.md",
      "file_type": "skill",
      "content": "# Code Review Skill\n...",
      "last_modified": "2025-11-10T12:00:00Z"
    }
  ]
}
```

### 5.7 Get Single Config File

```http
GET /api/agents/files/{file_path}
```

### 5.8 Update Config File

```http
PUT /api/agents/files/{file_path}
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "# Updated content..."
}
```

### 5.9 Create Config File

```http
POST /api/agents/files
Content-Type: application/json
```

### 5.10 Delete Config File

```http
DELETE /api/agents/files/{file_path}
```

---

## 6. HRM (Hierarchical Reasoning Module) API

### 6.1 Update HRM Config

```http
POST /api/hrm/config
Content-Type: application/json
```

**Request Body:**
```json
{
  "project_id": "uuid",
  "task_id": null,
  "config": {
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
  },
  "apply_immediately": true,
  "persist": true
}
```

**Agent Switching Strategies:**
- `cost_optimized` - Minimize cost (prefer Gemini)
- `quality_first` - Maximize quality (prefer Claude)
- `speed_optimized` - Maximize speed
- `adaptive` - Balance all factors (RL-based)
- `round_robin` - Rotate agents
- `manual` - Manual selection

**Response:**
```json
{
  "status": "applied",
  "config_id": "uuid",
  "applied_at": "2025-11-10T12:00:00Z",
  "impact_estimate": {
    "cost_change": -0.28,
    "speed_change": 0.30,
    "quality_change": 0.06,
    "token_reduction": 0.40
  },
  "active_tasks_affected": 3,
  "future_tasks_affected": true
}
```

### 6.2 Get HRM Config

```http
GET /api/hrm/config?project_id={id}&task_id={id}
```

**Response:**
```json
{
  "config_id": "uuid",
  "config": { ... },
  "preset_name": "balanced",
  "last_updated": "2025-11-10T12:00:00Z",
  "updated_by": "user@example.com"
}
```

### 6.3 Get HRM Presets

```http
GET /api/hrm/config/presets
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "balanced",
    "description": "Balanced performance, cost, and quality",
    "icon": "balance-scale",
    "color": "#3b82f6",
    "builtin": true,
    "config": { ... },
    "usage_stats": {
      "usage_count": 125,
      "avg_quality": 0.87,
      "avg_cost": 2.50,
      "avg_duration": 1200.0
    }
  }
]
```

**Built-in Presets:**
- `balanced` - Balanced (default)
- `cost_optimized` - Minimize cost
- `quality_first` - Maximize quality
- `speed` - Maximize speed

### 6.4 Create Custom Preset

```http
POST /api/hrm/config/presets
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "My Custom Preset",
  "description": "Optimized for my workflow",
  "icon": "custom",
  "color": "#10b981",
  "visibility": "private",
  "config": { ... }
}
```

**Visibility Options:**
- `private` - Only visible to creator
- `shared` - Visible to team
- `public` - Visible to all

### 6.5 Update Preset

```http
PUT /api/hrm/config/presets/{preset_id}
```

### 6.6 Delete Preset

```http
DELETE /api/hrm/config/presets/{preset_id}
```

**Note:** Cannot delete built-in presets

### 6.7 Apply Preset

```http
POST /api/hrm/config/presets/{preset_id}/apply?project_id={id}&apply_immediately={bool}
```

### 6.8 Simulate HRM Impact

```http
POST /api/hrm/simulate
Content-Type: application/json
```

**Request Body:**
```json
{
  "current_config": { ... },
  "proposed_config": { ... },
  "task_context": {
    "complexity": 10.0,
    "estimated_duration": 450,
    "current_quality": 0.87
  }
}
```

**Response:**
```json
{
  "impact_analysis": {
    "cost": {
      "current": 2.50,
      "predicted": 1.80,
      "change_percent": -28.0,
      "confidence": 0.85
    },
    "speed": {
      "current": 450,
      "predicted": 315,
      "change_percent": 30.0,
      "confidence": 0.80
    },
    "quality": {
      "current": 0.87,
      "predicted": 0.92,
      "change_percent": 6.0,
      "confidence": 0.82
    },
    "tokens": {
      "current": 50000,
      "predicted": 30000,
      "change_percent": -40.0,
      "confidence": 0.90
    }
  },
  "recommendations": [
    "Excellent cost optimization: 28% reduction predicted",
    "Speed improvement of 30% predicted"
  ],
  "warnings": []
}
```

### 6.9 Get Config History

```http
GET /api/hrm/config/history/{config_id}?limit={limit}
```

---

## 7. WebSocket (Real-Time Updates)

### 7.1 Global WebSocket

```javascript
const ws = new WebSocket("ws://localhost:1336/ws");

ws.onopen = () => {
  console.log("Connected to global channel");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
};

// Ping/Pong
ws.send(JSON.stringify({ type: "ping" }));

// Subscribe to additional channel
ws.send(JSON.stringify({
  type: "subscribe",
  channel: "project_123"
}));

// Unsubscribe
ws.send(JSON.stringify({
  type: "unsubscribe",
  channel: "project_123"
}));
```

### 7.2 Project-Specific WebSocket

```javascript
const ws = new WebSocket("ws://localhost:1336/ws/project/123");
```

### 7.3 Task-Specific WebSocket

```javascript
const ws = new WebSocket("ws://localhost:1336/ws/task/456");
```

### 7.4 WebSocket Events

**Connection Status:**
```json
{
  "type": "connection_status",
  "connected": true,
  "channel": "global",
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**Task Update:**
```json
{
  "type": "task_update",
  "task_id": "uuid",
  "status": "in_progress",
  "current_iteration": 2,
  "current_quality": 0.75,
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**Agent Switch:**
```json
{
  "type": "agent_switch",
  "task_id": "uuid",
  "from_agent": "gemini",
  "to_agent": "claude",
  "reason": "quality_threshold_not_met",
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**Feedback Loop:**
```json
{
  "type": "feedback_loop",
  "task_id": "uuid",
  "iteration": 2,
  "quality_score": 0.85,
  "suggestions": ["Add error handling", "Improve documentation"],
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**System Alert:**
```json
{
  "type": "system_alert",
  "message": "Circuit breaker OPEN for agent 'copilot'",
  "severity": "warning",
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**Severity Levels:**
- `info` - Informational
- `success` - Success
- `warning` - Warning
- `error` - Error

**HRM Config Update:**
```json
{
  "type": "hrm_config_update",
  "project_id": "uuid",
  "config_id": "uuid",
  "config": { ... },
  "impact": {
    "cost_change": -0.28,
    "speed_change": 0.30,
    "quality_change": 0.06,
    "token_reduction": 0.40
  },
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**HRM Impact Update (Real-time):**
```json
{
  "type": "hrm_impact_update",
  "task_id": "uuid",
  "metrics": {
    "current_cost": 1.25,
    "predicted_final_cost": 2.50,
    "tokens_used": 25000,
    "quality_trajectory": 0.82
  },
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**HRM Checkpoint Reached:**
```json
{
  "type": "hrm_checkpoint_reached",
  "task_id": "uuid",
  "checkpoint": {
    "progress": 0.33,
    "quality": 0.78,
    "passed": true,
    "suggestions": []
  },
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**HRM Preset Applied:**
```json
{
  "type": "hrm_preset_applied",
  "project_id": "uuid",
  "preset_name": "cost_optimized",
  "config": { ... },
  "timestamp": "2025-11-10T12:00:00Z"
}
```

**HRM Optimization Result:**
```json
{
  "type": "hrm_optimization_result",
  "task_id": "uuid",
  "optimization_type": "bayesian",
  "result": {
    "best_params": { ... },
    "improvement": 0.15
  },
  "timestamp": "2025-11-10T12:00:00Z"
}
```

### 7.5 WebSocket Health

```http
GET /api/ws/health
```

**Response:**
```json
{
  "status": "healthy",
  "native_ws": {
    "total_connections": 5,
    "channels": ["global", "project_123", "task_456"],
    "channel_counts": {
      "global": 3,
      "project_123": 1,
      "task_456": 1
    }
  },
  "socket_io": {
    "enabled": true,
    "status": "legacy_support"
  },
  "performance": {
    "protocol": "native_ws_primary",
    "improvement": "20-30% vs Socket.IO"
  }
}
```

---

## 8. Health & System Endpoints

### 8.1 System Health

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2025-11-10T12:00:00Z"
}
```

### 8.2 Metrics (Prometheus)

```http
GET /api/metrics
```

**Response:** Prometheus text format
```
# HELP phantom_api_requests_total Total API requests
# TYPE phantom_api_requests_total counter
phantom_api_requests_total{method="POST",endpoint="/api/orchestration/execute"} 125

# HELP phantom_api_duration_seconds API response time
# TYPE phantom_api_duration_seconds histogram
phantom_api_duration_seconds_bucket{method="POST",endpoint="/api/orchestration/execute",le="0.1"} 50
phantom_api_duration_seconds_bucket{method="POST",endpoint="/api/orchestration/execute",le="0.5"} 100
...
```

---

## 9. Data Models (Schemas)

### 9.1 Enums

**ProjectType:**
- `python`
- `typescript`
- `react`
- `node`
- `general`

**ProjectStatus:**
- `active`
- `paused`
- `archived`

**TaskStatus:**
- `pending`
- `in_progress`
- `completed`
- `failed`

**AgentType:**
- `claude`
- `gemini`
- `copilot`
- `cursor`
- `windsurf`
- `openai`
- `anthropic`
- `google`

### 9.2 Project Model

```typescript
interface Project {
  id: string;
  name: string;
  type: ProjectType;
  status: ProjectStatus;
  github_repo: string | null;
  slot: string; // "Projekt-A", "Projekt-B", "Projekt-C"
  config: ProjectConfiguration;
  total_tasks: number;
  successful_tasks: number;
  avg_quality: number;
  total_cost: number;
  created_at: string;
  updated_at: string;
}

interface ProjectConfiguration {
  priority: {
    mode: string;
    custom_weights?: Record<string, any>;
  };
  timeframe: {
    max_minutes: number;
    preset: string;
  };
  risk_tolerance: {
    level: number;
    allow_experimental: boolean;
    ml_features_enabled: boolean;
  };
  deployment: {
    targets: string[];
    docker_enabled: boolean;
    kubernetes_enabled: boolean;
  };
  ml_components: {
    adaptive_iterations: boolean;
    quality_weight_learning: boolean;
    latent_reasoning: boolean;
    agent_switching: boolean;
    inference_time_scaling: boolean;
  };
}
```

### 9.3 Task Model

```typescript
interface Task {
  id: string;
  project_id: string;
  issue_number: number;
  title: string;
  description: string | null;
  labels: string[];
  status: TaskStatus;
  assigned_agent: AgentType;
  agent_switches: number;
  current_iteration: number;
  max_iterations: number;
  current_quality: number;
  final_quality: number | null;
  tests_passing: boolean;
  security_issues: number;
  started_at: string | null;
  completed_at: string | null;
  duration_seconds: number | null;
  estimated_cost: number;
  actual_cost: number | null;
  created_at: string;
  updated_at: string;
}
```

### 9.4 HRM Config Model

```typescript
interface HRMConfig {
  latent_reasoning: {
    enabled: boolean;
    dimensionality: number; // 128-1024
    compression_ratio_target: number; // 1.0-10.0
    auto_adjust: boolean;
  };
  ml_iteration_prediction: {
    mode: "auto" | "manual" | "fixed";
    max_iterations: number; // 2-20
    confidence_threshold: number; // 0.0-1.0
  };
  agent_switching: {
    strategy: "cost_optimized" | "quality_first" | "speed_optimized" | "adaptive" | "round_robin" | "manual";
    quality_drop_threshold: number; // 0.0-1.0
    cost_ceiling: number;
    max_switches_per_task: number; // 0-10
  };
  deep_supervision: {
    enabled: boolean;
    checkpoints: number[]; // e.g., [0.33, 0.66, 1.00]
    quality_gate_threshold: number; // 0.0-1.0
  };
  parallel_evaluation: {
    enabled: boolean;
    worker_count: number; // 1-16
    timeout_seconds: number; // 10-300
  };
  caching: {
    memory: boolean;
    disk: boolean;
    remote: boolean;
    aggressive_mode: boolean;
    max_size_mb: number; // 100-5000
  };
  bayesian_optimization: {
    enabled: boolean;
    iterations: number; // 10-100
  };
  rl_refinement: {
    enabled: boolean;
    epsilon: number; // 0.0-1.0
    learning_rate: number; // 0.0001-0.1
  };
  prometheus_metrics: {
    enabled: boolean;
    export_interval: number; // 5-60
  };
  multi_repo: {
    enabled: boolean;
  };
}
```

### 9.5 Agent Connection Model

```typescript
interface AgentConnection {
  agent_id: string;
  agent_name: string;
  connection_type: "api" | "local" | "remote";
  endpoint: string | null;
  port: number | null;
  api_key_id: string | null;
  enabled: boolean;
}
```

---

## Error Responses

All endpoints may return these error responses:

**400 Bad Request:**
```json
{
  "detail": "Invalid request parameters"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error: {error message}"
}
```

---

## Rate Limiting

**No rate limiting currently enforced**

Recommended frontend implementation:
- Debounce config updates (500ms)
- Throttle WebSocket messages (100ms)
- Batch API calls when possible

---

## Authentication

**Currently no authentication required**

For production:
- Add Bearer token authentication
- Implement API key management
- Add role-based access control (RBAC)

---

## CORS Configuration

**Allowed Origins:**
- `http://localhost:3000`
- `http://localhost:5173`
- `http://localhost:1337`

---

## Environment Variables

**Backend Configuration:**
```bash
DATABASE_URL=sqlite:///./phantom.db
REDIS_URL=redis://localhost:6379
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## Notes for Frontend Implementation

1. **WebSocket Reconnection:** Implement automatic reconnection with exponential backoff
2. **Optimistic Updates:** Update UI immediately, rollback on error
3. **Polling Fallback:** If WebSocket fails, poll `/api/tasks/{id}` every 5 seconds
4. **Error Handling:** Show user-friendly error messages
5. **Loading States:** Show spinners for all async operations
6. **Caching:** Cache GET requests for projects/presets (invalidate on POST/PUT/DELETE)
7. **Real-time Sync:** Subscribe to relevant WebSocket channels based on current view
8. **Type Safety:** Use TypeScript interfaces from section 9
9. **Request Cancellation:** Cancel pending requests on component unmount
10. **Batch Requests:** Use `Promise.all()` for parallel independent requests

---

## Testing

**Test Backend Locally:**
```bash
# Health check
curl http://localhost:1336/api/health

# Get projects
curl http://localhost:1336/api/projects

# Execute task
curl -X POST http://localhost:1336/api/orchestration/execute \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test task", "task_type": "code_generation"}'

# WebSocket test
websocat ws://localhost:1336/ws
```

---

**Last Updated:** 2025-11-10
**Maintainer:** LEEI1337
**Documentation Version:** 2.0.0
