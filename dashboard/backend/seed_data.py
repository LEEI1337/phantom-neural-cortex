#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Seeding Script
Seeds initial data including HRM presets, system templates, etc.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, HRMPreset, Project
from datetime import datetime
import json
import uuid


def seed_hrm_presets(db: Session):
    """Seed built-in HRM configuration presets."""

    # Check if presets already exist
    existing = db.query(HRMPreset).filter(HRMPreset.is_builtin == True).count()
    if existing > 0:
        print(f"HRM presets already seeded ({existing} presets found)")
        return

    presets = [
        {
            "id": "preset_speed_optimized",
            "name": "speed_optimized",
            "description": "Maximum speed with acceptable quality trade-offs. Best for rapid prototyping.",
            "icon": "⚡",
            "color": "#FFD700",
            "is_builtin": True,
            "config": {
                "latent_reasoning": {
                    "enabled": True,
                    "dimensionality": 256,  # Lower for speed
                    "compression_ratio": 2.5
                },
                "ml_iteration_prediction": {
                    "enabled": True,
                    "model_type": "fast_estimator",  # Faster model
                    "confidence_threshold": 0.6
                },
                "agent_switching": {
                    "enabled": True,
                    "strategy": "speed_first",
                    "fallback_on_failure": True,
                    "cost_weight": 0.2,
                    "speed_weight": 0.6,  # High speed priority
                    "quality_weight": 0.2
                },
                "deep_supervision": {
                    "enabled": True,
                    "checkpoints": [50, 100],  # Fewer checkpoints
                    "auto_rollback": True
                },
                "parallel_evaluation": {
                    "enabled": True,
                    "num_parallel_agents": 2,  # Lower parallelism
                    "voting_strategy": "simple_majority"
                },
                "caching": {
                    "enabled": True,
                    "memory_cache_size_mb": 128,
                    "disk_cache_size_mb": 512,
                    "remote_cache_enabled": False,  # Skip remote
                    "ttl_seconds": 3600
                },
                "bayesian_optimization": {
                    "enabled": False  # Disable for speed
                },
                "rl_refinement": {
                    "enabled": False  # Disable for speed
                },
                "prometheus_metrics": {
                    "enabled": True,
                    "export_interval_seconds": 30
                },
                "multi_repo": {
                    "enabled": False,
                    "max_repos": 1
                }
            }
        },
        {
            "id": "preset_cost_optimized",
            "name": "cost_optimized",
            "description": "Minimize API costs while maintaining good quality. Best for budget-conscious projects.",
            "icon": "💰",
            "color": "#4CAF50",
            "is_builtin": True,
            "config": {
                "latent_reasoning": {
                    "enabled": True,
                    "dimensionality": 512,
                    "compression_ratio": 4.0  # High compression = cost savings
                },
                "ml_iteration_prediction": {
                    "enabled": True,
                    "model_type": "random_forest",
                    "confidence_threshold": 0.8  # Avoid unnecessary iterations
                },
                "agent_switching": {
                    "enabled": True,
                    "strategy": "cost_optimized",
                    "fallback_on_failure": True,
                    "cost_weight": 0.6,  # High cost priority
                    "speed_weight": 0.2,
                    "quality_weight": 0.2
                },
                "deep_supervision": {
                    "enabled": True,
                    "checkpoints": [33, 66, 100],
                    "auto_rollback": True
                },
                "parallel_evaluation": {
                    "enabled": False  # Disable to save costs
                },
                "caching": {
                    "enabled": True,
                    "memory_cache_size_mb": 256,
                    "disk_cache_size_mb": 2048,
                    "remote_cache_enabled": True,  # Maximize cache hit rate
                    "ttl_seconds": 86400  # 24 hours
                },
                "bayesian_optimization": {
                    "enabled": True,
                    "acquisition_function": "ei",
                    "n_initial_points": 3  # Fewer iterations
                },
                "rl_refinement": {
                    "enabled": False  # Disable to save costs
                },
                "prometheus_metrics": {
                    "enabled": True,
                    "export_interval_seconds": 60
                },
                "multi_repo": {
                    "enabled": False,
                    "max_repos": 2
                }
            }
        },
        {
            "id": "preset_quality_first",
            "name": "quality_first",
            "description": "Maximum quality regardless of cost or time. Best for production-critical code.",
            "icon": "🎯",
            "color": "#9C27B0",
            "is_builtin": True,
            "config": {
                "latent_reasoning": {
                    "enabled": True,
                    "dimensionality": 1024,  # Maximum context
                    "compression_ratio": 2.0
                },
                "ml_iteration_prediction": {
                    "enabled": True,
                    "model_type": "gradient_boosting",
                    "confidence_threshold": 0.9
                },
                "agent_switching": {
                    "enabled": True,
                    "strategy": "quality_first",
                    "fallback_on_failure": True,
                    "cost_weight": 0.1,
                    "speed_weight": 0.1,
                    "quality_weight": 0.8  # High quality priority
                },
                "deep_supervision": {
                    "enabled": True,
                    "checkpoints": [20, 40, 60, 80, 100],  # More checkpoints
                    "auto_rollback": True
                },
                "parallel_evaluation": {
                    "enabled": True,
                    "num_parallel_agents": 5,  # Maximum parallelism
                    "voting_strategy": "weighted_consensus"
                },
                "caching": {
                    "enabled": True,
                    "memory_cache_size_mb": 512,
                    "disk_cache_size_mb": 4096,
                    "remote_cache_enabled": True,
                    "ttl_seconds": 86400
                },
                "bayesian_optimization": {
                    "enabled": True,
                    "acquisition_function": "ucb",
                    "n_initial_points": 10
                },
                "rl_refinement": {
                    "enabled": True,
                    "algorithm": "ppo",
                    "num_refinement_iterations": 5,
                    "learning_rate": 0.0001
                },
                "prometheus_metrics": {
                    "enabled": True,
                    "export_interval_seconds": 15
                },
                "multi_repo": {
                    "enabled": True,
                    "max_repos": 10
                }
            }
        },
        {
            "id": "preset_balanced",
            "name": "balanced",
            "description": "Balanced configuration for general-purpose use. Good for most projects.",
            "icon": "⚖️",
            "color": "#2196F3",
            "is_builtin": True,
            "config": {
                "latent_reasoning": {
                    "enabled": True,
                    "dimensionality": 512,
                    "compression_ratio": 3.0
                },
                "ml_iteration_prediction": {
                    "enabled": True,
                    "model_type": "random_forest",
                    "confidence_threshold": 0.75
                },
                "agent_switching": {
                    "enabled": True,
                    "strategy": "adaptive",
                    "fallback_on_failure": True,
                    "cost_weight": 0.33,
                    "speed_weight": 0.33,
                    "quality_weight": 0.34
                },
                "deep_supervision": {
                    "enabled": True,
                    "checkpoints": [33, 66, 100],
                    "auto_rollback": True
                },
                "parallel_evaluation": {
                    "enabled": True,
                    "num_parallel_agents": 3,
                    "voting_strategy": "weighted_consensus"
                },
                "caching": {
                    "enabled": True,
                    "memory_cache_size_mb": 256,
                    "disk_cache_size_mb": 2048,
                    "remote_cache_enabled": True,
                    "ttl_seconds": 7200
                },
                "bayesian_optimization": {
                    "enabled": True,
                    "acquisition_function": "ei",
                    "n_initial_points": 5
                },
                "rl_refinement": {
                    "enabled": True,
                    "algorithm": "ppo",
                    "num_refinement_iterations": 3,
                    "learning_rate": 0.0003
                },
                "prometheus_metrics": {
                    "enabled": True,
                    "export_interval_seconds": 30
                },
                "multi_repo": {
                    "enabled": True,
                    "max_repos": 5
                }
            }
        }
    ]

    # Insert presets
    for preset_data in presets:
        preset = HRMPreset(
            id=preset_data["id"],
            name=preset_data["name"],
            description=preset_data["description"],
            icon=preset_data["icon"],
            color=preset_data["color"],
            visibility="public",  # Built-in presets are public
            is_builtin=preset_data["is_builtin"],
            config=preset_data["config"],
            created_at=datetime.utcnow()
        )
        db.add(preset)

    db.commit()
    print(f"Seeded {len(presets)} HRM presets")


