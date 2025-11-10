"""
Spec-Kit Integration System

This package implements GitHub Spec-Driven Development workflow:
- 7-phase workflow (Constitution → Analyze)
- ML/RL optimizations per phase
- Smart agent switching
- Quality checkpointing

Phases:
1. Constitution: Define principles and constraints
2. Specify: Create detailed requirements
3. Clarify: Resolve ambiguities
4. Plan: Design architecture
5. Tasks: Generate implementation tasks
6. Implement: Execute with refinement
7. Analyze: Validate results

Components:
- speckit_orchestrator.py: Main orchestrator for Spec-Kit workflow

Usage:
    from lazy_bird.speckit import SpecKitOrchestrator

    orchestrator = SpecKitOrchestrator(
        project_id='my-project',
        project_path='/path/to/project',
        ai_agent='claude',
        enable_latent_reasoning=True,
        enable_rl_refinement=True,
        enable_smart_switching=True
    )

    # Create and run feature
    result = await orchestrator.run_feature(
        feature_id='user-auth',
        name='User Authentication',
        description='OAuth2 + JWT authentication system'
    )
"""

__version__ = "2.0.0"
__author__ = "Phantom Neural Cortex Team"

from .speckit_orchestrator import SpecKitOrchestrator

__all__ = ['SpecKitOrchestrator']
