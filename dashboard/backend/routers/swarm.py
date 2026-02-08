"""
Swarm Orchestration Control Panel
Advanced swarm orchestration with multiple control modes and strategies
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from enum import Enum

from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..database import get_async_db
from ..models import SwarmConfig as SwarmConfigModel, AgentType
from ..swarm.orchestrator import SwarmOrchestrator, SwarmTask, SwarmResult
from ..swarm.intelligence import IntelligenceEngine
from ..swarm.impact import ImpactReport

router = APIRouter(tags=["Swarm Orchestration"])

# Global orchestrator instance
orchestrator = SwarmOrchestrator()
class IntelligenceMode(str, Enum):
    """AI intelligence modes"""
    SPEED = "speed"  # Fast responses, lower quality
    BALANCED = "balanced"  # Balance speed and quality
    QUALITY = "quality"  # High quality, slower
    EXPERT = "expert"  # Maximum quality, slowest
    CUSTOM = "custom"  # User-defined parameters

class AgentSwitchingStrategy(str, Enum):
    """How to switch between AI agents"""
    COST_OPTIMIZED = "cost_optimized"  # Minimize cost
    QUALITY_FIRST = "quality_first"  # Maximize quality
    SPEED_FIRST = "speed_first"  # Maximize speed
    ADAPTIVE = "adaptive"  # Learn from results
    ROUND_ROBIN = "round_robin"  # Cycle through agents
    MANUAL = "manual"  # User chooses

class RetryStrategy(str, Enum):
    """Error retry strategies"""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    IMMEDIATE = "immediate"
    ADAPTIVE = "adaptive"
    NO_RETRY = "no_retry"

class CachingStrategy(str, Enum):
    """Caching strategies"""
    AGGRESSIVE = "aggressive"  # Cache everything
    BALANCED = "balanced"  # Cache common requests
    MINIMAL = "minimal"  # Cache only identical requests
    DISABLED = "disabled"  # No caching

# Swarm Configuration Models
class ParallelizationConfig(BaseModel):
    """Parallelization settings"""
    enabled: bool = Field(default=True)
    max_parallel_tasks: int = Field(default=5, ge=1, le=50)
    max_parallel_agents: int = Field(default=3, ge=1, le=10)
    auto_scale: bool = Field(default=True, description="Automatically adjust based on load")
    batch_size: int = Field(default=10, ge=1, le=100, description="Batch size for parallel processing")

class IntelligenceConfig(BaseModel):
    """Intelligence mode settings"""
    mode: IntelligenceMode = Field(default=IntelligenceMode.BALANCED)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, ge=100, le=100000)
    use_latent_reasoning: bool = Field(default=True)
    reasoning_depth: int = Field(default=3, ge=1, le=10)

class FeedbackLoopConfig(BaseModel):
    """Feedback loop and iteration settings"""
    enabled: bool = Field(default=True)
    max_iterations: int = Field(default=5, ge=1, le=20)
    quality_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    adaptive_iterations: bool = Field(default=True, description="ML-optimized iteration count")
    early_stopping: bool = Field(default=True)
    convergence_threshold: float = Field(default=0.05, ge=0.0, le=1.0)

class CostControlConfig(BaseModel):
    """Cost management settings"""
    daily_budget: Optional[float] = Field(default=None, description="Daily budget in USD")
    monthly_budget: Optional[float] = Field(default=None, description="Monthly budget in USD")
    per_task_budget: Optional[float] = Field(default=None, description="Budget per task in USD")
    auto_pause_on_budget: bool = Field(default=True)
    cost_alerting_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Alert at 80% budget")
    prefer_cheaper_models: bool = Field(default=False)

class AgentSwitchingConfig(BaseModel):
    """Agent switching logic"""
    strategy: AgentSwitchingStrategy = Field(default=AgentSwitchingStrategy.ADAPTIVE)
    allow_fallback: bool = Field(default=True)
    primary_agent: Optional[str] = Field(default=None)
    fallback_agents: List[str] = Field(default=[])
    quality_threshold_for_switch: float = Field(default=0.7, ge=0.0, le=1.0)
    latency_threshold_ms: int = Field(default=5000, ge=100, le=60000)

class CachingConfig(BaseModel):
    """Caching configuration"""
    strategy: CachingStrategy = Field(default=CachingStrategy.BALANCED)
    ttl_seconds: int = Field(default=3600, ge=60, le=86400, description="Cache TTL in seconds")
    max_cache_size_mb: int = Field(default=500, ge=10, le=10000)
    semantic_similarity_threshold: float = Field(default=0.95, ge=0.0, le=1.0)
    invalidate_on_code_change: bool = Field(default=True)

class RetryConfig(BaseModel):
    """Retry and error handling"""
    strategy: RetryStrategy = Field(default=RetryStrategy.EXPONENTIAL_BACKOFF)
    max_retries: int = Field(default=3, ge=0, le=10)
    initial_delay_ms: int = Field(default=1000, ge=100, le=10000)
    max_delay_ms: int = Field(default=30000, ge=1000, le=300000)
    retry_on_rate_limit: bool = Field(default=True)
    retry_on_timeout: bool = Field(default=True)
    retry_on_quality_fail: bool = Field(default=True)

class SwarmConfig(BaseModel):
    """Complete swarm orchestration configuration"""
    name: str = Field(..., description="Configuration name")
    description: Optional[str] = None
    parallelization: ParallelizationConfig = Field(default_factory=ParallelizationConfig)
    intelligence: IntelligenceConfig = Field(default_factory=IntelligenceConfig)
    feedback_loop: FeedbackLoopConfig = Field(default_factory=FeedbackLoopConfig)
    cost_control: CostControlConfig = Field(default_factory=CostControlConfig)
    agent_switching: AgentSwitchingConfig = Field(default_factory=AgentSwitchingConfig)
    caching: CachingConfig = Field(default_factory=CachingConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    enabled: bool = Field(default=True)

class SwarmStats(BaseModel):
    """Swarm performance statistics"""
    total_tasks: int
    active_tasks: int
    completed_tasks: int
    failed_tasks: int
    avg_task_duration_seconds: float
    avg_quality_score: float
    total_cost: float
    cache_hit_rate: float
    avg_iterations: float
    agent_distribution: dict

# In-memory storage
swarm_configs = {}
swarm_stats_db = {}

# Predefined configurations
PRESET_CONFIGS = {
    "speed_optimized": SwarmConfig(
        name="Speed Optimized",
        description="Maximize speed with parallel execution and caching",
        parallelization=ParallelizationConfig(
            enabled=True,
            max_parallel_tasks=10,
            max_parallel_agents=5,
            auto_scale=True,
        ),
        intelligence=IntelligenceConfig(
            mode=IntelligenceMode.SPEED,
            temperature=0.5,
            max_tokens=2048,
            use_latent_reasoning=False,
        ),
        feedback_loop=FeedbackLoopConfig(
            enabled=True,
            max_iterations=2,
            adaptive_iterations=False,
        ),
        caching=CachingConfig(
            strategy=CachingStrategy.AGGRESSIVE,
            ttl_seconds=7200,
        ),
    ),
    "cost_optimized": SwarmConfig(
        name="Cost Optimized",
        description="Minimize costs with caching and budget controls",
        intelligence=IntelligenceConfig(
            mode=IntelligenceMode.BALANCED,
            max_tokens=2048,
        ),
        cost_control=CostControlConfig(
            prefer_cheaper_models=True,
            auto_pause_on_budget=True,
        ),
        agent_switching=AgentSwitchingConfig(
            strategy=AgentSwitchingStrategy.COST_OPTIMIZED,
        ),
        caching=CachingConfig(
            strategy=CachingStrategy.AGGRESSIVE,
        ),
    ),
    "quality_first": SwarmConfig(
        name="Quality First",
        description="Maximum quality with expert mode and deep reasoning",
        intelligence=IntelligenceConfig(
            mode=IntelligenceMode.EXPERT,
            temperature=0.8,
            max_tokens=8192,
            use_latent_reasoning=True,
            reasoning_depth=5,
        ),
        feedback_loop=FeedbackLoopConfig(
            enabled=True,
            max_iterations=10,
            quality_threshold=0.95,
            adaptive_iterations=True,
        ),
        agent_switching=AgentSwitchingConfig(
            strategy=AgentSwitchingStrategy.QUALITY_FIRST,
        ),
    ),
}

# Endpoints

@router.get("/configs", response_model=List[SwarmConfig])
async def list_swarm_configs(db: AsyncSession = Depends(get_async_db)):
    """
    List all swarm configurations including presets.
    """
    # 1. Start with presets
    configs = [c.model_dump() if hasattr(c, 'model_dump') else c for c in PRESET_CONFIGS.values()]
    
    # 2. Add from database
    stmt = select(SwarmConfigModel)
    result = await db.execute(stmt)
    db_configs = result.scalars().all()
    
    for db_c in db_configs:
        # Map database model to Pydantic model
        config_data = {
            "name": db_c.name,
            "description": db_c.description,
            "parallelization": db_c.agents_config.get('parallelization', {}),
            "intelligence": db_c.agents_config.get('intelligence', {}),
            "feedback_loop": db_c.agents_config.get('feedback_loop', {}),
            "cost_control": db_c.agents_config.get('cost_control', {}),
            "agent_switching": db_c.agents_config.get('agent_switching', {}),
            "caching": db_c.agents_config.get('caching', {}),
            "retry": db_c.agents_config.get('retry', {}),
            "enabled": db_c.is_active
        }
        configs.append(config_data)
        
    return configs

@router.get("/configs/presets", response_model=List[SwarmConfig])
async def get_preset_configs():
    """
    Get predefined swarm configurations.
    """
    return list(PRESET_CONFIGS.values())

@router.post("/configs", response_model=SwarmConfig, status_code=201)
async def create_swarm_config(config: SwarmConfig, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new swarm configuration (Persistent).
    """
    if config.name in PRESET_CONFIGS:
        raise HTTPException(status_code=400, detail="Configuration name conflicts with a preset")

    # Check if exists in DB
    stmt = select(SwarmConfigModel).filter(SwarmConfigModel.name == config.name)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
         raise HTTPException(status_code=400, detail="Configuration name already exists in database")

    # Save to DB
    # We store the complex Pydantic structure in the agents_config JSON column
    db_config = SwarmConfigModel(
        name=config.name,
        description=config.description,
        project_id="default",  # Default or linked to a project
        agents_config=config.model_dump(),
        is_active=config.enabled,
        coordination_mode="hierarchical"
    )
    
    db.add(db_config)
    await db.commit()
    await db.refresh(db_config)
    
    return config