def seed_demo_projects(db: Session):
    """Seed demo projects for testing."""

    # Check if projects already exist
    existing = db.query(Project).count()
    if existing > 0:
        print(f"Demo projects already seeded ({existing} projects found)")
        return

    demo_projects = [
        {
            "name": "AI Code Assistant",
            "type": "python",
            "slot": "Projekt-A",
            "github_repo": "https://github.com/phantom-cortex/ai-code-assistant",
            "config": {
                "agent": "claude",
                "model": "claude-sonnet-4",
                "temperature": 0.7,
                "max_tokens": 4096,
                "quality_gate": 0.8
            }
        },
        {
            "name": "React Dashboard",
            "type": "react",
            "slot": "Projekt-B",
            "github_repo": "https://github.com/phantom-cortex/react-dashboard",
            "config": {
                "agent": "claude",
                "model": "claude-sonnet-4",
                "temperature": 0.5,
                "max_tokens": 2048,
                "quality_gate": 0.85
            }
        }
    ]

    for project_data in demo_projects:
        project = Project(
            id=str(uuid.uuid4()),
            name=project_data["name"],
            type=project_data["type"],
            slot=project_data["slot"],
            github_repo=project_data.get("github_repo"),
            config=project_data.get("config", {}),
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(project)

    db.commit()
    print(f"Seeded {len(demo_projects)} demo projects")


def seed_all(db: Session):
    """Seed all initial data."""
    print("Seeding database...")
    seed_hrm_presets(db)
    seed_demo_projects(db)
    print("Database seeding complete!")


def main():
    """Main seeding function."""
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create a database session
    db = SessionLocal()

    try:
        seed_all(db)
    except Exception as e:
        print(f"ERROR: Seeding failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
