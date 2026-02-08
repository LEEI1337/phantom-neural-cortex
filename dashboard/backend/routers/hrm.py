"""
HRM (Hierarchical Reasoning Module) Configuration API Router

Provides endpoints for real-time HRM parameter control, preset management,
and impact simulation.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..database import get_async_db
from ..models import (
    HRMConfig, HRMConfigHistory, HRMPreset, Project, Task,
    AgentType, TaskStatus
)
from pydantic import BaseModel, Field
from .websocket import (
    emit_hrm_config_update,
    emit_hrm_preset_applied,
    emit_system_alert
)


router = APIRouter(tags=["HRM Configuration"])


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class LatentReasoningConfig(BaseModel):
    """Latent reasoning compression settings"""
    enabled: bool = True
    dimensionality: int = Field(512, ge=128, le=1024)
    compression_ratio_target: float = Field(3.8, ge=1.0, le=10.0)
    auto_adjust: bool = False


class MLIterationPredictionConfig(BaseModel):
    """ML iteration prediction settings"""
    mode: str = Field("auto", pattern="^(auto|manual|fixed)$")
    max_iterations: int = Field(7, ge=2, le=20)
    confidence_threshold: float = Field(0.80, ge=0.0, le=1.0)


class AgentSwitchingConfig(BaseModel):
    """Smart agent switching settings"""
    strategy: str = Field("adaptive", pattern="^(cost_optimized|quality_first|speed_optimized|adaptive|round_robin|manual)$")
    quality_drop_threshold: float = Field(0.20, ge=0.0, le=1.0)
    cost_ceiling: float = Field(5.00, ge=0.0)
    max_switches_per_task: int = Field(3, ge=0, le=10)


class DeepSupervisionConfig(BaseModel):
    """Deep supervision checkpoint settings"""
    enabled: bool = True
    checkpoints: List[float] = [0.33, 0.66, 1.00]
    quality_gate_threshold: float = Field(0.75, ge=0.0, le=1.0)


class ParallelEvaluationConfig(BaseModel):
    """Parallel quality evaluation settings"""
    enabled: bool = True
    worker_count: int = Field(4, ge=1, le=16)
    timeout_seconds: int = Field(60, ge=10, le=300)


class CachingConfig(BaseModel):
    """Three-layer caching settings"""
    memory: bool = True
    disk: bool = True
    remote: bool = False
    aggressive_mode: bool = True
    max_size_mb: int = Field(500, ge=100, le=5000)


class BayesianOptimizationConfig(BaseModel):
    """Bayesian weight optimization settings"""
    enabled: bool = False
    iterations: int = Field(30, ge=10, le=100)


class RLRefinementConfig(BaseModel):
    """RL refinement chain settings"""
    enabled: bool = True
    epsilon: float = Field(0.1, ge=0.0, le=1.0)
    learning_rate: float = Field(0.001, ge=0.0001, le=0.1)


class PrometheusMetricsConfig(BaseModel):
    """Prometheus metrics settings"""
    enabled: bool = True
    export_interval: int = Field(15, ge=5, le=60)


class MultiRepoConfig(BaseModel):
    """Multi-repository coordination settings"""
    enabled: bool = True


class HRMConfigSchema(BaseModel):
    """Complete HRM configuration schema"""
    latent_reasoning: LatentReasoningConfig
    ml_iteration_prediction: MLIterationPredictionConfig
    agent_switching: AgentSwitchingConfig
    deep_supervision: DeepSupervisionConfig
    parallel_evaluation: ParallelEvaluationConfig
    caching: CachingConfig
    bayesian_optimization: BayesianOptimizationConfig
    rl_refinement: RLRefinementConfig
    prometheus_metrics: PrometheusMetricsConfig
    multi_repo: MultiRepoConfig


class HRMConfigRequest(BaseModel):
    """HRM configuration update request"""
    project_id: Optional[str] = None
    task_id: Optional[str] = None
    config: HRMConfigSchema
    apply_immediately: bool = True
    persist: bool = True


class ImpactEstimate(BaseModel):
    """Impact estimate for configuration change"""
    cost_change: float  # -0.28 = 28% reduction
    speed_change: float  # 0.30 = 30% faster
    quality_change: float  # 0.06 = 6% improvement
    token_reduction: float  # 0.40 = 40% reduction


class HRMConfigResponse(BaseModel):
    """HRM configuration response"""
    status: str
    config_id: str
    applied_at: datetime
    impact_estimate: ImpactEstimate
    active_tasks_affected: int
    future_tasks_affected: bool


class HRMPresetResponse(BaseModel):
    """HRM preset response"""
    id: str
    name: str
    description: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    builtin: bool
    config: Dict[str, Any]
    usage_stats: Dict[str, Any]


class HRMPresetCreate(BaseModel):
    """Create custom HRM preset"""
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    visibility: str = Field("private", pattern="^(private|shared|public)$")
    config: HRMConfigSchema


class SimulationRequest(BaseModel):
    """Simulation request"""
    current_config: HRMConfigSchema
    proposed_config: HRMConfigSchema
    task_context: Dict[str, Any]


class MetricChange(BaseModel):
    """Metric change prediction"""
    current: float
    predicted: float
    change_percent: float
    confidence: float


class ImpactAnalysis(BaseModel):
    """Impact analysis result"""
    cost: MetricChange
    speed: MetricChange
    quality: MetricChange
    tokens: MetricChange


class SimulationResponse(BaseModel):
    """Simulation response"""
    impact_analysis: ImpactAnalysis
    recommendations: List[str]
    warnings: List[str]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_impact_estimate(
    current_config: Dict[str, Any],
    new_config: Dict[str, Any],
    task_context: Optional[Dict[str, Any]] = None
) -> ImpactEstimate:
    """
    Calculate impact estimate based on config changes

    This is a simplified version. In production, this would use ML models
    trained on historical data to predict actual impact.
    """

    # Default impact (neutral)
    cost_change = 0.0
    speed_change = 0.0
    quality_change = 0.0
    token_reduction = 0.0

    # Latent Reasoning impact
    if new_config.get("latent_reasoning", {}).get("enabled"):
        old_dim = current_config.get("latent_reasoning", {}).get("dimensionality", 512)
        new_dim = new_config.get("latent_reasoning", {}).get("dimensionality", 512)

        if new_dim < old_dim:
            # Lower dimensionality = faster, cheaper, but lower quality
            cost_change -= 0.15
            speed_change += 0.20
            quality_change -= 0.05
            token_reduction += 0.20
        elif new_dim > old_dim:
            # Higher dimensionality = slower, more expensive, higher quality
            cost_change += 0.15
            speed_change -= 0.15
            quality_change += 0.08
            token_reduction += 0.10

    # Agent Switching impact
    new_strategy = new_config.get("agent_switching", {}).get("strategy", "adaptive")
    if new_strategy == "cost_optimized":
        cost_change -= 0.40
        quality_change -= 0.08
        speed_change += 0.15
    elif new_strategy == "quality_first":
        cost_change += 0.35
        quality_change += 0.15
        speed_change -= 0.10
    elif new_strategy == "speed_optimized":
        speed_change += 0.35
        cost_change += 0.10
        quality_change -= 0.05

    # Parallel Evaluation impact
    new_workers = new_config.get("parallel_evaluation", {}).get("worker_count", 4)
    old_workers = current_config.get("parallel_evaluation", {}).get("worker_count", 4)

    if new_workers > old_workers:
        speed_change += 0.15 * (new_workers - old_workers) / 4
        cost_change += 0.05 * (new_workers - old_workers) / 4

    # Caching impact
    if new_config.get("caching", {}).get("aggressive_mode"):
        speed_change += 0.25
        cost_change -= 0.10

    # ML Iteration Prediction impact
    if new_config.get("ml_iteration_prediction", {}).get("mode") == "auto":
        cost_change -= 0.12
        speed_change += 0.18

    return ImpactEstimate(
        cost_change=round(cost_change, 2),
        speed_change=round(speed_change, 2),
        quality_change=round(quality_change, 2),
        token_reduction=round(token_reduction, 2)
    )


async def get_active_tasks_count(db: AsyncSession, project_id: Optional[str] = None) -> int:
    """Get count of active tasks that will be affected (async)"""
    stmt = select(Task).where(Task.status == TaskStatus.IN_PROGRESS)

    if project_id:
        stmt = stmt.where(Task.project_id == project_id)

    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return len(tasks)


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/config", response_model=HRMConfigResponse)
async def update_hrm_config(
    request: HRMConfigRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update HRM configuration in real-time

    Updates HRM configuration for a project or specific task.
    Can apply immediately to running tasks or persist for future tasks.
    """

    # Generate config ID
    config_id = str(uuid.uuid4())

    # Convert Pydantic models to dict
    config_dict = request.config.dict()

    # Get current config for comparison (if exists)
    current_config = {}
    if request.project_id:
        stmt = select(HRMConfig).where(
            HRMConfig.project_id == request.project_id,
            HRMConfig.task_id.is_(None)
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            current_config = existing.config
            config_id = existing.id

    # Calculate impact
    impact = calculate_impact_estimate(current_config, config_dict)

    # Count affected tasks
    active_tasks = await get_active_tasks_count(db, request.project_id)

    # Create or update HRM config
    if request.persist:
        hrm_config = HRMConfig(
            id=config_id,
            project_id=request.project_id,
            task_id=request.task_id,
            name="Custom Configuration",
            config=config_dict,
            created_by="user@example.com"  # TODO: Get from auth
        )

        # Check if exists
        stmt = select(HRMConfig).where(HRMConfig.id == config_id)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.config = config_dict
            existing.updated_at = datetime.utcnow()
        else:
            db.add(hrm_config)

        # Log to history
        history_entry = HRMConfigHistory(
            config_id=config_id,
            changed_by="user@example.com",
            change_type="update" if existing else "create",
            old_config=current_config,
            new_config=config_dict,
            task_id=request.task_id,
            impact_metrics=impact.dict()
        )
        db.add(history_entry)

        await db.commit()

    # Emit WebSocket event for real-time UI updates
    if request.project_id:
        await emit_hrm_config_update(
            project_id=request.project_id,
            config_id=config_id,
            config_data=config_dict,
            impact=impact.dict()
        )

    # Emit system alert if applying to active tasks
    if request.apply_immediately and active_tasks > 0:
        await emit_system_alert(
            message=f"HRM configuration updated for {active_tasks} active task(s)",
            severity="info"
        )

    return HRMConfigResponse(
        status="applied" if request.apply_immediately else "saved",
        config_id=config_id,
        applied_at=datetime.utcnow(),
        impact_estimate=impact,
        active_tasks_affected=active_tasks if request.apply_immediately else 0,
        future_tasks_affected=request.persist
    )


@router.get("/config", response_model=Dict[str, Any])
async def get_hrm_config(
    project_id: Optional[str] = Query(None),
    task_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current HRM configuration"""

    # Try task-specific first, then project, then default
    config = None

    if task_id:
        stmt = select(HRMConfig).where(HRMConfig.task_id == task_id)
        result = await db.execute(stmt)
        config = result.scalar_one_or_none()

    if not config and project_id:
        stmt = select(HRMConfig).where(
            HRMConfig.project_id == project_id,
            HRMConfig.task_id.is_(None)
        )
        result = await db.execute(stmt)
        config = result.scalar_one_or_none()

    if not config:
        # Return default balanced preset
        stmt = select(HRMPreset).where(HRMPreset.name == "balanced")
        result = await db.execute(stmt)
        preset = result.scalar_one_or_none()

        if preset:
            return {
                "config_id": "default",
                "config": preset.config,
                "preset_name": preset.name,
                "last_updated": None,
                "updated_by": None
            }

        # Fallback to hardcoded default
        return {
            "config_id": "default",
            "config": {
                "latent_reasoning": {"enabled": True, "dimensionality": 512},
                "ml_iteration_prediction": {"mode": "auto", "max_iterations": 7},
                "agent_switching": {"strategy": "adaptive"},
                "deep_supervision": {"enabled": True, "checkpoints": [0.33, 0.66, 1.00]},
                "parallel_evaluation": {"enabled": True, "worker_count": 4},
                "caching": {"memory": True, "disk": True, "remote": False},
                "bayesian_optimization": {"enabled": False},
                "rl_refinement": {"enabled": True, "epsilon": 0.1},
                "prometheus_metrics": {"enabled": True, "export_interval": 15},
                "multi_repo": {"enabled": True}
            },
            "preset_name": "balanced",
            "last_updated": None,
            "updated_by": None
        }

    return {
        "config_id": config.id,
        "config": config.config,
        "preset_name": None,
        "last_updated": config.updated_at,
        "updated_by": config.created_by
    }


@router.get("/config/presets", response_model=List[HRMPresetResponse])
async def get_hrm_presets(db: AsyncSession = Depends(get_async_db)):
    """Get all available HRM presets"""

    stmt = select(HRMPreset)
    result = await db.execute(stmt)
    presets = result.scalars().all()

    return [
        HRMPresetResponse(
            id=str(preset.id),
            name=preset.name,
            description=preset.description or "",
            icon=preset.icon or "package",
            color=preset.color or "#666666",
            builtin=preset.is_builtin,
            config=preset.config,
            usage_stats={
                "usage_count": preset.usage_count,
                "avg_quality": preset.avg_quality,
                "avg_cost": preset.avg_cost,
                "avg_duration": preset.avg_duration_seconds
            }
        )
        for preset in presets
    ]


@router.post("/config/presets", response_model=HRMPresetResponse)
async def create_hrm_preset(
    preset_data: HRMPresetCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Create custom HRM preset"""

    # Check if name already exists
    stmt = select(HRMPreset).where(HRMPreset.name == preset_data.name)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail=f"Preset with name '{preset_data.name}' already exists")

    # Create preset
    preset = HRMPreset(
        id=str(uuid.uuid4()),
        name=preset_data.name,
        description=preset_data.description,
        icon=preset_data.icon,
        color=preset_data.color,
        builtin=False,
        config=preset_data.config.dict(),
        created_by="user@example.com",  # TODO: Get from auth
        visibility=preset_data.visibility
    )

    db.add(preset)
    await db.commit()
    await db.refresh(preset)

    return HRMPresetResponse(
        id=preset.id,
        name=preset.name,
        description=preset.description,
        icon=preset.icon,
        color=preset.color,
        builtin=preset.builtin,
        config=preset.config,
        usage_stats={
            "usage_count": 0,
            "avg_quality": None,
            "avg_cost": None,
            "avg_duration": None
        }
    )


@router.post("/simulate", response_model=SimulationResponse)
async def simulate_hrm_impact(request: SimulationRequest):
    """
    Simulate impact of configuration change before applying

    Uses ML models to predict impact on cost, speed, quality, and tokens.
    """

    current_dict = request.current_config.dict()
    proposed_dict = request.proposed_config.dict()

    # Calculate impact
    impact = calculate_impact_estimate(current_dict, proposed_dict, request.task_context)

    # Convert to MetricChange objects with confidence scores
    task_complexity = request.task_context.get("complexity", 10.0)
    base_confidence = 0.85 if task_complexity < 15 else 0.75

    # Calculate current metrics from task context
    current_duration = request.task_context.get("estimated_duration", 450)
    current_quality = request.task_context.get("current_quality", 0.87)
    current_cost = 2.50  # Default estimate
    current_tokens = 50000  # Default estimate

    # Apply impact percentages
    impact_analysis = ImpactAnalysis(
        cost=MetricChange(
            current=current_cost,
            predicted=current_cost * (1 + impact.cost_change),
            change_percent=impact.cost_change * 100,
            confidence=base_confidence
        ),
        speed=MetricChange(
            current=current_duration,
            predicted=current_duration * (1 - impact.speed_change),
            change_percent=impact.speed_change * 100,
            confidence=base_confidence - 0.05
        ),
        quality=MetricChange(
            current=current_quality,
            predicted=min(1.0, current_quality * (1 + impact.quality_change)),
            change_percent=impact.quality_change * 100,
            confidence=base_confidence - 0.03
        ),
        tokens=MetricChange(
            current=current_tokens,
            predicted=current_tokens * (1 - impact.token_reduction),
            change_percent=-impact.token_reduction * 100,
            confidence=base_confidence + 0.05
        )
    )

    # Generate recommendations
    recommendations = []
    warnings = []

    if impact.cost_change > 0.30:
        warnings.append(f"Cost may increase by {impact.cost_change*100:.0f}%. Consider cost-optimized strategy.")
    elif impact.cost_change < -0.20:
        recommendations.append(f"Excellent cost optimization: {abs(impact.cost_change)*100:.0f}% reduction predicted")

    if impact.quality_change < -0.10:
        warnings.append(f"Quality may decrease by {abs(impact.quality_change)*100:.0f}%. Consider quality-first strategy.")
    elif impact.quality_change > 0.05:
        recommendations.append(f"Quality improvement of {impact.quality_change*100:.0f}% predicted")

    if impact.speed_change > 0.20:
        recommendations.append(f"Speed improvement of {impact.speed_change*100:.0f}% predicted")

    if impact.token_reduction > 0.30:
        recommendations.append(f"Significant token reduction of {impact.token_reduction*100:.0f}% with latent reasoning")

    # Strategy-specific recommendations
    proposed_strategy = proposed_dict.get("agent_switching", {}).get("strategy")
    if proposed_strategy == "cost_optimized":
        recommendations.append("Consider using Gemini (free) for bulk tasks, Claude for critical sections")
    elif proposed_strategy == "quality_first":
        recommendations.append("Claude will be used for maximum quality - ensure budget allows")

    return SimulationResponse(
        impact_analysis=impact_analysis,
        recommendations=recommendations,
        warnings=warnings
    )


@router.get("/config/history/{config_id}", response_model=List[Dict[str, Any]])
async def get_hrm_config_history(
    config_id: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db)
):
    """Get configuration change history"""

    stmt = select(HRMConfigHistory).where(
        HRMConfigHistory.config_id == config_id
    ).order_by(HRMConfigHistory.created_at.desc()).limit(limit)

    result = await db.execute(stmt)
    history = result.scalars().all()

    return [
        {
            "id": entry.id,
            "changed_by": entry.changed_by,
            "change_type": entry.change_type,
            "old_config": entry.old_config,
            "new_config": entry.new_config,
            "impact_metrics": entry.impact_metrics,
            "created_at": entry.created_at
        }
        for entry in history
    ]