@router.get("/configs/{config_name}", response_model=SwarmConfig)
async def get_swarm_config(config_name: str, db: AsyncSession = Depends(get_async_db)):
    """
    Get a specific swarm configuration.
    """
    if config_name in PRESET_CONFIGS:
        return PRESET_CONFIGS[config_name]
        
    stmt = select(SwarmConfigModel).filter(SwarmConfigModel.name == config_name)
    result = await db.execute(stmt)
    db_c = result.scalar_one_or_none()
    
    if db_c:
        return SwarmConfig(**db_c.agents_config)
        
    raise HTTPException(status_code=404, detail="Configuration not found")

@router.put("/configs/{config_name}", response_model=SwarmConfig)
async def update_swarm_config(config_name: str, config: SwarmConfig):
    """
    Update an existing swarm configuration.
    """
    if config_name in PRESET_CONFIGS:
        raise HTTPException(status_code=400, detail="Cannot modify preset configurations")
    if config_name not in swarm_configs:
        raise HTTPException(status_code=404, detail="Configuration not found")

    swarm_configs[config_name] = config
    return config

@router.delete("/configs/{config_name}", status_code=204)
async def delete_swarm_config(config_name: str, db: AsyncSession = Depends(get_async_db)):
    """
    Delete a swarm configuration.
    """
    if config_name in PRESET_CONFIGS:
        raise HTTPException(status_code=400, detail="Cannot delete preset configurations")
        
    stmt = delete(SwarmConfigModel).filter(SwarmConfigModel.name == config_name)
    result = await db.execute(stmt)
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Configuration not found")
        
    await db.commit()
    return None

