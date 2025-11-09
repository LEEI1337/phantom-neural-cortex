"""
Swarm Orchestration Control Panel
Advanced swarm orchestration with multiple control modes and strategies
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from enum import Enum

router = APIRouter()

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
async def list_swarm_configs():
    """
    List all swarm configurations including presets.
    """
    configs = list(PRESET_CONFIGS.values())
    configs.extend(swarm_configs.values())
    return configs

@router.get("/configs/presets", response_model=List[SwarmConfig])
async def get_preset_configs():
    """
    Get predefined swarm configurations.
    """
    return list(PRESET_CONFIGS.values())

@router.post("/configs", response_model=SwarmConfig, status_code=201)
async def create_swarm_config(config: SwarmConfig):
    """
    Create a new swarm configuration.
    """
    if config.name in swarm_configs or config.name in PRESET_CONFIGS:
        raise HTTPException(status_code=400, detail="Configuration name already exists")

    swarm_configs[config.name] = config
    return config

@router.get("/configs/{config_name}", response_model=SwarmConfig)
async def get_swarm_config(config_name: str):
    """
    Get a specific swarm configuration.
    """
    if config_name in PRESET_CONFIGS:
        return PRESET_CONFIGS[config_name]
    if config_name in swarm_configs:
        return swarm_configs[config_name]
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
async def delete_swarm_config(config_name: str):
    """
    Delete a swarm configuration.
    """
    if config_name in PRESET_CONFIGS:
        raise HTTPException(status_code=400, detail="Cannot delete preset configurations")
    if config_name not in swarm_configs:
        raise HTTPException(status_code=404, detail="Configuration not found")

    del swarm_configs[config_name]
    return None

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
async def optimize_config(current_stats: dict):
    """
    Get optimization recommendations based on current performance.
    """
    recommendations = []

    if current_stats.get("cache_hit_rate", 0) < 0.5:
        recommendations.append({
            "category": "caching",
            "recommendation": "Increase cache TTL and use AGGRESSIVE caching strategy",
            "potential_savings": "15-25% cost reduction"
        })

    if current_stats.get("avg_iterations", 0) > 5:
        recommendations.append({
            "category": "feedback_loop",
            "recommendation": "Enable adaptive iterations to reduce unnecessary refinement loops",
            "potential_savings": "20-30% time reduction"
        })

    if current_stats.get("avg_quality_score", 0) < 0.8:
        recommendations.append({
            "category": "intelligence",
            "recommendation": "Switch to QUALITY or EXPERT mode with latent reasoning",
            "potential_improvement": "10-15% quality increase"
        })

    return {
        "recommendations": recommendations,
        "confidence": 0.85,
        "estimated_improvement": {
            "cost_reduction": 0.20,
            "time_reduction": 0.25,
            "quality_improvement": 0.12,
        }
    }
