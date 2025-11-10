"""
Lazy Bird Core Scripts

This package contains the main automation scripts:
- issue_watcher.py: GitHub issue monitoring and routing
- project_initializer.py: Automatic project setup from issues
- agent_selector.py: Cost-optimized AI agent routing
- project_manager.py: Project CRUD operations
- rover_adapter.py: Rover orchestration adapter
- smart_agent_switcher.py: Mid-task agent switching (ADR-005)

Usage:
    # Issue watcher (runs as daemon)
    python -m lazy_bird.scripts.issue_watcher

    # Initialize project from issue
    python -m lazy_bird.scripts.project_initializer \
        --issue 123 \
        --repo owner/repo

    # Select optimal agent
    from lazy_bird.scripts import AgentSelector

    selector = AgentSelector()
    agent = selector.select_best_agent(
        task_type='security',
        complexity=8,
        budget=20.0
    )
"""

__version__ = "1.0.0"
__author__ = "Phantom Neural Cortex Team"

from .agent_selector import AgentSelector
from .project_manager import ProjectManager
from .smart_agent_switcher import SmartAgentSwitcher

__all__ = [
    'AgentSelector',
    'ProjectManager',
    'SmartAgentSwitcher',
]
