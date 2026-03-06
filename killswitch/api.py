"""Killswitch REST API + Mattermost Webhook endpoints."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from .handler import KillReason, KillswitchHandler

logger = logging.getLogger(__name__)

killswitch_router = APIRouter(prefix="/killswitch", tags=["killswitch"])

# Global registry of killswitch handlers per agent
_handlers: dict[str, KillswitchHandler] = {}


def register_handler(agent_name: str, handler: KillswitchHandler):
    """Register a killswitch handler for an agent."""
    _handlers[agent_name] = handler


class KillRequest(BaseModel):
    triggered_by: str
    details: str = ""


class MMWebhookPayload(BaseModel):
    """Mattermost slash command webhook payload."""
    text: str = ""
    user_name: str = ""
    channel_name: str = ""


@killswitch_router.post("/agent/{agent_name}/kill")
async def kill_agent(agent_name: str, req: KillRequest):
    """REST endpoint to kill an agent."""
    handler = _handlers.get(agent_name)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")

    try:
        event = await handler.kill(
            reason=KillReason.API,
            triggered_by=req.triggered_by,
            details=req.details,
        )
        return {"status": "killed", "event": event.model_dump()}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@killswitch_router.post("/agent/{agent_name}/revive")
async def revive_agent(agent_name: str, req: KillRequest):
    """REST endpoint to revive a killed agent."""
    handler = _handlers.get(agent_name)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")

    try:
        await handler.revive(authorized_by=req.triggered_by)
        return {"status": "revived", "agent": agent_name}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@killswitch_router.get("/agent/{agent_name}/status")
async def agent_kill_status(agent_name: str):
    """Check if an agent is killed or alive."""
    handler = _handlers.get(agent_name)
    if not handler:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")

    return {
        "agent": agent_name,
        "killed": handler.is_killed,
        "active_tasks": len(handler._active_tasks),
    }


@killswitch_router.post("/webhook/killswitch")
async def mm_killswitch_webhook(payload: MMWebhookPayload):
    """Mattermost /killswitch slash command webhook.

    Usage in MM: /killswitch lisa01
    """
    agent_name = payload.text.strip()
    if not agent_name:
        return {
            "response_type": "ephemeral",
            "text": "Usage: `/killswitch <agent_name>`\nAvailable agents: " + ", ".join(_handlers.keys()),
        }

    handler = _handlers.get(agent_name)
    if not handler:
        return {
            "response_type": "ephemeral",
            "text": f"Agent `{agent_name}` not found. Available: {', '.join(_handlers.keys())}",
        }

    try:
        event = await handler.kill(
            reason=KillReason.MATTERMOST,
            triggered_by=payload.user_name,
            details=f"via /killswitch in #{payload.channel_name}",
        )
        return {
            "response_type": "in_channel",
            "text": f"**KILLSWITCH ACTIVATED** for `{agent_name}` by @{payload.user_name}\nHash: `{event.hash[:16]}...`",
        }
    except PermissionError:
        return {
            "response_type": "ephemeral",
            "text": f"You are not authorized to kill `{agent_name}`. Authorized users: {handler.authorized_users}",
        }


@killswitch_router.get("/agents")
async def list_agents():
    """List all registered agents and their kill status."""
    return {
        "agents": {
            name: {
                "killed": h.is_killed,
                "active_tasks": len(h._active_tasks),
                "authorized_users": h.authorized_users,
            }
            for name, h in _handlers.items()
        }
    }
