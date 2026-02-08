"""
Spec-Kit API Router
Provides REST endpoints for GitHub Spec-Kit workflow integration
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
import sys

# Add lazy-bird to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'lazy-bird'))

from speckit.speckit_orchestrator import (
    SpecKitOrchestrator,
    SpecKitConfig,
    FeatureSpec,
    SpecKitPhase
)
from ..database import get_db
from ..models import Project


router = APIRouter(prefix="/speckit", tags=["speckit"])


# ============================================================
# Pydantic Models
# ============================================================

class SpecKitProjectCreate(BaseModel):
    """Request model for creating Spec-Kit enabled project."""
    project_id: str
    project_path: str
    ai_agent: str = Field(default="claude", description="Primary AI agent")

    # UltraThink Optimizations
    enable_latent_reasoning: bool = True
    enable_rl_refinement: bool = True
    enable_smart_switching: bool = True
    enable_parallel_eval: bool = True
    enable_ml_iteration_prediction: bool = True


class FeatureCreate(BaseModel):
    """Request model for creating new feature."""
    feature_id: str = Field(..., description="Unique feature identifier")
    name: str = Field(..., description="Feature name")
    description: str = Field(..., description="Feature description")


class ConstitutionCreate(BaseModel):
    """Request model for constitution phase."""
    feature_id: str
    principles: List[str] = Field(..., description="Governing principles")


class SpecificationCreate(BaseModel):
    """Request model for specification phase."""
    feature_id: str
    user_stories: List[Dict] = Field(..., description="User stories")
    requirements: List[str] = Field(..., description="Functional requirements")


class PlanCreate(BaseModel):
    """Request model for plan phase."""
    feature_id: str
    architecture: str = Field(..., description="Architecture description")
    tech_stack: Dict[str, str] = Field(..., description="Technology stack")
    components: List[Dict] = Field(..., description="Component breakdown")


class TasksCreate(BaseModel):
    """Request model for tasks phase."""
    feature_id: str
    tasks: List[Dict] = Field(..., description="Implementation tasks")


class ImplementRequest(BaseModel):
    """Request model for implement phase."""
    feature_id: str
    async_execution: bool = Field(default=False, description="Execute asynchronously")


class FeatureResponse(BaseModel):
    """Response model for feature."""
    feature_id: str
    name: str
    description: str
    current_phase: str
    completed_phases: List[str]
    estimated_iterations: Optional[int]
    optimal_agent: Optional[str]
    complexity_score: Optional[float]
    latent_compression: Optional[Dict]


class PhaseResponse(BaseModel):
    """Response model for phase execution."""
    feature_id: str
    phase: str
    status: str
    details: Dict


# ============================================================
# Global Orchestrator Instance
# ============================================================

_orchestrators: Dict[str, SpecKitOrchestrator] = {}


def get_orchestrator(project_id: str, db: Session = Depends(get_db)) -> SpecKitOrchestrator:
    """Get or create orchestrator for project."""
    if project_id in _orchestrators:
        return _orchestrators[project_id]

    # Load project from database
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

    # Create orchestrator config
    config = SpecKitConfig(
        project_name=project.name,
        project_path=Path.cwd() / "projects" / project_id,
        ai_agent="claude",
        enable_latent_reasoning=True,
        enable_rl_refinement=True,
        enable_smart_switching=True,
        enable_parallel_eval=True,
        enable_ml_iteration_prediction=True
    )

    orchestrator = SpecKitOrchestrator(config)
    _orchestrators[project_id] = orchestrator

    return orchestrator


# ============================================================
# Endpoints
# ============================================================

@router.post("/projects", response_model=Dict)
async def create_speckit_project(
    project_data: SpecKitProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Initialize Spec-Kit for existing project.

    Creates .specify/ directory structure with UltraThink optimizations.
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create orchestrator
    config = SpecKitConfig(
        project_name=project.name,
        project_path=Path(project_data.project_path),
        ai_agent=project_data.ai_agent,
        enable_latent_reasoning=project_data.enable_latent_reasoning,
        enable_rl_refinement=project_data.enable_rl_refinement,
        enable_smart_switching=project_data.enable_smart_switching,
        enable_parallel_eval=project_data.enable_parallel_eval,
        enable_ml_iteration_prediction=project_data.enable_ml_iteration_prediction
    )

    orchestrator = SpecKitOrchestrator(config)
    _orchestrators[project_data.project_id] = orchestrator

    return {
        "project_id": project_data.project_id,
        "speckit_initialized": True,
        "specify_dir": str(config.specify_dir),
        "optimizations": {
            "latent_reasoning": project_data.enable_latent_reasoning,
            "rl_refinement": project_data.enable_rl_refinement,
            "smart_switching": project_data.enable_smart_switching,
            "parallel_eval": project_data.enable_parallel_eval,
            "ml_iteration_prediction": project_data.enable_ml_iteration_prediction
        }
    }


@router.post("/features", response_model=FeatureResponse)
async def create_feature(
    feature_data: FeatureCreate,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """
    Create new feature with UltraThink analysis.

    Returns estimated complexity, optimal agent, and iteration predictions.
    """
    feature = orchestrator.create_feature(
        feature_id=feature_data.feature_id,
        name=feature_data.name,
        description=feature_data.description
    )

    return FeatureResponse(
        feature_id=feature.feature_id,
        name=feature.name,
        description=feature.description,
        current_phase=feature.current_phase.value,
        completed_phases=[p.value for p in feature.completed_phases],
        estimated_iterations=feature.estimated_iterations,
        optimal_agent=feature.optimal_agent,
        complexity_score=feature.complexity_score,
        latent_compression=feature.latent_state
    )


@router.get("/features", response_model=List[FeatureResponse])
async def list_features(
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """List all features for project."""
    features = []
    for feature in orchestrator.features.values():
        features.append(FeatureResponse(
            feature_id=feature.feature_id,
            name=feature.name,
            description=feature.description,
            current_phase=feature.current_phase.value,
            completed_phases=[p.value for p in feature.completed_phases],
            estimated_iterations=feature.estimated_iterations,
            optimal_agent=feature.optimal_agent,
            complexity_score=feature.complexity_score,
            latent_compression=feature.latent_state
        ))
    return features


@router.get("/features/{feature_id}", response_model=FeatureResponse)
async def get_feature(
    feature_id: str,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """Get specific feature details."""
    feature = orchestrator.features.get(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {feature_id} not found")

    return FeatureResponse(
        feature_id=feature.feature_id,
        name=feature.name,
        description=feature.description,
        current_phase=feature.current_phase.value,
        completed_phases=[p.value for p in feature.completed_phases],
        estimated_iterations=feature.estimated_iterations,
        optimal_agent=feature.optimal_agent,
        complexity_score=feature.complexity_score,
        latent_compression=feature.latent_state
    )


@router.post("/phases/constitution", response_model=PhaseResponse)
async def execute_constitution_phase(
    constitution_data: ConstitutionCreate,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """
    Execute Constitution phase.

    Establishes project governing principles.
    """
    result = orchestrator.execute_constitution_phase(
        feature_id=constitution_data.feature_id,
        constitution_principles=constitution_data.principles
    )

    return PhaseResponse(
        feature_id=result['feature_id'],
        phase=result['phase'],
        status=result['status'],
        details={'principles_count': result['principles_count']}
    )


@router.post("/phases/specify", response_model=PhaseResponse)
async def execute_specify_phase(
    spec_data: SpecificationCreate,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """
    Execute Specify phase.

    Defines requirements and user stories with latent reasoning compression.
    """
    result = orchestrator.execute_specify_phase(
        feature_id=spec_data.feature_id,
        user_stories=spec_data.user_stories,
        requirements=spec_data.requirements
    )

    return PhaseResponse(
        feature_id=result['feature_id'],
        phase=result['phase'],
        status=result['status'],
        details={
            'user_stories_count': result['user_stories_count'],
            'requirements_count': result['requirements_count'],
            'latent_compression': result.get('latent_compression')
        }
    )


@router.post("/phases/plan", response_model=PhaseResponse)
async def execute_plan_phase(
    plan_data: PlanCreate,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """
    Execute Plan phase.

    Creates technical architecture with ML-based iteration prediction.
    """
    result = orchestrator.execute_plan_phase(
        feature_id=plan_data.feature_id,
        architecture=plan_data.architecture,
        tech_stack=plan_data.tech_stack,
        components=plan_data.components
    )

    return PhaseResponse(
        feature_id=result['feature_id'],
        phase=result['phase'],
        status=result['status'],
        details={
            'estimated_iterations': result['estimated_iterations'],
            'optimal_agent': result['optimal_agent'],
            'components_count': result['components_count']
        }
    )


@router.post("/phases/tasks", response_model=PhaseResponse)
async def execute_tasks_phase(
    tasks_data: TasksCreate,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """
    Execute Tasks phase.

    Generates task list with RL-based optimization.
    """
    result = orchestrator.execute_tasks_phase(
        feature_id=tasks_data.feature_id,
        tasks=tasks_data.tasks
    )

    return PhaseResponse(
        feature_id=result['feature_id'],
        phase=result['phase'],
        status=result['status'],
        details={
            'tasks_count': result['tasks_count'],
            'parallel_tasks': result['parallel_tasks']
        }
    )


@router.post("/phases/implement", response_model=Dict)
async def execute_implement_phase(
    implement_data: ImplementRequest,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """
    Execute Implement phase.

    Runs all tasks with smart agent switching and parallel evaluation.

    Note: This is a simplified mock implementation.
    In production, this would execute actual code generation tasks.
    """
    # Mock executor callback
    def mock_executor(task: Dict, agent: str) -> Dict:
        return {
            'status': 'completed',
            'time': 30.0,
            'cost': 0.05,
            'agent': agent
        }

    result = orchestrator.execute_implement_phase(
        feature_id=implement_data.feature_id,
        executor_callback=mock_executor
    )

    return {
        'feature_id': implement_data.feature_id,
        'phase': 'implement',
        'status': 'completed',
        'completed_tasks': result['completed_tasks'],
        'failed_tasks': result['failed_tasks'],
        'agent_switches': result['agent_switches'],
        'quality_checkpoints': result['quality_checkpoints'],
        'total_time': result['total_time'],
        'total_cost': result['total_cost']
    }


@router.get("/status/{feature_id}", response_model=Dict)
async def get_feature_status(
    feature_id: str,
    project_id: str,
    orchestrator: SpecKitOrchestrator = Depends(get_orchestrator)
):
    """
    Get complete feature status including all phases and UltraThink metrics.
    """
    feature = orchestrator.features.get(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {feature_id} not found")

    return {
        'feature_id': feature.feature_id,
        'name': feature.name,
        'description': feature.description,
        'current_phase': feature.current_phase.value,
        'completed_phases': [p.value for p in feature.completed_phases],
        'progress_percentage': (len(feature.completed_phases) / 7) * 100,  # 7 total phases
        'ultrathink_metrics': {
            'estimated_iterations': feature.estimated_iterations,
            'optimal_agent': feature.optimal_agent,
            'complexity_score': feature.complexity_score,
            'latent_compression': feature.latent_state
        },
        'has_constitution': feature.constitution is not None,
        'has_specification': feature.specification is not None,
        'has_plan': feature.plan is not None,
        'has_tasks': feature.tasks is not None
    }
