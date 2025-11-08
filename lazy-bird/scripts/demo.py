#!/usr/bin/env python3
"""
Lazy Bird Demo - Demonstrates the autonomous workflow

This script shows how the Lazy Bird system would work without requiring
actual GitHub API access or Rover installation.
"""

import sys
import importlib.util

# Import modules with hyphens in filenames
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

agent_selector = load_module("agent_selector", "agent-selector.py")
project_manager = load_module("project_manager", "project-manager.py")

AgentSelector = agent_selector.AgentSelector
ProjectManager = project_manager.ProjectManager


def demo_agent_selection():
    """Demonstrate intelligent agent selection based on issue labels."""
    print("\n" + "=" * 60)
    print("🤖 DEMO: Agent Selection (Cost Optimization)")
    print("=" * 60 + "\n")
    
    selector = AgentSelector()
    
    # Simulate different types of issues
    test_cases = [
        {
            "title": "Fix critical security vulnerability in authentication",
            "labels": ["security", "critical", "bug"],
            "expected": "claude"
        },
        {
            "title": "Generate API documentation for 200 endpoints",
            "labels": ["documentation", "enhancement"],
            "expected": "gemini"
        },
        {
            "title": "Update GitHub Actions workflow",
            "labels": ["github-workflow", "ci-cd"],
            "expected": "copilot"
        },
        {
            "title": "Refactor codebase to use TypeScript",
            "labels": ["enhancement", "bulk-refactor"],
            "expected": "gemini"
        },
        {
            "title": "Add new feature without specific labels",
            "labels": ["enhancement"],
            "expected": "gemini"  # fallback
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. Issue: {test['title']}")
        print(f"   Labels: {', '.join(test['labels'])}")
        
        agent = selector.select_agent(test['labels'], "demo-project")
        
        print(f"   Selected: {agent}")
        print(f"   Expected: {test['expected']}")
        print(f"   Result: {'✅ CORRECT' if agent == test['expected'] else '❌ MISMATCH'}\n")
    
    # Show usage statistics
    print("\n" + "-" * 60)
    print("📊 Usage Statistics")
    print("-" * 60 + "\n")
    
    stats = selector.get_usage_stats()
    for agent, data in stats.items():
        print(f"{agent.upper()}: {data['count']} tasks ({data['percentage']:.1f}%)")
        print(f"  Cost level: {data['cost_level']}")
    
    # Show optimization suggestions
    print("\n" + "-" * 60)
    print("💡 Cost Optimization Suggestions")
    print("-" * 60 + "\n")
    
    suggestions = selector.suggest_optimization()
    for suggestion in suggestions:
        print(suggestion)


def demo_project_management():
    """Demonstrate multi-project configuration."""
    print("\n" + "=" * 60)
    print("📦 DEMO: Project Management")
    print("=" * 60 + "\n")
    
    manager = ProjectManager("../configs/projects.json")
    
    print(f"Loaded {len(manager.projects)} project(s):\n")
    
    for project in manager.projects:
        print(f"Project: {project['name']}")
        print(f"  ID: {project['id']}")
        print(f"  Type: {project['type']}")
        print(f"  Repo: {project['repo']}")
        print(f"  Rover Enabled: {'✅ Yes' if project.get('rover_enabled') else '❌ No'}")
        
        settings = project.get('settings', {})
        print(f"  Default Agent: {settings.get('default_agent', 'N/A')}")
        print(f"  Test Command: {settings.get('test_command', 'N/A')}")
        print()


def demo_workflow():
    """Demonstrate the complete workflow."""
    print("\n" + "=" * 60)
    print("🔄 DEMO: Complete Workflow")
    print("=" * 60 + "\n")
    
    print("Simulated GitHub Issue:")
    print("-" * 60)
    print("Title: Add OAuth2.0 authentication")
    print("Labels: ['lazy-bird', 'security', 'feature']")
    print("Body: Implement JWT-based authentication with refresh tokens...")
    print()
    
    print("Step 1: Issue Watcher detects issue")
    print("  ✅ Issue #42 detected with 'lazy-bird' label")
    print()
    
    print("Step 2: Agent Selector chooses AI")
    selector = AgentSelector()
    agent = selector.select_agent(["security", "feature"], "ai-orchestrator")
    print(f"  ✅ Selected: {agent} (security label detected)")
    print()
    
    print("Step 3: Rover Adapter creates task")
    print(f"  ✅ Command: rover task 'Add OAuth2.0...' --agent {agent}")
    print("  ✅ Task ID: task-abc123")
    print()
    
    print("Step 4: Rover executes in isolated environment")
    print("  ✅ Created git worktree: .rover/task-abc123")
    print("  ✅ Started Docker container")
    print(f"  ✅ Running {agent} with MCP servers")
    print()
    
    print("Step 5: AI implements the feature")
    print("  ✅ Generated authentication module")
    print("  ✅ Added JWT token handling")
    print("  ✅ Created tests")
    print("  ✅ Updated documentation")
    print()
    
    print("Step 6: Test Coordinator validates")
    print("  ✅ Running: pytest tests/ -v")
    print("  ✅ Tests passed: 15/15")
    print()
    
    print("Step 7: Rover merges and creates PR")
    print("  ✅ Merged changes to main branch")
    print("  ✅ Created PR: https://github.com/.../pull/123")
    print("  ✅ Added comment to issue #42")
    print()
    
    print("Step 8: Human reviews and merges")
    print("  👤 Developer reviews code quality")
    print("  👤 Developer merges PR")
    print("  ✅ Issue #42 automatically closed")
    print()
    
    print("=" * 60)
    print("🎉 Complete autonomous workflow demonstrated!")
    print("=" * 60)


def main():
    """Run all demos."""
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  🚀 LAZY BIRD - AUTONOMOUS DEVELOPMENT DEMO".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    
    demo_agent_selection()
    demo_project_management()
    demo_workflow()
    
    print("\n" + "=" * 60)
    print("📖 Learn More")
    print("=" * 60)
    print("\nDocumentation:")
    print("  • Setup Guide (EN): ../docs/LAZY-BIRD-SETUP-EN.md")
    print("  • Setup Guide (DE): ../docs/LAZY-BIRD-SETUP-DE.md")
    print("  • Architecture: ../docs/LAZY-BIRD-ARCHITECTURE.md")
    print("  • README: ../lazy-bird/README.md")
    print("\nTo start using Lazy Bird:")
    print("  1. Configure projects in ../configs/projects.json")
    print("  2. Set GITHUB_TOKEN environment variable")
    print("  3. Run: python3 issue-watcher.py")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
