"""
Skills Registry

Discovers and manages available skills.
"""

import logging
from typing import Dict, Optional, List
from pathlib import Path
import importlib
import sys

from .base import Skill, SkillStatus

logger = logging.getLogger(__name__)


class SkillRegistry:
    """
    Registry for managing skills.
    
    Features:
    - Discover skills in skills/ directory
    - Load/unload skills dynamically
    - Hot-reload on file changes
    - Track enabled/disabled skills
    """
    
    def __init__(self, skills_dir: str = "skills/community"):
        """
        Initialize registry.
        
        Args:
            skills_dir: Directory containing skill modules
        """
        self.skills_dir = Path(skills_dir)
        self._skills: Dict[str, Skill] = {}
        self._skill_modules: Dict[str, any] = {}
        
        logger.info(f"SkillRegistry initialized with directory: {skills_dir}")
    
    async def discover_skills(self) -> List[str]:
        """
        Discover available skills in skills directory.
        
        Returns:
            List of discovered skill names
        """
        discovered = []
        
        if not self.skills_dir.exists():
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return discovered
        
        # Find all Python files
        for skill_file in self.skills_dir.glob("*.py"):
            if skill_file.name.startswith("_"):
                continue
            
            skill_name = skill_file.stem
            discovered.append(skill_name)
            logger.info(f"Discovered skill: {skill_name}")
        
        return discovered
    
    async def load_skill(self, skill_name: str) -> bool:
        """
        Load skill by name.
        
        Args:
            skill_name: Name of skill to load
            
        Returns:
            True if loaded successfully
        """
        try:
            # Import skill module
            module_path = f"skills.community.{skill_name}"
            
            if module_path in sys.modules:
                # Reload if already loaded
                module = importlib.reload(sys.modules[module_path])
            else:
                module = importlib.import_module(module_path)
            
            # Find Skill class in module
            skill_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, Skill) and 
                    attr != Skill):
                    skill_class = attr
                    break
            
            if not skill_class:
                logger.error(f"No Skill class found in {skill_name}")
                return False
            
            # Instantiate skill
            skill = skill_class()
            
            # Call on_load
            await skill.on_load()
            
            # Register skill
            self._skills[skill_name] = skill
            self._skill_modules[skill_name] = module
            
            logger.info(f"Loaded skill: {skill_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to load skill {skill_name}: {e}")
            return False
    
    async def unload_skill(self, skill_name: str) -> bool:
        """
        Unload skill by name.
        
        Args:
            skill_name: Name of skill to unload
            
        Returns:
            True if unloaded successfully
        """
        if skill_name not in self._skills:
            return False
        
        try:
            skill = self._skills[skill_name]
            await skill.on_unload()
            
            del self._skills[skill_name]
            del self._skill_modules[skill_name]
            
            logger.info(f"Unloaded skill: {skill_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to unload skill {skill_name}: {e}")
            return False
    
    async def reload_skill(self, skill_name: str) -> bool:
        """
        Reload skill (unload then load).
        
        Args:
            skill_name: Name of skill to reload
            
        Returns:
            True if reloaded successfully
        """
        if skill_name in self._skills:
            await self.unload_skill(skill_name)
        
        return await self.load_skill(skill_name)
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get skill by name"""
        return self._skills.get(skill_name)
    
    def list_skills(self, status: Optional[SkillStatus] = None) -> List[Skill]:
        """
        List all skills.
        
        Args:
            status: Optional status filter
            
        Returns:
            List of skills
        """
        skills = list(self._skills.values())
        
        if status:
            skills = [s for s in skills if s.status == status]
        
        return skills
    
    async def enable_skill(self, skill_name: str) -> bool:
        """Enable skill"""
        skill = self.get_skill(skill_name)
        if not skill:
            return False
        
        await skill.on_enable()
        return True
    
    async def disable_skill(self, skill_name: str) -> bool:
        """Disable skill"""
        skill = self.get_skill(skill_name)
        if not skill:
            return False
        
        await skill.on_disable()
        return True
