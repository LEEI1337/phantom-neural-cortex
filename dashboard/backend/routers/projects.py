"""
Projects API Router
CRUD operations for projects
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import uuid

from ..database import get_db
from ..models import Project, ProjectType, ProjectStatus

router = APIRouter()

# Pydantic schemas
class ProjectConfigPriority(BaseModel):
    mode: str
    custom_weights: dict | None = None

class ProjectConfigTimeframe(BaseModel):
    max_minutes: int
    preset: str

class ProjectConfigRiskTolerance(BaseModel):
    level: int
    allow_experimental: bool
    ml_features_enabled: bool

class ProjectConfigDeployment(BaseModel):
    targets: List[str]
    docker_enabled: bool
    kubernetes_enabled: bool

class ProjectConfigMLComponents(BaseModel):
    adaptive_iterations: bool
    quality_weight_learning: bool
    latent_reasoning: bool
    agent_switching: bool
    inference_time_scaling: bool

class ProjectConfiguration(BaseModel):
    priority: ProjectConfigPriority
    timeframe: ProjectConfigTimeframe
    risk_tolerance: ProjectConfigRiskTolerance
    deployment: ProjectConfigDeployment
    ml_components: ProjectConfigMLComponents

class ProjectCreate(BaseModel):
    name: str
    type: ProjectType
    github_repo: str | None = None
    config: ProjectConfiguration | None = None

class ProjectUpdate(BaseModel):
    name: str | None = None
    status: ProjectStatus | None = None
    github_repo: str | None = None
    config: ProjectConfiguration | None = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    type: ProjectType
    status: ProjectStatus
    github_repo: str | None
    slot: str
    config: dict
    total_tasks: int
    successful_tasks: int
    avg_quality: float
    total_cost: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# GET all projects
@router.get("/", response_model=List[ProjectResponse])
async def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [ProjectResponse.model_validate(p) for p in projects]

# GET single project
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.model_validate(project)

# CREATE project
@router.post("/", response_model=ProjectResponse)
async def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    # Find available slot
    existing_projects = db.query(Project).all()
    used_slots = {p.slot for p in existing_projects}

    available_slot = None
    for slot in ["Projekt-A", "Projekt-B", "Projekt-C"]:
        if slot not in used_slots:
            available_slot = slot
            break

    if not available_slot:
        raise HTTPException(status_code=400, detail="No available project slots (max 3)")

    # Default configuration
    default_config = {
        "priority": {"mode": "balanced"},
        "timeframe": {"max_minutes": 30, "preset": "standard"},
        "risk_tolerance": {"level": 50, "allow_experimental": False, "ml_features_enabled": True},
        "deployment": {"targets": ["windows"], "docker_enabled": False, "kubernetes_enabled": False},
        "ml_components": {
            "adaptive_iterations": True,
            "quality_weight_learning": True,
            "latent_reasoning": True,
            "agent_switching": True,
            "inference_time_scaling": True
        }
    }

    config = project_data.config.model_dump() if project_data.config else default_config

    project = Project(
        id=str(uuid.uuid4()),
        name=project_data.name,
        type=project_data.type,
        github_repo=project_data.github_repo,
        slot=available_slot,
        config=config,
        status=ProjectStatus.ACTIVE
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return ProjectResponse.model_validate(project)

# UPDATE project
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project_data.name is not None:
        project.name = project_data.name
    if project_data.status is not None:
        project.status = project_data.status
    if project_data.github_repo is not None:
        project.github_repo = project_data.github_repo
    if project_data.config is not None:
        project.config = project_data.config.model_dump()

    db.commit()
    db.refresh(project)

    return ProjectResponse.model_validate(project)

# DELETE project
@router.delete("/{project_id}")
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}

# UPDATE project configuration
@router.put("/{project_id}/config", response_model=ProjectResponse)
async def update_project_config(
    project_id: str,
    config: ProjectConfiguration,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.config = config.model_dump()
    db.commit()
    db.refresh(project)

    return ProjectResponse.model_validate(project)
