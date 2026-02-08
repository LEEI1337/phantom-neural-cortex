import os
import json
import asyncio
import logging
from typing import Any, Dict
from skills.base import Skill, SkillContext

# Set up logging to captured output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MaliciousSkill(Skill):
    """
    A skill designed to test sandbox isolation boundaries.
    """
    def __init__(self):
        super().__init__(
            name="malicious_test_skill",
            version="1.0.0",
            author="Security Auditor",
            description="Tests sandbox escapes and resource exhaustion.",
            tags=["security", "test"]
        )

    async def execute(self, action: str, context: SkillContext, **kwargs) -> Dict[str, Any]:
        if action == "test_fs_escape":
            return await self._test_fs_escape()
        elif action == "test_network_access":
            return await self._test_network_access()
        elif action == "test_resource_exhaustion":
            return await self._test_resource_exhaustion()
        elif action == "test_env_leak":
            return await self._test_env_leak()
        else:
            raise ValueError(f"Unknown security test action: {action}")

    async def _test_fs_escape(self) -> Dict[str, Any]:
        """Try to read sensitive files from the host."""
        paths_to_test = [
            "/etc/passwd",          # Linux sensitive
            "/proc/self/environ",   # Process info
            "C:/Windows/win.ini",   # Windows sensitive
            "../../.env"            # Host env file relative escape
        ]
        
        results = {}
        for path in paths_to_test:
            try:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        content = f.read(20) # Read a snippet
                    results[path] = f"EXPOSED: {content}..."
                else:
                    results[path] = "SECURE: Path not found"
            except Exception as e:
                results[path] = f"SECURE: Access Denied ({str(e)})"
        
        return results

    async def _test_network_access(self) -> Dict[str, Any]:
        """Try to reach the outside world."""
        import socket
        targets = [("google.com", 80), ("8.8.8.8", 53)]
        results = {}
        
        for host, port in targets:
            try:
                socket.setdefaulttimeout(2)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
                results[host] = "EXPOSED: Connection Successful"
            except Exception as e:
                results[host] = f"SECURE: Connection Failed ({str(e)})"
        
        return results

    async def _test_resource_exhaustion(self) -> Dict[str, Any]:
        """Try to consume all memory."""
        # Note: This is dangerous but limited by the container
        try:
            # Try to allocate 1GB in a loop (Docker limit is 256MB/512MB)
            garbage = []
            for i in range(10):
                garbage.append(" " * (100 * 1024 * 1024)) # 100MB chunks
            return {"status": "EXPOSED: Resource limit not enforced (Allocated ~1GB)"}
        except MemoryError:
            return {"status": "SECURE: MemoryError caught (Limit enforced)"}
        except Exception as e:
            return {"status": f"SECURE: Process killed or error ({str(e)})"}

    async def _test_env_leak(self) -> Dict[str, Any]:
        """Check for host credentials in environment variables."""
        sensitive_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DATABASE_URL"]
        leaks = {k: os.environ.get(k, "NOT_FOUND") for k in sensitive_keys}
        return leaks
