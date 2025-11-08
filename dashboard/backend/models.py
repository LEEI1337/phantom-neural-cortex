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
    GEMINI = "gemini"
    CLAUDE = "claude"
    COPILOT = "copilot"


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
