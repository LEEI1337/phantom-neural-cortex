import sys
import json
import asyncio
import importlib.util
import os
from typing import Any, Dict

async def run_skill(skill_path: str, action: str, params: Dict[str, Any]):
    """
    Standardizes skill execution inside the container.
    """
    try:
        # 1. Load the skill module
        spec = importlib.util.spec_from_file_location("skill_module", skill_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 2. Find the Skill class (usually exported via registry or defined in file)
        # For simplicity, we assume the file contains a 'skill' instance or a class we can instantiate
        skill_instance = None
        for item_name in dir(module):
            item = getattr(module, item_name)
            if hasattr(item, 'execute') and item_name != 'Skill':
                # Check if it's an instance or a class
                if isinstance(item, type):
                    skill_instance = item()
                else:
                    skill_instance = item
                break
        
        if not skill_instance:
            raise ValueError(f"No valid Skill implementation found in {skill_path}")

        # 3. Prepare Context (minimal, as many context features are host-side)
        # In a real scenario, we'd pass simplified context data
        from skills.base import SkillContext
        context = SkillContext(session_id="docker-execution")

        # 4. Execute
        result = await skill_instance.execute(action, context, **params)
        
        # 5. Output result
        print(json.dumps({
            "status": "success",
            "result": result
        }))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": str(e)
        }), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python bridge.py <skill_file> <action> <json_params>")
        sys.exit(1)
        
    skill_file = sys.argv[1]
    action = sys.argv[2]
    params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    
    asyncio.run(run_skill(skill_file, action, params))
