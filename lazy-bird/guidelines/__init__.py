"""
Hierarchical Guidelines System (Layer 0-4)

This package provides AI agent guidelines organized in layers:
- LAYER-0: Universal standards (all agents)
- LAYER-1: MCP server usage
- LAYER-2: AI CLI general + agent-specific
- LAYER-3: Rover orchestration
- LAYER-4: Lazy Bird automation

Components:
- tools/guideline_injector.py: Guideline loading and composition
- embedding_generator.py: Hierarchical embeddings (256D→512D→1024D)

Usage:
    from lazy_bird.guidelines import GuidelineInjector

    injector = GuidelineInjector()

    # Load guidelines for specific layer and agent
    guidelines = injector.load_guidelines(
        layer=2,
        agent='claude'
    )

    # Inject into AI prompt
    prompt = injector.compose_prompt(
        task="Implement authentication",
        layer=2,
        agent='claude'
    )
"""

__version__ = "2.0.0"
__author__ = "Phantom Neural Cortex Team"

from .tools.guideline_injector import GuidelineInjector
from .embedding_generator import HierarchicalEmbeddingGenerator

__all__ = ['GuidelineInjector', 'HierarchicalEmbeddingGenerator']
