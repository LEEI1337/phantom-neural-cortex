"""
Context Management API Router

REST API endpoints for context window management.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging

from context import (
    ContextTracker,
    ContextPruner,
    ContextCompactor,
    ContextInspector,
    ModelType,
    ContextStatus,
    ContextInspection,
    PruneResult,
    CompactResult
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/context", tags=["Context Management"])

# In-memory storage for context trackers (in production, use Redis or database)
_context_trackers: Dict[str, ContextTracker] = {}


async def get_or_create_tracker(
    session_id: str,
    model: ModelType = ModelType.CLAUDE
) -> ContextTracker:
    """
    Get existing tracker or create new one with persistent history.
    """
    if session_id not in _context_trackers:
        tracker = ContextTracker(session_id=session_id, model=model)
        # Load history from Phase 4 persistence
        await tracker.load_history()
        _context_trackers[session_id] = tracker
        logger.info(f"Initialized context tracker for session {session_id} (Persistent)")
    
    return _context_trackers[session_id]


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class StatusRequest(BaseModel):
    """Request model for status endpoint"""
    session_id: str = Field(..., description="Session identifier")
    model: Optional[ModelType] = Field(ModelType.CLAUDE, description="AI model type")


class PruneRequest(BaseModel):
    """Request model for pruning endpoint"""
    session_id: str = Field(..., description="Session identifier")
    target_percent: Optional[float] = Field(70.0, description="Target usage percentage", ge=0, le=100)


class CompactRequest(BaseModel):
    """Request model for compaction endpoint"""
    session_id: str = Field(..., description="Session identifier")


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get(
    "/status",
    response_model=ContextStatus,
    summary="Get context window status",
    description="Get current status of context window including token usage and capacity"
)
async def get_status(
    session_id: str,
    model: ModelType = ModelType.CLAUDE
):
    """
    Get context window status for a session.
    
    Similar to OpenClaw's /status command.
    """
    tracker = await get_or_create_tracker(session_id, model)
    status = tracker.get_status()
    
    logger.info(
        f"Status request for {session_id}: "
        f"{status.total_tokens}/{status.max_tokens} tokens "
        f"({status.usage_percent:.1f}%)"
    )
    
    return status


@router.get(
    "/inspection",
    response_model=ContextInspection,
    summary="Get detailed context inspection",
    description="Get complete context inspection with all items and breakdown"
)
async def get_inspection(
    session_id: str,
    model: ModelType = ModelType.CLAUDE
):
    """
    Get detailed context inspection.
    
    Similar to OpenClaw's /context detail command.
    """
    tracker = await get_or_create_tracker(session_id, model)
    inspector = ContextInspector(tracker)
    
    inspection = inspector.get_inspection_data()
    
    logger.info(f"Inspection request for {session_id}")
    
    return inspection


@router.post(
    "/prune",
    response_model=PruneResult,
    summary="Prune context window",
    description="Remove old or low-importance items to free up space"
)
async def prune_context(request: PruneRequest):
    """
    Prune context to target usage percentage.
    
    Uses smart pruning strategy:
    1. Remove old tool results
    2. Remove old messages
    3. Remove low-importance items
    """
    tracker = await get_or_create_tracker(request.session_id)
    pruner = ContextPruner(tracker)
    
    result = pruner.prune_to_threshold(target_percent=request.target_percent)
    
    # Persist pruned state
    await tracker.persist_state()
    
    logger.info(
        f"Pruned {request.session_id}: "
        f"removed {len(result.pruned_items)} items, "
        f"freed {result.tokens_freed} tokens"
    )
    
    return result


@router.post(
    "/compact",
    response_model=CompactResult,
    summary="Compact context window",
    description="Summarize old messages and compress tool outputs"
)
async def compact_context(request: CompactRequest):
    """
    Compact context using AI-powered summarization.
    
    Similar to OpenClaw's /compact command.
    """
    tracker = await get_or_create_tracker(request.session_id)
    compactor = ContextCompactor(tracker)
    
    result = compactor.compact()
    
    # Persist compacted state
    await tracker.persist_state()
    
    logger.info(
        f"Compacted {request.session_id}: "
        f"saved {result.tokens_saved} tokens "
        f"({result.compression_ratio:.1%} compression)"
    )
    
    return result


@router.delete(
    "/clear",
    summary="Clear context window",
    description="Clear all non-pinned items from context"
)
async def clear_context(session_id: str):
    """
    Clear all non-pinned context items.
    """
    if session_id not in _context_trackers:
        raise HTTPException(status_code=404, detail="Session not found")
    
    tracker = _context_trackers[session_id]
    tracker.clear()
    
    # Clear persistence
    await tracker.persistence.clear_context_items(session_id)
    await tracker.persist_state()
    
    logger.info(f"Cleared context for {session_id}")
    
    return {"message": "Context cleared and persisted", "session_id": session_id}


@router.get(
    "/sessions",
    summary="List active sessions",
    description="Get list of all active context sessions"
)
async def list_sessions():
    """
    List all active context tracking sessions.
    """
    sessions = []
    for session_id, tracker in _context_trackers.items():
        status = tracker.get_status()
        sessions.append({
            "session_id": session_id,
            "model": status.model.value,
            "tokens": status.total_tokens,
            "max_tokens": status.max_tokens,
            "usage_percent": status.usage_percent,
            "item_count": status.item_count
        })
    
    return {"sessions": sessions, "count": len(sessions)}


@router.get(
    "/health",
    summary="Health check",
    description="Check if context management system is operational"
)
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "active_sessions": len(_context_trackers),
        "version": "1.0.0"
    }
