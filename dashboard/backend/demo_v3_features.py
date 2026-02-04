"""
v3.0 Features Demo

This script demonstrates all the new v3.0 features:
- Context Window Management (Phase 1)
- Gateway Architecture (Phase 2)
- Skills System (Phase 3)
"""

import asyncio
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


async def demo_context_management():
    """Demo Phase 1: Context Window Management"""
    print("\n" + "="*60)
    print("PHASE 1: Context Window Management Demo")
    print("="*60)
    
    try:
        from dashboard.backend.context import (
            ContextTracker, 
            ContextPruner,
            ContextInspector,
            ModelType
        )
        
        # Create context tracker
        tracker = ContextTracker(
            session_id="demo_session",
            model=ModelType.CLAUDE
        )
        
        # Add messages
        tracker.add_system_prompt("You are a helpful AI assistant", pinned=True)
        tracker.add_user_message("What is Python?")
        tracker.add_assistant_message("Python is a high-level programming language...")
        tracker.add_tool_call("search", "python")
        tracker.add_tool_result("Python.org - Official Website", "search")
        
        # Get status
        status = tracker.get_status()
        print(f"\n✓ Context Status:")
        print(f"  - Total Tokens: {status.total_tokens}/{status.max_tokens}")
        print(f"  - Usage: {status.usage_percent:.1f}%")
        print(f"  - Items: {status.item_count}")
        
        # Use inspector
        inspector = ContextInspector(tracker)
        print(f"\n✓ Context Items:")
        for item in tracker.get_items()[:3]:
            print(f"  - [{item.type.value}] {item.tokens} tokens")
        
        print("\n✓ Context Management Demo Complete!")
        
    except Exception as e:
        print(f"✗ Context Management Demo Failed: {e}")
        import traceback
        traceback.print_exc()


async def demo_gateway():
    """Demo Phase 2: Gateway Architecture"""
    print("\n" + "="*60)
    print("PHASE 2: Gateway Architecture Demo")
    print("="*60)
    
    try:
        from gateway import GatewayConfig, SessionManager, MessageRouter, HealthMonitor
        
        # Create configuration
        config = GatewayConfig(
            host="0.0.0.0",
            port=18789,
            session_timeout=3600
        )
        print(f"\n✓ Gateway Configuration:")
        print(f"  - Host: {config.host}")
        print(f"  - Port: {config.port}")
        print(f"  - Session Timeout: {config.session_timeout}s")
        
        # Create session manager
        session_manager = SessionManager(storage_backend="memory")
        await session_manager.start()
        
        # Create session
        session = await session_manager.create_session(user_id="demo_user")
        print(f"\n✓ Session Created:")
        print(f"  - Session ID: {session.session_id}")
        print(f"  - Status: {session.status.value}")
        
        # Create message router
        router = MessageRouter(queue_size=1000)
        print(f"\n✓ Message Router Initialized")
        
        # Create health monitor
        health = HealthMonitor(check_interval=30)
        await health.start()
        health_status = await health.get_health_status(session_manager, router)
        print(f"\n✓ Health Status:")
        print(f"  - Status: {health_status.status.value}")
        print(f"  - Active Sessions: {health_status.active_sessions}")
        
        # Cleanup
        await health.stop()
        await session_manager.stop()
        
        print("\n✓ Gateway Architecture Demo Complete!")
        
    except Exception as e:
        print(f"✗ Gateway Demo Failed: {e}")
        import traceback
        traceback.print_exc()


async def demo_skills():
    """Demo Phase 3: Skills System"""
    print("\n" + "="*60)
    print("PHASE 3: Skills System Demo")
    print("="*60)
    
    try:
        from skills import SkillRegistry, SkillLoader, SkillContext
        
        # Create registry
        registry = SkillRegistry("skills/community")
        print(f"\n✓ Skills Registry Created")
        
        # Discover skills
        discovered = await registry.discover_skills()
        print(f"\n✓ Discovered {len(discovered)} skills:")
        for skill_name in discovered:
            print(f"  - {skill_name}")
        
        # Load skills
        loader = SkillLoader(registry)
        loaded_count = await loader.load_all_skills()
        print(f"\n✓ Loaded {loaded_count} skills")
        
        # List loaded skills
        skills = registry.list_skills()
        if skills:
            print(f"\n✓ Loaded Skills:")
            for skill in skills:
                print(f"  - {skill.metadata.name} v{skill.metadata.version}")
                print(f"    Author: {skill.metadata.author}")
                print(f"    Actions: {', '.join(skill.get_actions())}")
        
        # Execute skill if available
        if skills:
            skill = skills[0]
            context = SkillContext(session_id="demo", workspace=".")
            
            # Get available actions
            actions = skill.get_actions()
            if actions:
                action = actions[0]
                print(f"\n✓ Executing skill action: {action}")
                
                # Note: This is a demo, actual execution might require specific parameters
                try:
                    # Mock execution for demo
                    print(f"  - Skill: {skill.metadata.name}")
                    print(f"  - Action: {action}")
                    print(f"  - Status: Ready to execute")
                except Exception as e:
                    print(f"  - Note: {e}")
        
        print("\n✓ Skills System Demo Complete!")
        
    except Exception as e:
        print(f"✗ Skills Demo Failed: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("PHANTOM NEURAL CORTEX v3.0 - FEATURES DEMO")
    print("="*60)
    print("\nDemonstrating all new OpenClaw-inspired features:")
    print("  1. Context Window Management")
    print("  2. Gateway Architecture")
    print("  3. Skills System")
    
    # Run demos
    await demo_context_management()
    await demo_gateway()
    await demo_skills()
    
    # Summary
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("\nAll v3.0 features have been demonstrated.")
    print("Phantom Neural Cortex is now OpenClaw-compatible")
    print("with additional unique features:")
    print("  ✓ Quality Assessment")
    print("  ✓ Guidelines Evolution")
    print("  ✓ Multi-Agent Cost Optimization")
    print("\nResult: Best-of-both-worlds platform! 🏆")
    print("="*60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nDemo failed: {e}")
        import traceback
        traceback.print_exc()
