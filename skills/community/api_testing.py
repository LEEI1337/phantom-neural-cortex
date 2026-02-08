"""
API Testing Skill
Provides functionality for testing REST APIs.
"""

import httpx
from typing import Dict, Any
from ..base import Skill, SkillResult

class APITestingSkill(Skill):
    """
    Skill for testing and validating REST API endpoints.
    """
    
    def __init__(self):
        super().__init__(
            name="api_testing",
            version="1.0.0",
            description="REST API testing utilities",
            author="LEEI1337"
        )
        
    async def execute(self, action: str, params: Dict[str, Any]) -> SkillResult:
        if action == "test_endpoint":
            return await self._test_endpoint(params)
        else:
            return SkillResult(
                success=False,
                message=f"Unknown action: {action}",
                data={}
            )
            
    async def _test_endpoint(self, params: Dict[str, Any]) -> SkillResult:
        url = params.get("url")
        method = params.get("method", "GET").upper()
        headers = params.get("headers", {})
        payload = params.get("payload")
        
        if not url:
            return SkillResult(success=False, message="URL is required", data={})
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, headers=headers, json=payload, timeout=10.0)
                
                return SkillResult(
                    success=True,
                    message=f"API Request to {url} completed with status {response.status_code}",
                    data={
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "body": response.text[:1000] # Truncate for safety
                    }
                )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"API Request failed: {str(e)}",
                data={}
            )
