"""
Config API Router
System configuration and defaults
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ProjectConfiguration(BaseModel):
    priority: dict
    timeframe: dict
    risk_tolerance: dict
    deployment: dict
    ml_components: dict

# GET default configuration
@router.get("/default", response_model=ProjectConfiguration)
async def get_default_config():
    return ProjectConfiguration(
        priority={
            "mode": "balanced",
            "custom_weights": None
        },
        timeframe={
            "max_minutes": 30,
            "preset": "standard"
        },
        risk_tolerance={
            "level": 50,
            "allow_experimental": False,
            "ml_features_enabled": True
        },
        deployment={
            "targets": ["windows"],
            "docker_enabled": False,
            "kubernetes_enabled": False
        },
        ml_components={
            "adaptive_iterations": True,
            "quality_weight_learning": True,
            "latent_reasoning": True,
            "agent_switching": True,
            "inference_time_scaling": True
        }
    )

# VALIDATE configuration
@router.post("/validate")
async def validate_config(config: ProjectConfiguration):
    errors = []

    # Validate timeframe
    if config.timeframe["max_minutes"] < 5 or config.timeframe["max_minutes"] > 180:
        errors.append("Timeframe must be between 5 and 180 minutes")

    # Validate risk tolerance
    if config.risk_tolerance["level"] < 0 or config.risk_tolerance["level"] > 100:
        errors.append("Risk tolerance level must be between 0 and 100")

    # Validate deployment targets
    valid_targets = {"windows", "linux", "macos", "kubernetes", "cross-platform"}
    for target in config.deployment["targets"]:
        if target not in valid_targets:
            errors.append(f"Invalid deployment target: {target}")

    return {
        "valid": len(errors) == 0,
        "errors": errors if errors else None
    }
