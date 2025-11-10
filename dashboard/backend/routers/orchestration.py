"""
CLI-First Multi-Agent Orchestration API

FastAPI endpoints for Hub-and-Spoke multi-agent orchestration system.

Features:
- Execute single agent tasks
- Execute parallel agent tasks
- Chain multiple agents (Claude -> Gemini -> Claude)
- Smart agent selection
- Real-time WebSocket progress
- Cost tracking and optimization
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import asyncio
import json
from datetime import datetime

from database import get_async_db
from orchestration.orchestrator import (
    CLIOrchestrator,
    Task,
    TaskType,
    AgentType,
    AgentResponse
)
from routers.redis_manager import redis_manager
from routers.websocket import manager as websocket_manager

router = APIRouter(prefix="/api/orchestration", tags=["Multi-Agent Orchestration"])

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class TaskTypeEnum(str, Enum):
    """Task types for smart agent routing"""
    SECURITY = "security"
    ARCHITECTURE = "architecture"
    BULK_ANALYSIS = "bulk_analysis"
    GITHUB_WORKFLOW = "github_workflow"
    CODE_GENERATION = "code_generation"
    DEBUGGING = "debugging"


class ExecuteTaskRequest(BaseModel):
    """Request model for single task execution"""
    prompt: str = Field(..., description="Task prompt for the agent")
    task_type: Optional[TaskTypeEnum] = Field(
        TaskTypeEnum.CODE_GENERATION,
        description="Type of task for smart agent selection"
    )
    files: Optional[List[str]] = Field(
        default=[],
        description="File patterns to include in context"
    )
    workspace: Optional[str] = Field(
        default=".",
        description="Working directory for task execution"
    )
    requires_security: Optional[bool] = Field(
        default=False,
        description="Force Claude for security-critical tasks"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Review this code for security vulnerabilities",
                "task_type": "security",
                "requires_security": True
            }
        }


class TaskExecutionResponse(BaseModel):
    """Response model for task execution"""
    task_id: str
    agent: str
    content: str
    tokens: int
    cost: float
    duration: float
    session_id: Optional[str] = None
    timestamp: str
    metadata: Dict[str, Any] = {}


# Global orchestrator instance
_orchestrator: Optional[CLIOrchestrator] = None


def get_orchestrator() -> CLIOrchestrator:
    """Get or create global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = CLIOrchestrator(
            redis_manager=redis_manager,
            websocket_manager=websocket_manager
        )
    return _orchestrator


@router.post("/execute", response_model=TaskExecutionResponse)
async def execute_task(
    request: ExecuteTaskRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """Execute a single task with smart agent selection"""
    import uuid

    orchestrator = get_orchestrator()
    task_id = str(uuid.uuid4())

    task = Task(
        id=task_id,
        prompt=request.prompt,
        task_type=TaskType[request.task_type.value.upper()],
        files=request.files or [],
        workspace=request.workspace or ".",
        requires_security=request.requires_security or False
    )

    try:
        response = await orchestrator.execute_task(task)

        return TaskExecutionResponse(
            task_id=task_id,
            agent=response.agent.value,
            content=response.content,
            tokens=response.tokens,
            cost=response.cost,
            duration=response.duration,
            session_id=response.session_id,
            timestamp=response.timestamp.isoformat(),
            metadata=response.metadata
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for orchestration system"""
    orchestrator = get_orchestrator()

    health_status = {
        "status": "healthy",
        "orchestrator": "initialized",
        "timestamp": datetime.utcnow().isoformat()
    }

    return health_status


@router.get("/circuit-breaker-status")
async def get_circuit_breaker_status():
    """Get circuit breaker status for all agents"""
    orchestrator = get_orchestrator()

    status = orchestrator.get_circuit_breaker_status()

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "circuit_breakers": status
    }
