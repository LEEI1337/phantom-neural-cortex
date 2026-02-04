"""
Base Skill Class

Foundation for all skills in the system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SkillStatus(str, Enum):
    """Skill status enum"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"
    LOADING = "loading"


@dataclass
class SkillMetadata:
    """Skill metadata"""
    name: str
    version: str
    author: str
    description: str
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)


@dataclass
class SkillContext:
    """Context passed to skills during execution"""
    session_id: str
    user_id: Optional[str] = None
    workspace: str = "."
    metadata: Dict[str, Any] = field(default_factory=dict)


class Skill(ABC):
    """
    Base class for all skills.
    
    Skills are modular, hot-reloadable plugins that extend the capabilities
    of Phantom Neural Cortex. Similar to OpenClaw's skills system.
    """
    
    def __init__(
        self,
        name: str,
        version: str,
        author: str,
        description: str,
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None
    ):
        self.metadata = SkillMetadata(
            name=name,
            version=version,
            author=author,
            description=description,
            tags=tags or [],
            dependencies=dependencies or [],
            permissions=permissions or []
        )
        
        self.status = SkillStatus.ENABLED
        self.logger = logging.getLogger(f"skill.{name}")
    
    @abstractmethod
    async def execute(self, action: str, context: SkillContext, **kwargs) -> Any:
        """Execute skill action"""
        pass
    
    async def on_load(self):
        """Called when skill is loaded"""
        self.logger.info(f"Skill {self.metadata.name} loaded")
    
    async def on_unload(self):
        """Called when skill is unloaded"""
        self.logger.info(f"Skill {self.metadata.name} unloaded")
    
    def get_actions(self) -> List[str]:
        """Get list of available actions"""
        return [
            method[7:]
            for method in dir(self)
            if method.startswith('action_') and callable(getattr(self, method))
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary"""
        return {
            'name': self.metadata.name,
            'version': self.metadata.version,
            'author': self.metadata.author,
            'description': self.metadata.description,
            'tags': self.metadata.tags,
            'status': self.status.value,
            'actions': self.get_actions()
        }