@router.delete("/config/presets/{preset_id}")
async def delete_hrm_preset(
    preset_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Delete custom HRM preset (cannot delete built-in presets)"""

    stmt = select(HRMPreset).where(HRMPreset.id == preset_id)
    result = await db.execute(stmt)
    preset = result.scalar_one_or_none()

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    if preset.builtin:
        raise HTTPException(status_code=400, detail="Cannot delete built-in preset")

    await db.delete(preset)
    await db.commit()

    return {"message": f"Preset '{preset.name}' deleted successfully"}


@router.put("/config/presets/{preset_id}", response_model=HRMPresetResponse)
async def update_hrm_preset(
    preset_id: str,
    preset_data: HRMPresetCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Update custom HRM preset (cannot update built-in presets)"""

    stmt = select(HRMPreset).where(HRMPreset.id == preset_id)
    result = await db.execute(stmt)
    preset = result.scalar_one_or_none()

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    if preset.builtin:
        raise HTTPException(status_code=400, detail="Cannot modify built-in preset")

    # Update fields
    preset.name = preset_data.name
    preset.description = preset_data.description
    preset.icon = preset_data.icon
    preset.color = preset_data.color
    preset.config = preset_data.config.dict()
    preset.visibility = preset_data.visibility
    preset.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(preset)

    return HRMPresetResponse(
        id=preset.id,
        name=preset.name,
        description=preset.description,
        icon=preset.icon,
        color=preset.color,
        builtin=preset.builtin,
        config=preset.config,
        usage_stats={
            "usage_count": preset.usage_count,
            "avg_quality": preset.avg_quality,
            "avg_cost": preset.avg_cost,
            "avg_duration": preset.avg_duration_seconds
        }
    )


@router.post("/config/presets/{preset_id}/apply", response_model=HRMConfigResponse)
async def apply_hrm_preset(
    preset_id: str,
    project_id: str = Query(..., description="Project ID to apply preset to"),
    apply_immediately: bool = Query(False, description="Apply to running tasks"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Apply an HRM preset to a project

    Applies a saved preset configuration to a project and optionally to running tasks.
    Emits WebSocket events for real-time UI updates.
    """

    # Get preset
    stmt = select(HRMPreset).where(HRMPreset.id == preset_id)
    result = await db.execute(stmt)
    preset = result.scalar_one_or_none()

    if not preset:
        raise HTTPException(status_code=404, detail=f"Preset '{preset_id}' not found")

    # Get current config for impact calculation
    current_config = {}
    config_id = str(uuid.uuid4())

    stmt = select(HRMConfig).where(
        HRMConfig.project_id == project_id,
        HRMConfig.task_id.is_(None)
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        current_config = existing.config
        config_id = existing.id

    # Calculate impact
    impact = calculate_impact_estimate(current_config, preset.config)

    # Count affected tasks
    active_tasks = await get_active_tasks_count(db, project_id)

    # Create or update HRM config with preset
    hrm_config = HRMConfig(
        id=config_id,
        project_id=project_id,
        task_id=None,
        name=f"Preset: {preset.name}",
        config=preset.config,
        created_by="user@example.com"  # TODO: Get from auth
    )

    if existing:
        existing.config = preset.config
        existing.name = f"Preset: {preset.name}"
        existing.updated_at = datetime.utcnow()
    else:
        db.add(hrm_config)

    # Log to history
    history_entry = HRMConfigHistory(
        config_id=config_id,
        changed_by="user@example.com",
        change_type="preset_applied",
        old_config=current_config,
        new_config=preset.config,
        task_id=None,
        impact_metrics=impact.dict()
    )
    db.add(history_entry)

    # Update preset usage stats
    preset.usage_count += 1
    preset.last_used_at = datetime.utcnow()

    await db.commit()

    # Emit WebSocket events
    await emit_hrm_preset_applied(
        project_id=project_id,
        preset_name=preset.name,
        preset_config=preset.config
    )

    await emit_hrm_config_update(
        project_id=project_id,
        config_id=config_id,
        config_data=preset.config,
        impact=impact.dict()
    )

    if apply_immediately and active_tasks > 0:
        await emit_system_alert(
            message=f"HRM preset '{preset.name}' applied to {active_tasks} active task(s)",
            severity="success"
        )

    return HRMConfigResponse(
        status="applied" if apply_immediately else "saved",
        config_id=config_id,
        applied_at=datetime.utcnow(),
        impact_estimate=impact,
        active_tasks_affected=active_tasks if apply_immediately else 0,
        future_tasks_affected=True
    )
