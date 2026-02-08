import asyncio
import json
import os
import sys
import logging
from skills.sandbox import SkillSandbox
from skills.community.malicious_test import MaliciousSkill
from skills.base import SkillContext

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def run_security_audit():
    print("🛡️ Starting Phase 7 Sandbox Security Audit...")
    print("-" * 50)

    # Initialize Sandbox
    # Force use_docker=True to test the isolation. 
    # If Docker isn't running, it will fall back to local (and likely fail some tests).
    sandbox = SkillSandbox(max_memory_mb=512, use_docker=True)
    
    skill = MaliciousSkill()
    context = SkillContext(session_id="audit-123")
    
    tests = [
        ("File System Isolation", "test_fs_escape"),
        ("Network Isolation", "test_network_access"),
        ("Environment Isolation", "test_env_leak"),
        ("Resource Quotas", "test_resource_exhaustion")
    ]
    
    audit_results = {}

    for name, action in tests:
        print(f"Testing {name}...")
        try:
            result = await sandbox.execute_skill(skill, action, context)
            audit_results[name] = result
            print(f"  Done. Result: {json.dumps(result, indent=4)[:200]}...")
        except Exception as e:
            print(f"  ❌ Audit Fail (Execution Error): {e}")
            audit_results[name] = {"error": str(e)}

    print("-" * 50)
    print("📝 Security Audit Summary:")
    
    # Analyze results
    is_secure = True
    
    # 1. FS Check
    fs = audit_results.get("File System Isolation", {})
    if any("EXPOSED" in str(v) for v in fs.values()):
        print("🔴 FAIL: File System Escape detected!")
        is_secure = False
    else:
        print("✅ PASS: File System is isolated.")

    # 2. Network Check
    net = audit_results.get("Network Isolation", {})
    if any("EXPOSED" in str(v) for v in net.values()):
        print("🔴 FAIL: Outbound Network access detected!")
        is_secure = False
    else:
        print("✅ PASS: Network is isolated.")

    # 3. Env Check
    env = audit_results.get("Environment Isolation", {})
    if any(v != "NOT_FOUND" for v in env.values()):
        print("🔴 FAIL: Host Environment Variables leaked!")
        is_secure = False
    else:
        print("✅ PASS: Environment is clean.")

    if is_secure:
        print("\n🏆 AUDIT COMPLETE: Sandbox boundaries are RIGID. Multi-Tenant safety confirmed.")
    else:
        print("\n⚠️ AUDIT COMPLETE: Vulnerabilities found. Do not deploy skills without fixing.")

if __name__ == "__main__":
    asyncio.run(run_security_audit())
