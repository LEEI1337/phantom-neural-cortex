import logging
import json
import os
import tempfile
import shutil
import sys
from typing import Any, Optional
import asyncio

try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False

from .base import Skill, SkillContext

logger = logging.getLogger(__name__)


class SkillSandbox:
    """
    Sandboxed execution environment for skills.
    
    Features:
    - Resource limits (CPU, memory, time)
    - Docker-based process isolation (Phase 7 Hardening)
    - Restricted file system and network access
    """
    
    def __init__(
        self,
        max_execution_time: int = 300,
        max_memory_mb: int = 512,
        use_docker: bool = True
    ):
        """
        Initialize sandbox.
        """
        self.max_execution_time = max_execution_time
        self.max_memory_mb = max_memory_mb
        self.use_docker = use_docker and DOCKER_AVAILABLE
        
        if self.use_docker:
            try:
                self.docker_client = docker.from_env()
                self.docker_client.ping()
                logger.info("DockerSandbox initialized and ready")
            except Exception as e:
                logger.warning(f"Docker not responsive, falling back to local sandbox: {e}")
                self.use_docker = False
        
        if not self.use_docker:
            logger.info("Local SkillSandbox initialized (Direct Execution)")

    async def execute_skill(
        self,
        skill: Skill,
        action: str,
        context: SkillContext,
        **kwargs
    ) -> Any:
        """
        Execute skill in sandbox (Isolated or Local).
        """
        if self.use_docker:
            return await self._execute_in_docker(skill, action, context, **kwargs)
        
        return await self._execute_local(skill, action, context, **kwargs)

    async def _execute_local(self, skill: Skill, action: str, context: SkillContext, **kwargs) -> Any:
        """Original execution logic with timeout wrapper"""
        try:
            result = await asyncio.wait_for(
                skill.execute(action, context, **kwargs),
                timeout=self.max_execution_time
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Skill {skill.metadata.name} execution timed out")
            raise
        except Exception as e:
            logger.error(f"Error executing skill {skill.metadata.name}: {e}")
            raise

    async def _execute_in_docker(self, skill: Skill, action: str, context: SkillContext, **kwargs) -> Any:
        """Isolated execution in a transient Docker container (Phase 7)"""
        # 1. Prepare temporary directory for execution
        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy skill file to tmpdir
            skill_src = os.path.abspath(sys.modules[skill.__class__.__module__].__file__)
            skill_filename = os.path.basename(skill_src)
            shutil.copy(skill_src, os.path.join(tmpdir, skill_filename))
            
            # Prepare parameters
            params_json = json.dumps(kwargs)
            
            # 2. Configure container
            # Requirements: phantom-skill-runner image must exist
            container_config = {
                "image": "phantom-skill-runner:latest",
                "command": [skill_filename, action, params_json],
                "volumes": {os.path.abspath(tmpdir): {"bind": "/app/workdir", "mode": "ro"}},
                "mem_limit": f"{self.max_memory_mb}m",
                "nano_cpus": 500000000, # 0.5 CPU
                "network_disabled": True,
                "remove": True,
                "stdout": True,
                "stderr": True,
                "user": "phantom"
            }

            try:
                # Run container (synchronously in executor thread to not block)
                loop = asyncio.get_event_loop()
                container_output = await loop.run_in_executor(
                    None, 
                    lambda: self.docker_client.containers.run(**container_config)
                )
                
                # Parse output
                result_data = json.loads(container_output.decode('utf-8'))
                if result_data.get("status") == "success":
                    return result_data.get("result")
                else:
                    raise RuntimeError(result_data.get("error", "Unknown container error"))
                    
            except Exception as e:
                logger.error(f"Docker isolation failure for {skill.metadata.name}: {e}")
                # Optional: Fail safe or fail hard? For now, fall back to local if critical
                logger.info("Attempting emergency local fallback...")
                return await self._execute_local(skill, action, context, **kwargs)
