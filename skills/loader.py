"""
Skill Loader

Dynamic skill loading with dependency injection.
"""

import logging
from typing import Optional

from .base import Skill
from .registry import SkillRegistry

logger = logging.getLogger(__name__)


class SkillLoader:
    """
    Loads skills with dependency injection.
    """
    
    def __init__(self, registry: SkillRegistry):
        """
        Initialize loader.
        
        Args:
            registry: Skill registry
        """
        self.registry = registry
        logger.info("SkillLoader initialized")
    
    async def load_all_skills(self) -> int:
        """
        Discover and load all skills.
        
        Returns:
            Number of skills loaded
        """
        discovered = await self.registry.discover_skills()
        
        loaded_count = 0
        for skill_name in discovered:
            success = await self.registry.load_skill(skill_name)
            if success:
                loaded_count += 1
        
        logger.info(f"Loaded {loaded_count}/{len(discovered)} skills")
        return loaded_count
