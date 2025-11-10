# Phantom Neural Cortex - Complete API Reference

**Version:** 2.0.0
**Base URL:** `http://localhost:1336/api`
**WebSocket URL:** `ws://localhost:1336/ws`
**Interactive Docs:** `http://localhost:1336/docs` (Swagger UI)

---

## Table of Contents

1. [Projects API](#projects-api) - 6 endpoints
2. [Tasks API](#tasks-api) - 4 endpoints
3. [Metrics API](#metrics-api) - 5 endpoints
4. [Configuration API](#configuration-api) - 2 endpoints
5. [HRM Configuration API](#hrm-configuration-api) - 7 endpoints
6. [Prometheus API](#prometheus-api) - 5 endpoints
7. [API Keys API](#api-keys-api) - 8 endpoints
8. [Swarm Orchestration API](#swarm-orchestration-api) - 7 endpoints
9. [Spec-Kit API](#spec-kit-api) - 10 endpoints
10. [Templates API](#templates-api) - 4 endpoints
11. [System API](#system-api) - 3 endpoints
12. [WebSocket Events](#websocket-events) - 13 event types

---

## Projects API

### GET /api/projects
Get all projects

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "name": "My Project",
    "type": "python",
    "status": "active",
    "github_repo": "owner/repo",
    "slot": "Projekt-A",
    "config": {
      "priority": {
        "mode": "balanced",
        "weights": {"quality": 0.4, "speed": 0.3, "cost": 0.3}
      },
      "timeframe": {"minutes": 30, "preset": "standard"},
      "risk": {"level": 50, "allow_experimental": false},
      "deployment": {"targets": ["kubernetes"], "docker_enabled": true},
      "ml_components": {
        "adaptive_iterations": true,
        "latent_reasoning": true,
        "agent_switching": true,
        "inference_time_scaling": false
      }
    },
    "statistics": {
      "total_tasks": 15,
      "completed": 12,
      "failed": 1,
      "avg_quality": 0.87
    }
  }
]
```

---

### POST /api/projects
Create new project

**Request Body:**
```json
{
  "name": "New Project",
  "type": "typescript",  // python | typescript | react | node | general
  "github_repo": "owner/repo",  // optional
  "config": {
    // ProjectConfiguration object (optional, uses defaults)
  }
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "name": "New Project",
  "slot": "Projekt-B",  // Auto-assigned to available slot
  "status": "active",
  "config": { /* default config */ }
}
```

---

### GET /api/projects/{project_id}
Get single project by ID

**Response:** `200 OK` - Same structure as GET /api/projects item

---

### PUT /api/projects/{project_id}
Update project

**Request Body (all fields optional):**
```json
{
  "name": "Updated Name",
  "status": "paused",  // active | paused | archived
  "github_repo": "new-owner/repo",
  "config": { /* partial config update */ }
}
```

**Response:** `200 OK` - Updated project object

---

### DELETE /api/projects/{project_id}
Delete project

**Response:** `200 OK`
```json
{
  "message": "Project {id} deleted successfully"
}
```

---

### PUT /api/projects/{project_id}/config
Update project configuration (5 dimensions)

**Request Body:**
```json
{
  "priority": {
    "mode": "quality",  // performance | cost | quality | balanced | custom
    "weights": {
      "quality": 0.7,
      "speed": 0.2,
      "cost": 0.1
    }
  },
  "timeframe": {
    "minutes": 60,
    "preset": "deep-work"  // sprint | standard | deep-work | marathon | custom
  },
  "risk": {
    "level": 75,  // 0-100
    "allow_experimental": true,
    "ml_features_enabled": true
  },
  "deployment": {
    "targets": ["linux", "kubernetes"],
    "docker_enabled": true,
    "kubernetes_enabled": true
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

**Response:** `200 OK` - Updated project with new config

---

## Tasks API

### GET /api/tasks
Get tasks with pagination and filtering

**Query Parameters:**
- `project_id` (optional) - Filter by project
- `status` (optional) - Filter by status: `pending | in_progress | completed | failed`
- `page` (default: 1) - Page number
- `page_size` (default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "uuid",
      "project_id": "uuid",
      "issue_number": 123,
      "title": "Implement authentication",
      "description": "Add OAuth2 support",
      "labels": ["security", "priority:high"],
      "status": "in_progress",
      "assigned_agent": "claude",
      "agent_switches": 2,
      "current_iteration": 3,
      "max_iterations": 10,
      "current_quality": 0.72,
      "final_quality": null,
      "tests_passing": true,
      "security_issues": 0,
      "started_at": "2025-11-09T10:00:00Z",
      "completed_at": null,
      "duration_seconds": null,
      "estimated_cost": 2.50,
      "actual_cost": 1.80
    }
  ],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

---

### GET /api/tasks/{task_id}
Get single task

**Response:** `200 OK` - Single task object (same structure as GET /api/tasks item)

---

### POST /api/tasks/{task_id}/retry
Retry failed task

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "status": "pending",
  "current_iteration": 0,
  "current_quality": 0.0,
  "message": "Task reset for retry"
}
```

---

### POST /api/tasks/{task_id}/cancel
Cancel running task

**Response:** `200 OK`
```json
{
  "message": "Task cancelled successfully"
}
```

---

## Metrics API

### GET /api/metrics/dashboard
Get dashboard overview statistics

**Response:** `200 OK`
```json
{
  "projects": {
    "total": 5,
    "active": 3,
    "paused": 1,
    "archived": 1
  },
  "tasks": {
    "total": 150,
    "active": 12,
    "completed_today": 8,
    "failed_today": 1,
    "success_rate": 0.92
  },
  "performance": {
    "avg_task_duration_seconds": 450,
    "avg_iterations": 4.2,
    "avg_quality_score": 0.85,
    "latent_compression_ratio": 3.8,
    "cache_hit_rate": 0.68
  },
  "cost": {
    "total_today": 12.50,
    "total_this_month": 280.00,
    "avg_cost_per_task": 1.75,
    "by_agent": {
      "claude": 120.00,
      "gemini": 0.00,
      "copilot": 40.00
    }
  }
}
```

---

### GET /api/metrics/quality
Get quality metrics trends

**Query Parameters:**
- `project_id` (optional) - Filter by project
- `start_date` (optional) - ISO 8601 date
- `end_date` (optional) - ISO 8601 date

**Response:** `200 OK`
```json
[
  {
    "date": "2025-11-01",
    "avg_quality": 0.82,
    "test_coverage": 0.78,
    "security_score": 0.91,
    "type_safety": 0.85,
    "task_count": 15
  },
  // ... 30-day trend data
]
```

---

### GET /api/metrics/cost
Get cost metrics

**Query Parameters:**
- `project_id` (optional)
- `period` (default: "30d") - `7d | 30d | 90d`

**Response:** `200 OK`
```json
{
  "total_cost": 280.00,
  "by_agent": {
    "claude": {"cost": 120.00, "percentage": 42.9},
    "gemini": {"cost": 0.00, "percentage": 0.0},
    "copilot": {"cost": 40.00, "percentage": 14.3},
    "other": {"cost": 120.00, "percentage": 42.9}
  },
  "avg_cost_per_task": 1.75,
  "projection_30d": 350.00,
  "daily_trend": [
    {"date": "2025-11-01", "cost": 12.50},
    // ... daily data
  ]
}
```

---

### GET /api/metrics/agents
Get agent performance comparison

**Query Parameters:**
- `project_id` (optional)
- `period` (default: "30d") - `7d | 30d | 90d`

**Response:** `200 OK`
```json
[
  {
    "agent": "claude",
    "tasks_completed": 45,
    "success_rate": 0.96,
    "avg_quality": 0.89,
    "avg_cost": 2.67,
    "avg_duration_seconds": 520
  },
  {
    "agent": "gemini",
    "tasks_completed": 120,
    "success_rate": 0.88,
    "avg_quality": 0.82,
    "avg_cost": 0.00,
    "avg_duration_seconds": 380
  }
]
```

---

### GET /api/metrics/performance
Get system performance metrics

**Query Parameters:**
- `project_id` (optional)

**Response:** `200 OK`
```json
{
  "avg_task_duration_seconds": 450,
  "avg_iterations": 4.2,
  "avg_quality_score": 0.85,
  "success_rate": 0.92,
  "latent_compression_ratio": 3.8,
  "token_reduction_percentage": 40.0,
  "cache_hit_rate": 0.68,
  "ml_iteration_accuracy": 0.82
}
```

---

## Configuration API

### GET /api/config/default
Get default project configuration

**Response:** `200 OK` - Returns full ProjectConfiguration object with defaults

---

### POST /api/config/validate
Validate configuration before applying

**Request Body:** ProjectConfiguration object

**Response:** `200 OK`
```json
{
  "valid": true,
  "errors": []
}
```

OR `400 Bad Request` if validation fails:
```json
{
  "valid": false,
  "errors": [
    "Timeframe must be between 5 and 180 minutes",
    "Risk level must be between 0 and 100"
  ]
}
```

---

## HRM Configuration API

The Hierarchical Reasoning Module (HRM) provides real-time control over 12 ML/RL optimization parameters. This API enables dynamic configuration changes, preset management, and impact simulation.

### POST /api/hrm/config
Update HRM configuration in real-time

**Request Body:**
```json
{
  "project_id": "uuid",
  "task_id": "uuid (optional)",
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
  "apply_immediately": false,
  "persist": true
}
```

**Response:** `200 OK`
```json
{
  "status": "applied|saved",
  "config_id": "uuid",
  "applied_at": "2025-11-09T12:34:56Z",
  "impact_estimate": {
    "cost_change": -0.15,
    "speed_change": 0.20,
    "quality_change": -0.05,
    "token_reduction": 0.40
  },
  "active_tasks_affected": 3,
  "future_tasks_affected": true
}
```

**WebSocket Events Emitted:**
- `hrm_config_update` - Real-time config update
- `system_alert` - If applied to active tasks

---

### GET /api/hrm/config
Get current HRM configuration

**Query Parameters:**
- `project_id` (optional) - Project ID
- `task_id` (optional) - Task ID

**Response:** `200 OK` - Returns full HRM configuration object

---

### POST /api/hrm/simulate
Simulate impact of configuration change before applying

**Request Body:**
```json
{
  "current_config": { /* HRM config object */ },
  "proposed_config": { /* HRM config object */ },
  "task_context": {
    "complexity": 12.5,
    "estimated_duration": 450,
    "current_quality": 0.87
  }
}
```

**Response:** `200 OK`
```json
{
  "impact_analysis": {
    "cost": {
      "current": 2.50,
      "predicted": 2.13,
      "change_percent": -15.0,
      "confidence": 0.85
    },
    "speed": {
      "current": 450,
      "predicted": 360,
      "change_percent": -20.0,
      "confidence": 0.85
    },
    "quality": {
      "current": 0.87,
      "predicted": 0.83,
      "change_percent": -4.6,
      "confidence": 0.80
    },
    "tokens": {
      "current": 50000,
      "predicted": 30000,
      "change_percent": -40.0,
      "confidence": 0.90
    }
  },
  "warnings": [
    "Quality may decrease by 5%"
  ],
  "recommendations": [
    "Consider enabling deep supervision to maintain quality"
  ]
}
```

---

### GET /api/hrm/config/presets
List all available HRM presets

**Query Parameters:**
- `include_builtin` (default: true) - Include built-in presets
- `visibility` (optional) - Filter by visibility (public|private|team)

**Response:** `200 OK`
```json
{
  "presets": [
    {
      "id": "uuid",
      "name": "speed_optimized",
      "description": "Maximum speed with acceptable quality trade-offs",
      "icon": "⚡",
      "color": "#FFD700",
      "builtin": true,
      "config": { /* Full HRM config */ },
      "usage_stats": {
        "usage_count": 142,
        "avg_quality": 0.82,
        "avg_cost": 1.85,
        "avg_duration": 320
      }
    },
    {
      "id": "uuid",
      "name": "cost_optimized",
      "description": "Minimize API costs while maintaining good quality",
      "icon": "💰",
      "color": "#4CAF50",
      "builtin": true,
      "config": { /* Full HRM config */ }
    },
    {
      "id": "uuid",
      "name": "quality_first",
      "description": "Maximum quality regardless of cost or time",
      "icon": "🎯",
      "color": "#9C27B0",
      "builtin": true,
      "config": { /* Full HRM config */ }
    },
    {
      "id": "uuid",
      "name": "balanced",
      "description": "Balanced configuration for general-purpose use",
      "icon": "⚖️",
      "color": "#2196F3",
      "builtin": true,
      "config": { /* Full HRM config */ }
    }
  ]
}
```

---

### POST /api/hrm/config/presets
Create custom HRM preset

**Request Body:**
```json
{
  "name": "my_custom_preset",
  "description": "My optimized settings",
  "icon": "🚀",
  "color": "#FF5722",
  "config": { /* Full HRM config object */ },
  "visibility": "private"
}
```

**Response:** `201 Created` - Returns HRMPresetResponse

---

### POST /api/hrm/config/presets/{preset_id}/apply
Apply an HRM preset to a project

**Path Parameters:**
- `preset_id` - Preset ID to apply

**Query Parameters:**
- `project_id` (required) - Project ID to apply preset to
- `apply_immediately` (default: false) - Apply to running tasks

**Response:** `200 OK`
```json
{
  "status": "applied",
  "config_id": "uuid",
  "applied_at": "2025-11-09T12:34:56Z",
  "impact_estimate": {
    "cost_change": -0.40,
    "speed_change": 0.35,
    "quality_change": -0.08,
    "token_reduction": 0.45
  },
  "active_tasks_affected": 5,
  "future_tasks_affected": true
}
```

**WebSocket Events Emitted:**
- `hrm_preset_applied` - Preset applied notification
- `hrm_config_update` - Config update notification
- `system_alert` - If applied to active tasks

---

### GET /api/hrm/config/history/{config_id}
Get configuration change history

**Path Parameters:**
- `config_id` - HRM configuration ID

**Response:** `200 OK`
```json
{
  "history": [
    {
      "id": "uuid",
      "config_id": "uuid",
      "changed_by": "user@example.com",
      "changed_at": "2025-11-09T12:34:56Z",
      "change_type": "update|create|preset_applied",
      "old_config": { /* Previous config */ },
      "new_config": { /* New config */ },
      "task_id": "uuid (optional)",
      "impact_metrics": {
        "cost_change": -0.15,
        "speed_change": 0.20,
        "quality_change": -0.05,
        "token_reduction": 0.40
      }
    }
  ]
}
```

---

## Prometheus API

### GET /api/metrics
Prometheus metrics export (text format)

**Response:** `200 OK` (Content-Type: text/plain)
```
# HELP lazybird_quality_score Task quality score percentage
# TYPE lazybird_quality_score gauge
lazybird_quality_score{project_id="uuid",task_id="uuid"} 87.5

# HELP lazybird_tasks_completed_total Total completed tasks
# TYPE lazybird_tasks_completed_total counter
lazybird_tasks_completed_total{project_id="uuid",status="completed"} 45

# ... 40+ custom metrics
```

---

### POST /api/metrics/task-completion
Record task completion metric

**Query Parameters:**
- `project_id` - Project UUID
- `task_id` - Task UUID
- `project_type` - Project type
- `quality_score` - 0.0-1.0
- `duration_seconds` - Duration
- `iteration_count` - Iterations used
- `status` - `completed | failed`
- `priority_mode` - Priority mode

**Response:** `200 OK`

---

### POST /api/metrics/token-usage
Record token usage

**Query Parameters:**
- `agent_type` - Agent name
- `prompt_tokens` - Prompt tokens count
- `completion_tokens` - Completion tokens count
- `cost_usd` - Cost in USD
- `project_type` - Project type

**Response:** `200 OK`

---

### POST /api/metrics/agent-switch
Record agent switch event

**Query Parameters:**
- `from_agent` - Source agent
- `to_agent` - Target agent
- `reason` - Switch reason

**Response:** `200 OK`

---

### POST /api/metrics/cache-operation
Record cache operation

**Query Parameters:**
- `cache_type` - Cache layer (memory/disk/remote)
- `operation` - `hit | miss | write`
- `size_bytes` (optional) - Data size

**Response:** `200 OK`

---

## API Keys API

### POST /api/api-keys/keys
Create new API key

**Request Body:**
```json
{
  "provider": "anthropic",  // anthropic | openai | google | cohere | mistral | ollama | groq | together
  "key_name": "Production Claude Key",
  "api_key": "sk-ant-xxx",
  "weight": 1.0,  // For weighted load balancing
  "budgets": {
    "daily_limit": 50.00,
    "monthly_limit": 1000.00
  },
  "rate_limit": 60,  // Requests per minute
  "enabled": true
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "provider": "anthropic",
  "key_name": "Production Claude Key",
  "key_preview": "sk-ant-xxx...xxx",  // Masked
  "weight": 1.0,
  "enabled": true,
  "created_at": "2025-11-09T10:00:00Z",
  "usage": {
    "requests_today": 0,
    "cost_today": 0.00,
    "requests_month": 0,
    "cost_month": 0.00
  }
}
```

---

### GET /api/api-keys/keys
List all API keys

**Query Parameters:**
- `provider` (optional) - Filter by provider
- `enabled_only` (default: false) - Only enabled keys

**Response:** `200 OK` - Array of APIKeyResponse objects

---

### GET /api/api-keys/keys/{key_id}
Get single API key

**Response:** `200 OK` - APIKeyResponse object

---

### PATCH /api/api-keys/keys/{key_id}
Update API key (partial update)

**Request Body (all fields optional):**
```json
{
  "key_name": "Updated Name",
  "weight": 2.0,
  "enabled": false,
  "rate_limit": 100
}
```

**Response:** `200 OK` - Updated APIKeyResponse

---

### DELETE /api/api-keys/keys/{key_id}
Delete API key

**Response:** `204 No Content`

---

### POST /api/api-keys/load-balancing/{provider}
Configure load balancing for provider

**Request Body:**
```json
{
  "strategy": "weighted",  // round_robin | weighted | cost_optimized | failover | random
  "enabled": true,
  "failover_enabled": true,
  "health_check_interval": 300  // seconds
}
```

**Response:** `200 OK` - LoadBalancingConfig object

---

### GET /api/api-keys/load-balancing/{provider}
Get load balancing configuration

**Response:** `200 OK` - LoadBalancingConfig object

---

### GET /api/api-keys/stats/{provider}
Get provider statistics

**Response:** `200 OK`
```json
{
  "total_keys": 3,
  "active_keys": 2,
  "total_requests": 1250,
  "total_cost": 45.00,
  "avg_latency_ms": 520,
  "success_rate": 0.98,
  "current_rps": 12.5
}
```

---

### POST /api/api-keys/keys/{key_id}/test
Test API key validity

**Response:** `200 OK`
```json
{
  "success": true,
  "provider": "anthropic",
  "key_preview": "sk-ant-xxx...xxx",
  "test_timestamp": "2025-11-09T10:00:00Z",
  "latency_ms": 245,
  "message": "API key is valid and working"
}
```

---

## Swarm Orchestration API

### GET /api/swarm/configs
Get all swarm configurations

**Response:** `200 OK` - Array of SwarmConfig objects (presets + user configs)

---

### GET /api/swarm/configs/presets
Get preset configurations only

**Response:** `200 OK`
```json
[
  {
    "name": "speed_optimized",
    "description": "Maximum speed, minimal quality checks",
    "parallelization": {
      "max_parallel_tasks": 10,
      "max_parallel_agents": 5,
      "auto_scale": true
    },
    "intelligence_mode": "speed",
    "feedback_loop": {
      "adaptive_iterations": true,
      "max_iterations": 2
    },
    "cost_control": {
      "daily_budget": null,
      "prefer_cheaper_models": true
    }
  },
  {
    "name": "cost_optimized",
    // ...
  },
  {
    "name": "quality_first",
    // ...
  }
]
```

---

### POST /api/swarm/configs
Create custom swarm configuration

**Request Body:** SwarmConfig object (7 dimensions)

**Response:** `201 Created` - Created SwarmConfig

---

### GET /api/swarm/configs/{config_name}
Get specific swarm configuration

**Response:** `200 OK` - SwarmConfig object

---

### PUT /api/swarm/configs/{config_name}
Update swarm configuration

**Note:** Cannot update preset configs (speed_optimized, cost_optimized, quality_first)

**Request Body:** SwarmConfig object

**Response:** `200 OK` - Updated SwarmConfig

---

### DELETE /api/swarm/configs/{config_name}
Delete custom swarm configuration

**Note:** Cannot delete preset configs

**Response:** `204 No Content`

---

### GET /api/swarm/stats
Get swarm performance statistics

**Response:** `200 OK`
```json
{
  "tasks": {
    "total": 150,
    "active": 12,
    "queued": 8
  },
  "quality": {
    "avg_quality": 0.87,
    "avg_iterations": 4.2
  },
  "cost": {
    "total_cost": 280.00,
    "avg_cost_per_task": 1.75
  },
  "cache": {
    "hit_rate": 0.68,
    "total_hits": 1250
  },
  "agents": {
    "claude": 45,
    "gemini": 120,
    "copilot": 30
  }
}
```

---

### POST /api/swarm/optimize
Get optimization recommendations

**Request Body:**
```json
{
  "cache_hit_rate": 0.68,
  "avg_iterations": 4.2,
  "avg_quality_score": 0.87
}
```

**Response:** `200 OK`
```json
{
  "recommendations": [
    "Increase cache size to 1GB for 15% better hit rate",
    "Enable aggressive caching for repetitive tasks"
  ],
  "confidence": 0.85,
  "estimated_improvement": {
    "cost_reduction": 0.12,
    "speed_improvement": 0.08
  }
}
```

---

## Spec-Kit API

### POST /api/speckit/projects
Initialize Spec-Kit for project

**Query Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "project_id": "uuid",
  "project_path": "/path/to/project",
  "ai_agent": "claude",
  "enable_latent_reasoning": true,
  "enable_rl_refinement": true,
  "enable_smart_switching": true
}
```

**Response:** `201 Created`
```json
{
  "project_id": "uuid",
  "speckit_initialized": true,
  "specify_dir": "/path/to/project/.specify",
  "optimizations": {
    "latent_reasoning": true,
    "rl_refinement": true,
    "smart_switching": true
  }
}
```

---

### POST /api/speckit/features
Create new feature

**Query Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "feature_id": "user-auth",
  "name": "User Authentication",
  "description": "OAuth2 + JWT authentication system"
}
```

**Response:** `201 Created`
```json
{
  "feature_id": "user-auth",
  "name": "User Authentication",
  "description": "OAuth2 + JWT authentication system",
  "current_phase": "constitution",
  "completed_phases": [],
  "estimated_iterations": 7,  // ML-predicted
  "optimal_agent": "claude",  // Auto-selected
  "complexity_score": 12.5
}
```

---

### GET /api/speckit/features
Get all features

**Query Parameters:**
- `project_id` - Project UUID

**Response:** `200 OK` - Array of FeatureResponse objects

---

### GET /api/speckit/features/{feature_id}
Get single feature

**Query Parameters:**
- `project_id` - Project UUID

**Response:** `200 OK` - FeatureResponse object

---

### POST /api/speckit/phases/constitution
Run Constitution phase

**Query Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "feature_id": "user-auth",
  "principles": [
    "Security-first approach with zero trust",
    "OAuth2 compliance",
    "Minimal user friction"
  ]
}
```

**Response:** `200 OK`
```json
{
  "phase": "constitution",
  "status": "completed",
  "output": {
    "principles": [...],
    "constraints": [...],
    "success_criteria": [...]
  }
}
```

---

### POST /api/speckit/phases/specify
Run Specification phase

**Query Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "feature_id": "user-auth",
  "user_stories": [
    "As a user, I want to login with Google OAuth",
    "As an admin, I want to revoke user tokens"
  ],
  "requirements": [
    "Support OAuth2 providers: Google, GitHub",
    "JWT token expiry: 24 hours"
  ]
}
```

**Response:** `200 OK` - PhaseResponse object

---

### POST /api/speckit/phases/plan
Run Planning phase

**Query Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "feature_id": "user-auth",
  "architecture": "Microservices with API Gateway",
  "tech_stack": ["FastAPI", "PostgreSQL", "Redis"],
  "components": [
    {"name": "AuthService", "type": "backend"},
    {"name": "TokenManager", "type": "library"}
  ]
}
```

**Response:** `200 OK` - PhaseResponse object

---

### POST /api/speckit/phases/tasks
Generate tasks

**Query Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "feature_id": "user-auth",
  "tasks": [
    {
      "title": "Setup OAuth2 providers",
      "description": "Configure Google & GitHub OAuth",
      "priority": "high",
      "estimated_hours": 4
    }
  ]
}
```

**Response:** `200 OK` - PhaseResponse with task list

---

### POST /api/speckit/phases/implement
Run Implementation phase

**Query Parameters:**
- `project_id` - Project UUID

**Request Body:**
```json
{
  "feature_id": "user-auth",
  "async_execution": true
}
```

**Response:** `202 Accepted` (if async)
```json
{
  "feature_id": "user-auth",
  "phase": "implement",
  "status": "running",
  "completed_tasks": 0,
  "failed_tasks": 0,
  "execution_id": "uuid"
}
```

---

### GET /api/speckit/status/{feature_id}
Get feature status

**Query Parameters:**
- `project_id` - Project UUID

**Response:** `200 OK`
```json
{
  "feature_id": "user-auth",
  "name": "User Authentication",
  "current_phase": "implement",
  "completed_phases": ["constitution", "specify", "plan", "tasks"],
  "progress_percentage": 65,
  "ultrathink_metrics": {
    "latent_compression_ratio": 3.8,
    "ml_predicted_iterations": 7,
    "actual_iterations": 5,
    "agent_switches": 2
  }
}
```

---

## Templates API

### GET /api/templates
Get all templates

**Response:** `200 OK`
```json
{
  "templates": [
    {
      "id": "production-web-app",
      "name": "Production Web Application",
      "description": "Full-stack web app with ML optimizations",
      "icon": "🚀"
    },
    {
      "id": "data-science-pipeline",
      "name": "Data Science Pipeline",
      "description": "ML/AI pipeline with data processing",
      "icon": "📊"
    },
    {
      "id": "microservices-platform",
      "name": "Microservices API Platform",
      "description": "Scalable microservices architecture",
      "icon": "🔧"
    }
  ]
}
```

---

### GET /api/templates/{template_id}
Get template details

**Response:** `200 OK`
```json
{
  "id": "production-web-app",
  "name": "Production Web Application",
  "description": "Full-stack web app with ML optimizations",
  "guidelines": [
    "Follow 12-factor app principles",
    "Implement CI/CD pipeline",
    "Use containerization"
  ],
  "prerequisites": [
    "Docker installed",
    "Kubernetes cluster (optional)",
    "PostgreSQL database"
  ],
  "tech_stack": ["React", "FastAPI", "PostgreSQL", "Redis"],
  "estimated_duration": "2-4 weeks",
  "complexity": "Medium-High"
}
```

---

### POST /api/templates/{template_id}/apply
Apply template to project

**Query Parameters:**
- `project_name` - Name for new project
- `customizations` (optional) - JSON customization object

**Response:** `201 Created`
```json
{
  "project_name": "My New Project",
  "template_id": "production-web-app",
  "template_name": "Production Web Application",
  "applied_config": { /* ProjectConfiguration */ },
  "guidelines": [...],
  "prerequisites": [...],
  "next_steps": [
    "Run docker-compose up",
    "Initialize database",
    "Configure environment variables"
  ]
}
```

---

### GET /api/templates/guidelines/best-practices
Get best practices by category

**Query Parameters:**
- `category` (optional) - `security | testing | performance | code_quality`

**Response:** `200 OK`
```json
{
  "security": {
    "practices": [
      "Always validate and sanitize user inputs",
      "Use parameterized queries to prevent SQL injection",
      "Implement rate limiting on all public endpoints"
    ]
  },
  "testing": {
    "practices": [
      "Maintain minimum 70% test coverage",
      "Write integration tests for critical paths",
      "Use pytest fixtures for test data"
    ]
  }
}
```

---

## System API

### GET /api/health
System health check

**Response:** `200 OK`
```json
{
  "status": "HEALTHY",  // HEALTHY | DEGRADED
  "version": "2.0.0",
  "uptime": "2 days, 14:32:15",
  "uptime_seconds": 225135,
  "started_at": "2025-11-07T08:00:00Z",
  "current_time": "2025-11-09T22:32:15Z",
  "components": {
    "database": {
      "status": "healthy",
      "latency_ms": 12
    },
    "websocket": {
      "status": "healthy",
      "connections": 5
    },
    "cache": {
      "status": "healthy",
      "hit_rate": 0.68
    }
  },
  "metrics": {
    "total_projects": 5,
    "active_tasks": 12,
    "requests_per_second": 15.2
  }
}
```

---

### GET /api/cache-stats
Get cache statistics

**Response:** `200 OK`
```json
{
  "guideline_cache": {
    "size": 1250,
    "hits": 8500,
    "misses": 1250,
    "hit_rate": 0.87
  },
  "github_cache": {
    "size": 850,
    "hits": 5200,
    "misses": 800,
    "hit_rate": 0.87
  },
  "quality_pattern_cache": {
    "size": 450,
    "hits": 3200,
    "misses": 450,
    "hit_rate": 0.88
  }
}
```

---

### POST /api/clear-cache
Clear cache layers

**Query Parameters:**
- `layer` (optional) - `guideline | github | quality` (if not specified, clears all)

**Response:** `200 OK`
```json
{
  "status": "success",
  "cleared_layers": ["guideline", "github", "quality"],
  "message": "All caches cleared successfully"
}
```

---

## WebSocket Events

**Connection URL:** `ws://localhost:1336/ws`

**Protocol:** Socket.IO

### Client Events (Emit to Server)

#### 1. subscribe_project
Subscribe to project updates

**Emit:**
```javascript
socket.emit('subscribe_project', {
  project_id: 'uuid'
});
```

---

#### 2. unsubscribe_project
Unsubscribe from project

**Emit:**
```javascript
socket.emit('unsubscribe_project', {
  project_id: 'uuid'
});
```

---

### Server Events (Listen from Server)

#### 1. connection_status
Connection lifecycle events

**Receive:**
```javascript
socket.on('connection_status', (data) => {
  // data.status: 'connected' | 'disconnected'
  // data.timestamp: ISO 8601 timestamp
});
```

---

#### 2. task_update
Real-time task progress

**Receive:**
```javascript
socket.on('task_update', (data) => {
  // {
  //   task_id: 'uuid',
  //   status: 'in_progress',
  //   current_iteration: 3,
  //   current_quality: 0.72,
  //   progress_percentage: 45
  // }
});
```

---

#### 3. feedback_loop
ML feedback loop iteration updates

**Receive:**
```javascript
socket.on('feedback_loop', (data) => {
  // {
  //   task_id: 'uuid',
  //   iteration: 3,
  //   quality_snapshot: {
  //     overall_quality: 0.72,
  //     test_coverage: 0.68,
  //     security_score: 0.88
  //   },
  //   decision: 'continue' | 'stop' | 'refine'
  // }
});
```

---

#### 4. quality_update
Quality metrics changes

**Receive:**
```javascript
socket.on('quality_update', (data) => {
  // {
  //   task_id: 'uuid',
  //   metrics: {
  //     test_coverage: 0.78,
  //     security_score: 0.91,
  //     type_safety: 0.85
  //   }
  // }
});
```

---

#### 5. cost_update
Cost tracking updates

**Receive:**
```javascript
socket.on('cost_update', (data) => {
  // {
  //   task_id: 'uuid',
  //   agent: 'claude',
  //   tokens_used: 1250,
  //   cost: 0.015
  // }
});
```

---

#### 6. agent_switch
Agent switching events

**Receive:**
```javascript
socket.on('agent_switch', (data) => {
  // {
  //   task_id: 'uuid',
  //   from_agent: 'gemini',
  //   to_agent: 'claude',
  //   reason: 'Security analysis required',
  //   timestamp: '2025-11-09T10:00:00Z'
  // }
});
```

---

#### 7. system_alert
Critical system notifications

**Receive:**
```javascript
socket.on('system_alert', (data) => {
  // {
  //   message: 'Budget limit reached',
  //   severity: 'warning' | 'error' | 'critical',
  //   timestamp: '2025-11-09T10:00:00Z',
  //   action_required: true
  // }
});
```

---

#### 8. project_stats
Project-level statistics

**Receive:**
```javascript
socket.on('project_stats', (data) => {
  // {
  //   project_id: 'uuid',
  //   active_tasks: 5,
  //   avg_quality: 0.87,
  //   total_cost: 12.50
  // }
});
```

---

#### 9. hrm_config_update
HRM configuration updated in real-time

**Receive:**
```javascript
socket.on('hrm_config_update', (data) => {
  // {
  //   project_id: 'uuid',
  //   config_id: 'uuid',
  //   config: { /* Full HRM configuration */ },
  //   impact: {
  //     cost_change: -0.15,
  //     speed_change: 0.20,
  //     quality_change: -0.05,
  //     token_reduction: 0.40
  //   },
  //   timestamp: '2025-11-09T12:34:56Z'
  // }
});
```

---

#### 10. hrm_impact_update
Real-time HRM impact metrics during task execution

**Receive:**
```javascript
socket.on('hrm_impact_update', (data) => {
  // {
  //   task_id: 'uuid',
  //   metrics: {
  //     tokens_saved: 20000,
  //     iterations_saved: 2,
  //     cost_savings: 1.25,
  //     time_saved_seconds: 120
  //   },
  //   timestamp: '2025-11-09T12:34:56Z'
  // }
});
```

---

#### 11. hrm_checkpoint_reached
Deep supervision checkpoint reached

**Receive:**
```javascript
socket.on('hrm_checkpoint_reached', (data) => {
  // {
  //   task_id: 'uuid',
  //   checkpoint: {
  //     checkpoint_percent: 33,
  //     quality_score: 0.87,
  //     should_rollback: false,
  //     checkpoint_id: 'uuid',
  //     metrics: {
  //       test_coverage: 0.82,
  //       security_score: 0.91
  //     }
  //   },
  //   timestamp: '2025-11-09T12:34:56Z'
  // }
});
```

---

#### 12. hrm_preset_applied
HRM preset applied to project

**Receive:**
```javascript
socket.on('hrm_preset_applied', (data) => {
  // {
  //   project_id: 'uuid',
  //   preset_name: 'speed_optimized',
  //   config: { /* Full HRM configuration from preset */ },
  //   timestamp: '2025-11-09T12:34:56Z'
  // }
});
```

---

#### 13. hrm_optimization_result
ML/RL optimization result

**Receive:**
```javascript
socket.on('hrm_optimization_result', (data) => {
  // {
  //   task_id: 'uuid',
  //   optimization_type: 'bayesian' | 'rl_refinement' | 'agent_switching',
  //   result: {
  //     success: true,
  //     iterations_used: 5,
  //     improvement_percent: 12.5,
  //     new_parameters: { /* Optimized parameters */ }
  //   },
  //   timestamp: '2025-11-09T12:34:56Z'
  // }
});
```

---

## Error Responses

All API endpoints may return these error responses:

### 400 Bad Request
Invalid request parameters

```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "timeframe.minutes",
      "message": "Must be between 5 and 180"
    }
  ]
}
```

---

### 404 Not Found
Resource not found

```json
{
  "detail": "Project with id {uuid} not found"
}
```

---

### 500 Internal Server Error
Server error

```json
{
  "detail": "Internal server error",
  "error_id": "uuid"
}
```

---

## Rate Limiting

**Global Rate Limit:** 100 requests/minute per IP (configurable)

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1699545600
```

---

## Authentication

**Current:** No authentication required (development mode)

**Production:** Will implement JWT-based authentication:
```
Authorization: Bearer {jwt_token}
```

---

## Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page` (default: 1)
- `page_size` (default: 20, max: 100)

**Response includes:**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

---

## CORS Configuration

**Allowed Origins:**
- `http://localhost:1337` (Frontend dev server)
- `http://localhost:3000` (Alternative dev port)
- Production domains (configure in backend)

---

## Versioning

**Current Version:** 2.0.0

**API Versioning Strategy:** URL-based (future: `/api/v2/...`)

---

**Last Updated:** 2025-11-09
**Maintainer:** Phantom Neural Cortex Team
