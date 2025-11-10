"""
SQLAlchemy Database Models
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class ProjectType(str, enum.Enum):
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    REACT = "react"
    NODE = "node"
    GENERAL = "general"


class ProjectStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentType(str, enum.Enum):
    CLAUDE = "claude"
    GEMINI = "gemini"
    COPILOT = "copilot"
    CURSOR = "cursor"
    WINDSURF = "windsurf"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(SQLEnum(ProjectType), nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.ACTIVE)
    github_repo = Column(String, nullable=True)
    slot = Column(String, nullable=False)  # "Projekt-A", "Projekt-B", etc.

    # 5-Dimension Configuration (stored as JSON)
    config = Column(JSON, nullable=False)

    # Statistics
    total_tasks = Column(Integer, default=0)
    successful_tasks = Column(Integer, default=0)
    avg_quality = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    issue_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    labels = Column(JSON, default=list)  # List of strings
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)

    # Agent Info
    assigned_agent = Column(SQLEnum(AgentType), nullable=False)
    agent_switches = Column(Integer, default=0)

    # Progress
    current_iteration = Column(Integer, default=0)
    max_iterations = Column(Integer, default=5)
    current_quality = Column(Float, default=0.0)

    # Results
    final_quality = Column(Float, nullable=True)
    tests_passing = Column(Boolean, default=False)
    security_issues = Column(Integer, default=0)

    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Cost
    estimated_cost = Column(Float, default=0.0)
    actual_cost = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="tasks")
    quality_snapshots = relationship("QualitySnapshot", back_populates="task", cascade="all, delete-orphan")


class QualitySnapshot(Base):
    __tablename__ = "quality_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    iteration = Column(Integer, nullable=False)

    # Quality Metrics
    overall_quality = Column(Float, nullable=False)
    test_coverage = Column(Float, default=0.0)
    tests_passing = Column(Boolean, default=False)
    security_score = Column(Float, default=0.0)
    code_quality_score = Column(Float, default=0.0)
    type_safety = Column(Float, default=0.0)
    documentation = Column(Float, default=0.0)

    # Details
    vulnerabilities = Column(Integer, default=0)
    type_errors = Column(Integer, default=0)
    complexity = Column(Float, default=0.0)
    failing_test_count = Column(Integer, nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="quality_snapshots")


class CostTracking(Base):
    __tablename__ = "cost_tracking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=True)
    agent = Column(SQLEnum(AgentType), nullable=False)

    # Cost Details
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, nullable=False)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)


class AgentSwitch(Base):
    __tablename__ = "agent_switches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    from_agent = Column(SQLEnum(AgentType), nullable=False)
    to_agent = Column(SQLEnum(AgentType), nullable=False)
    reason = Column(String, nullable=False)
    trigger = Column(String, nullable=False)
    cost_impact = Column(Float, default=0.0)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)


class HRMConfig(Base):
    """Hierarchical Resource Management Configuration per project/task"""
    __tablename__ = "hrm_configs"

    id = Column(String, primary_key=True)  # UUID string for compatibility with router
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)  # Made nullable for global configs
    task_id = Column(String, ForeignKey("tasks.id"), nullable=True)

    # Core fields used by router
    name = Column(String, nullable=True)  # Config name (e.g., "Custom Configuration", "Preset: balanced")
    config = Column(JSON, nullable=False)  # Complete HRM configuration object
    created_by = Column(String, nullable=True)  # User who created this config

    # Legacy fields - kept for backward compatibility and metadata
    dimension_config = Column(JSON, nullable=True)  # 5-dimension config (legacy)
    agent_preferences = Column(JSON, nullable=True)  # Agent preferences (legacy)

    # Resource Constraints
    max_iterations = Column(Integer, default=5)
    max_cost = Column(Float, nullable=True)
    max_duration_seconds = Column(Float, nullable=True)

    # Quality Thresholds
    quality_threshold = Column(Float, default=0.8)
    test_coverage_threshold = Column(Float, default=0.8)
    security_threshold = Column(Float, default=0.9)

    # Status
    is_active = Column(Boolean, default=True)
    is_preset = Column(Boolean, default=False)
    preset_name = Column(String, nullable=True)

    # Usage Tracking
    total_executions = Column(Integer, default=0)
    successful_executions = Column(Integer, default=0)
    total_tokens_used = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HRMConfigHistory(Base):
    """Audit log for HRM configuration changes"""
    __tablename__ = "hrm_config_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(String, ForeignKey("hrm_configs.id"), nullable=False)  # Renamed from hrm_config_id to match router

    # Change tracking
    changed_by = Column(String, nullable=False)  # user or system
    change_type = Column(String, nullable=False)  # created, updated, deleted, preset_applied

    # Router-compatible fields
    old_config = Column(JSON, nullable=True)  # Previous configuration
    new_config = Column(JSON, nullable=False)  # New configuration
    task_id = Column(String, ForeignKey("tasks.id"), nullable=True)  # Task this change applies to
    impact_metrics = Column(JSON, nullable=True)  # Predicted impact of this change

    # Legacy fields - kept for backward compatibility
    changes = Column(JSON, nullable=True)  # What changed (field -> {old_value, new_value})
    reason = Column(String, nullable=True)  # Reason for change
    config_snapshot = Column(JSON, nullable=True)  # Full config snapshot before change

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)


class HRMPreset(Base):
    """Built-in and custom HRM presets"""
    __tablename__ = "hrm_presets"

    id = Column(String, primary_key=True)  # UUID string for compatibility with router
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # UI metadata (used by frontend)
    icon = Column(String, nullable=True)  # Emoji or icon identifier (e.g., "⚡", "💰")
    color = Column(String, nullable=True)  # Hex color code (e.g., "#FFD700")
    visibility = Column(String, default="private")  # "private", "shared", "public"

    # Preset type
    is_builtin = Column(Boolean, default=False)
    created_by = Column(String, nullable=True)  # user who created custom preset

    # Preset configuration (JSON)
    config = Column(JSON, nullable=False)

    # Usage stats
    usage_count = Column(Integer, default=0)
    total_cost_saved = Column(Float, default=0.0)

    # Detailed usage statistics (calculated from task results)
    avg_quality = Column(Float, nullable=True)  # Average quality score with this preset
    avg_cost = Column(Float, nullable=True)  # Average cost per task
    avg_duration_seconds = Column(Float, nullable=True)  # Average task duration
    last_used_at = Column(DateTime, nullable=True)  # Last time this preset was applied

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class APIKey(Base):
    """Persistent API key storage for various providers"""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Provider info
    provider = Column(String, nullable=False)  # claude, gemini, copilot, etc.
    key_name = Column(String, nullable=False)

    # Encrypted key storage
    encrypted_key = Column(String, nullable=False)

    # Key metadata
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    created_by = Column(String, nullable=False)

    # Rate limits and quotas
    daily_requests = Column(Integer, default=0)
    monthly_requests = Column(Integer, default=0)
    current_usage = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LoadBalancingConfig(Base):
    """Load balancing configuration per provider"""
    __tablename__ = "load_balancing_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Provider identification
    provider = Column(String, nullable=False)  # claude, gemini, copilot, etc.
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)

    # Load balancing strategy
    strategy = Column(String, default="round_robin")  # round_robin, least_busy, cost_optimized

    # Provider weights (JSON: agent_type -> weight)
    provider_weights = Column(JSON, nullable=False)

    # Queue settings
    max_concurrent_tasks = Column(Integer, default=5)
    queue_timeout_seconds = Column(Integer, default=300)

    # Circuit breaker settings
    failure_threshold = Column(Float, default=0.5)  # 50% failure rate
    recovery_timeout_seconds = Column(Integer, default=300)

    # Performance tracking
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    avg_response_time_ms = Column(Float, default=0.0)

    # Status
    is_enabled = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SwarmConfig(Base):
    """Swarm orchestration configurations"""
    __tablename__ = "swarm_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Swarm identification
    name = Column(String, nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)

    # Swarm composition (JSON: list of agent configs)
    agents_config = Column(JSON, nullable=False)

    # Coordination strategy
    coordination_mode = Column(String, default="hierarchical")  # hierarchical, peer, delegator
    leader_agent = Column(SQLEnum(AgentType), nullable=True)

    # Communication settings (JSON)
    communication_config = Column(JSON, nullable=False)

    # Swarm parameters
    swarm_size = Column(Integer, default=3)
    consensus_threshold = Column(Float, default=0.66)  # 66% agreement required
    max_parallel_tasks = Column(Integer, default=5)

    # Performance metrics
    total_swarm_executions = Column(Integer, default=0)
    successful_swarm_executions = Column(Integer, default=0)
    consensus_agreements = Column(Integer, default=0)
    consensus_disagreements = Column(Integer, default=0)

    # Status
    is_active = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SpecKitFeature(Base):
    """Spec-Kit feature tracking and configuration"""
    __tablename__ = "speckit_features"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Feature identification
    feature_name = Column(String, nullable=False, unique=True)
    feature_version = Column(String, default="1.0")

    # Feature description and configuration
    description = Column(String, nullable=True)
    feature_config = Column(JSON, nullable=False)  # Feature-specific settings

    # Integration info
    integration_points = Column(JSON, nullable=False)  # List of components using this feature
    dependencies = Column(JSON, default=list)  # List of dependent features

    # Feature status
    is_enabled = Column(Boolean, default=True)
    is_beta = Column(Boolean, default=False)

    # Performance and usage tracking
    usage_count = Column(Integer, default=0)
    total_executions = Column(Integer, default=0)
    successful_executions = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    avg_execution_time_ms = Column(Float, default=0.0)

    # Optimization metrics
    optimization_potential = Column(Float, default=0.0)  # 0-1 scale

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SystemMetrics(Base):
    """System-wide metrics and monitoring"""
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Metric timestamp (usually collected at regular intervals)
    metric_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # CPU and Memory Metrics
    cpu_usage_percent = Column(Float, default=0.0)
    memory_usage_percent = Column(Float, default=0.0)

    # Agent Performance Metrics
    agents_active = Column(Integer, default=0)
    agents_idle = Column(Integer, default=0)
    agents_busy = Column(Integer, default=0)

    # Task Metrics
    tasks_pending = Column(Integer, default=0)
    tasks_running = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    avg_task_duration_seconds = Column(Float, default=0.0)

    # Cost Metrics
    hourly_cost = Column(Float, default=0.0)
    daily_cost = Column(Float, default=0.0)
    monthly_cost = Column(Float, default=0.0)

    # Quality Metrics
    avg_quality_score = Column(Float, default=0.0)
    test_pass_rate = Column(Float, default=0.0)
    security_score = Column(Float, default=0.0)

    # Network & API Metrics
    api_calls_total = Column(Integer, default=0)
    api_calls_failed = Column(Integer, default=0)
    api_avg_latency_ms = Column(Float, default=0.0)

    # Throughput Metrics
    throughput_tasks_per_hour = Column(Float, default=0.0)
    throughput_tokens_per_second = Column(Float, default=0.0)

    # Resource Utilization
    queue_depth = Column(Integer, default=0)
    cache_hit_rate = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
