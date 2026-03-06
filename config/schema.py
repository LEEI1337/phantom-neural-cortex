"""AGENT.yaml schema definition and validation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class LLMConfig(BaseModel):
    planner: str = "opus-4.6"
    executor: str = "mistral-small3.2"
    fallback: list[str] = Field(default_factory=lambda: ["llama3.1:8b"])
    local_only: bool = False
    ollama_url: str = "http://10.40.10.90:11434"


class MattermostConfig(BaseModel):
    token_vault_path: str = ""
    channels: list[str] = Field(default_factory=list)
    home_channel: str = ""
    url: str = "http://10.40.10.83:8065"


class CommunicationConfig(BaseModel):
    mattermost: MattermostConfig = Field(default_factory=MattermostConfig)


class SecurityConfig(BaseModel):
    nss_enabled: bool = True
    mars_threshold: float = 0.7
    approval_level: str = "RISKY"  # SAFE, RISKY, BLOCKED
    killswitch_owners: list[str] = Field(default_factory=lambda: ["joe"])
    nss_gateway_url: str = "http://localhost:11337"
    nss_guardian_url: str = "http://localhost:11338"
    nss_governance_url: str = "http://localhost:11339"

    @field_validator("approval_level")
    @classmethod
    def validate_approval_level(cls, v: str) -> str:
        valid = {"SAFE", "RISKY", "BLOCKED"}
        if v.upper() not in valid:
            raise ValueError(f"approval_level must be one of {valid}")
        return v.upper()


class MemoryConfig(BaseModel):
    rag_enabled: bool = True
    persist_learnings: bool = True
    context_max_tokens: int = 8192


class ToolsConfig(BaseModel):
    allowed: list[str] = Field(default_factory=lambda: ["file", "system", "knowledge"])
    blocked: list[str] = Field(default_factory=list)


class AgentConfig(BaseModel):
    """Root configuration for a Phantom Agent."""

    # Identity
    name: str
    role: str = "General Agent"
    description: str = ""

    # LLM
    llm: LLMConfig = Field(default_factory=LLMConfig)

    # Communication
    communication: CommunicationConfig = Field(default_factory=CommunicationConfig)

    # Security
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    # Tools
    tools: ToolsConfig = Field(default_factory=ToolsConfig)

    # Memory
    memory: MemoryConfig = Field(default_factory=MemoryConfig)

    # Paths
    rules_path: str = "./rules/"
    skills_path: str = "./skills/"

    # echo_log connection
    echoLog_url: str = "http://10.40.10.82:8085"

    @classmethod
    def from_yaml(cls, path: str | Path) -> AgentConfig:
        """Load agent config from YAML file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Agent config not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        # Flatten nested "agent" key if present
        if "agent" in raw and isinstance(raw["agent"], dict):
            agent_data = raw.pop("agent")
            raw = {**agent_data, **raw}

        return cls(**raw)

    def to_yaml(self, path: str | Path):
        """Save agent config to YAML file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {"agent": {"name": self.name, "role": self.role, "description": self.description}}
        data["llm"] = self.llm.model_dump()
        data["communication"] = self.communication.model_dump()
        data["security"] = self.security.model_dump()
        data["tools"] = self.tools.model_dump()
        data["memory"] = self.memory.model_dump()
        data["rules_path"] = self.rules_path
        data["skills_path"] = self.skills_path
        data["echoLog_url"] = self.echoLog_url

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        logger.info(f"Agent config saved to {path}")
