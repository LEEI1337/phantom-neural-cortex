"""
Tasks API Router
Task management and monitoring
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from ..database import get_db
from ..models import Task, TaskStatus

router = APIRouter()

class TaskResponse(BaseModel):
    id: str
    project_id: str
    issue_number: int
    title: str
    description: str | None
    labels: List[str]
    status: TaskStatus
    assigned_agent: str
    agent_switches: int
    current_iteration: int
    max_iterations: int
    current_quality: float
    final_quality: float | None
    tests_passing: bool
    security_issues: int
    started_at: str | None
    completed_at: str | None
    duration_seconds: float | None
    estimated_cost: float
    actual_cost: float | None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class PaginatedTasksResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# GET tasks with pagination and filters
@router.get("/", response_model=PaginatedTasksResponse)
async def get_tasks(
    project_id: Optional[str] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)

    total = query.count()
    total_pages = (total + page_size - 1) // page_size

    tasks = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedTasksResponse(
        items=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

# GET single task
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)

# RETRY task
@router.post("/{task_id}/retry", response_model=TaskResponse)
async def retry_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Reset task for retry
    task.status = TaskStatus.PENDING
    task.current_iteration = 0
    task.current_quality = 0.0
    task.started_at = None
    task.completed_at = None

    db.commit()
    db.refresh(task)

    return TaskResponse.model_validate(task)

# CANCEL task
@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == TaskStatus.IN_PROGRESS:
        task.status = TaskStatus.FAILED
        db.commit()

    return {"message": "Task cancelled"}