@router.post("/preview", response_model=ImpactReport)
async def preview_swarm_impact(request: Dict[str, str]):
    """
    Get a preview of how swarm would handle a task (Phase 5 Impact Mode).
    """
    description = request.get("description")
    if not description:
        raise HTTPException(status_code=400, detail="Task description is required")
    
    return await orchestrator.get_impact_report(description)


@router.post("/execute-smart", response_model=SwarmResult)
async def execute_smart_swarm(task: SwarmTask):
    """
    Execute a task using Advanced Swarm Intelligent Routing (Phase 5).
    """
    try:
        return await orchestrator.execute_task(task)
    except Exception as e:
        logger.error(f"Error in smart swarm execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=SwarmStats)
async def get_swarm_stats():
    """
    Get current swarm performance statistics.
    """
    # Mock data - would be calculated from real swarm execution
    return SwarmStats(
        total_tasks=150,
        active_tasks=5,
        completed_tasks=142,
        failed_tasks=3,
        avg_task_duration_seconds=45.2,
        avg_quality_score=0.89,
        total_cost=12.45,
        cache_hit_rate=0.68,
        avg_iterations=3.2,
        agent_distribution={
            "claude": 0.45,
            "gemini": 0.35,
            "copilot": 0.20,
        },
    )

@router.post("/optimize")
async def optimize_config(request: Dict[str, Any]):
    """
    Get optimization recommendations using IntelligenceEngine (Phase 5).
    """
    description = request.get("task_description", "Generic optimization request")
    priority = request.get("priority", "balanced")
    
    recommendation = await orchestrator.intelligence.analyze_and_route(description, priority=priority)
    
    # Generate intelligent recommendations
    recommendations = []
    
    if recommendation.estimated_cost > 0.01:
        recommendations.append({
            "category": "cost",
            "recommendation": f"Switch to {recommendation.selected_agent} for this type of task to reduce costs.",
            "potential_savings": f"{recommendation.confidence * 100:.0f}% confidence in optimization"
        })

    if recommendation.predicted_quality < 0.8:
        recommendations.append({
            "category": "quality",
            "recommendation": "Task complexity is high. Enable 'expert' mode for higher reasoning depth.",
            "potential_improvement": "10-15% quality increase"
        })

    return {
        "recommendations": recommendations,
        "selected_route": recommendation.dict(),
        "confidence": recommendation.confidence,
        "estimated_improvement": {
            "cost_reduction": 0.20,
            "time_reduction": 0.25,
            "quality_improvement": 0.12,
        }
    }
