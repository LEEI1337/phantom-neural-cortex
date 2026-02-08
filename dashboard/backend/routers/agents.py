"""
Agent Configuration Management Router
Handles agent connections, config files, skills, MCP servers, etc.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import get_db
import os
import json
from pathlib import Path

router = APIRouter(tags=["Agent Configuration"])


# ========== Models ==========

class AgentConnection(BaseModel):
    """Agent connection configuration"""
    agent_id: str
    agent_name: str
    connection_type: Literal['api', 'local', 'remote']
    endpoint: Optional[str] = None
    port: Optional[int] = None
    api_key_id: Optional[str] = None
    enabled: bool = True


class AgentConnectionUpdate(BaseModel):
    """Update agent connection"""
    agent_name: Optional[str] = None
    endpoint: Optional[str] = None
    port: Optional[int] = None
    api_key_id: Optional[str] = None
    enabled: Optional[bool] = None


class AgentConfigFile(BaseModel):
    """Agent configuration file"""
    file_path: str
    file_type: Literal['skill', 'mcp', 'instruction', 'config']
    content: str
    last_modified: str


class AgentConfigFileUpdate(BaseModel):
    """Update agent config file content"""
    content: str


class AgentConnectionsResponse(BaseModel):
    """Response with all agent connections"""
    connections: List[AgentConnection]


class AgentConfigFilesResponse(BaseModel):
    """Response with all agent config files"""
    files: List[AgentConfigFile]


# ========== Helpers ==========

def get_config_root() -> Path:
    """Get the root directory for config files"""
    # Look for .claude directory
    current = Path.cwd()
    for _ in range(5):  # Search up to 5 levels up
        claude_dir = current / ".claude"
        if claude_dir.exists():
            return current
        current = current.parent
    return Path.cwd()


def get_agent_connections_file() -> Path:
    """Get path to agent connections config file"""
    config_root = get_config_root()
    connections_file = config_root / "lazy-bird" / "agent_connections.json"
    connections_file.parent.mkdir(parents=True, exist_ok=True)
    return connections_file


def load_agent_connections() -> List[dict]:
    """Load agent connections from file"""
    connections_file = get_agent_connections_file()

    # NO DEFAULT CONNECTIONS - empty by default
    default_connections = []

    if not connections_file.exists():
        # Create file with defaults
        with open(connections_file, 'w') as f:
            json.dump(default_connections, f, indent=2)
        return default_connections

    with open(connections_file, 'r') as f:
        return json.load(f)


def save_agent_connections(connections: List[dict]):
    """Save agent connections to file"""
    connections_file = get_agent_connections_file()
    with open(connections_file, 'w') as f:
        json.dump(connections, f, indent=2)


def scan_config_files() -> List[dict]:
    """Scan for all agent config files"""
    config_root = get_config_root()
    files = []

    # Scan .claude directory
    claude_dir = config_root / ".claude"
    if claude_dir.exists():
        # Skills
        skills_dir = claude_dir / "skills"
        if skills_dir.exists():
            for file in skills_dir.glob("*.md"):
                stat = file.stat()
                files.append({
                    "file_path": str(file.relative_to(config_root)),
                    "file_type": "skill",
                    "content": file.read_text(encoding='utf-8'),
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })

        # Commands (Instructions)
        commands_dir = claude_dir / "commands"
        if commands_dir.exists():
            for file in commands_dir.glob("*.md"):
                stat = file.stat()
                files.append({
                    "file_path": str(file.relative_to(config_root)),
                    "file_type": "instruction",
                    "content": file.read_text(encoding='utf-8'),
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })

    # Scan lazy-bird directory
    lazy_bird_dir = config_root / "lazy-bird"
    if lazy_bird_dir.exists():
        # Guidelines
        guidelines_dir = lazy_bird_dir / "guidelines"
        if guidelines_dir.exists():
            for file in guidelines_dir.glob("*.py"):
                stat = file.stat()
                files.append({
                    "file_path": str(file.relative_to(config_root)),
                    "file_type": "config",
                    "content": file.read_text(encoding='utf-8'),
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })

    return files


# ========== Endpoints ==========

@router.get("/connections", response_model=AgentConnectionsResponse)
async def get_agent_connections():
    """Get all agent connections"""
    try:
        connections = load_agent_connections()
        return {"connections": connections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load agent connections: {str(e)}")


@router.get("/connections/{agent_id}", response_model=AgentConnection)
async def get_agent_connection(agent_id: str):
    """Get specific agent connection"""
    try:
        connections = load_agent_connections()
        connection = next((c for c in connections if c["agent_id"] == agent_id), None)

        if not connection:
            raise HTTPException(status_code=404, detail=f"Agent connection '{agent_id}' not found")

        return connection
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load agent connection: {str(e)}")


@router.post("/connections", response_model=AgentConnection)
async def create_agent_connection(connection: AgentConnection):
    """Create new agent connection"""
    try:
        connections = load_agent_connections()

        # Check if agent_id already exists
        if any(c["agent_id"] == connection.agent_id for c in connections):
            raise HTTPException(status_code=400, detail=f"Agent connection '{connection.agent_id}' already exists")

        # Add new connection
        connections.append(connection.model_dump())
        save_agent_connections(connections)

        return connection
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent connection: {str(e)}")


@router.put("/connections/{agent_id}", response_model=AgentConnection)
async def update_agent_connection(agent_id: str, update: AgentConnectionUpdate):
    """Update agent connection"""
    try:
        connections = load_agent_connections()
        connection = next((c for c in connections if c["agent_id"] == agent_id), None)

        if not connection:
            raise HTTPException(status_code=404, detail=f"Agent connection '{agent_id}' not found")

        # Update fields
        update_data = update.model_dump(exclude_unset=True)
        connection.update(update_data)

        save_agent_connections(connections)

        return connection
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update agent connection: {str(e)}")


@router.delete("/connections/{agent_id}")
async def delete_agent_connection(agent_id: str):
    """Delete agent connection"""
    try:
        connections = load_agent_connections()
        original_len = len(connections)

        connections = [c for c in connections if c["agent_id"] != agent_id]

        if len(connections) == original_len:
            raise HTTPException(status_code=404, detail=f"Agent connection '{agent_id}' not found")

        save_agent_connections(connections)

        return {"message": f"Agent connection '{agent_id}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete agent connection: {str(e)}")


@router.get("/files", response_model=AgentConfigFilesResponse)
async def get_agent_config_files(file_type: Optional[str] = None):
    """Get all agent config files, optionally filtered by type"""
    try:
        files = scan_config_files()

        # Filter by type if specified
        if file_type:
            files = [f for f in files if f["file_type"] == file_type]

        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scan config files: {str(e)}")


@router.get("/files/{file_path:path}", response_model=AgentConfigFile)
async def get_agent_config_file(file_path: str):
    """Get specific agent config file"""
    try:
        config_root = get_config_root()
        full_path = config_root / file_path

        if not full_path.exists():
            raise HTTPException(status_code=404, detail=f"Config file '{file_path}' not found")

        if not full_path.is_file():
            raise HTTPException(status_code=400, detail=f"'{file_path}' is not a file")

        # Determine file type
        file_type = "config"
        if ".claude/skills" in file_path:
            file_type = "skill"
        elif ".claude/commands" in file_path:
            file_type = "instruction"
        elif "mcp" in file_path.lower():
            file_type = "mcp"

        stat = full_path.stat()

        return {
            "file_path": file_path,
            "file_type": file_type,
            "content": full_path.read_text(encoding='utf-8'),
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read config file: {str(e)}")


@router.put("/files/{file_path:path}", response_model=AgentConfigFile)
async def update_agent_config_file(file_path: str, update: AgentConfigFileUpdate):
    """Update agent config file content"""
    try:
        config_root = get_config_root()
        full_path = config_root / file_path

        if not full_path.exists():
            raise HTTPException(status_code=404, detail=f"Config file '{file_path}' not found")

        if not full_path.is_file():
            raise HTTPException(status_code=400, detail=f"'{file_path}' is not a file")

        # Write new content
        full_path.write_text(update.content, encoding='utf-8')

        # Return updated file
        return await get_agent_config_file(file_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update config file: {str(e)}")


@router.post("/files", response_model=AgentConfigFile)
async def create_agent_config_file(file: AgentConfigFile):
    """Create new agent config file"""
    try:
        config_root = get_config_root()
        full_path = config_root / file.file_path

        if full_path.exists():
            raise HTTPException(status_code=400, detail=f"Config file '{file.file_path}' already exists")

        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        full_path.write_text(file.content, encoding='utf-8')

        # Return created file
        return await get_agent_config_file(file.file_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create config file: {str(e)}")


@router.delete("/files/{file_path:path}")
async def delete_agent_config_file(file_path: str):
    """Delete agent config file"""
    try:
        config_root = get_config_root()
        full_path = config_root / file_path

        if not full_path.exists():
            raise HTTPException(status_code=404, detail=f"Config file '{file_path}' not found")

        if not full_path.is_file():
            raise HTTPException(status_code=400, detail=f"'{file_path}' is not a file")

        # Delete file
        full_path.unlink()

        return {"message": f"Config file '{file_path}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete config file: {str(e)}")
