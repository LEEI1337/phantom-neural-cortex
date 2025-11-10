"""
Multi-Repository Coordination System (ADR-009)

This package implements cross-repository dependency management:
- NetworkX dependency graph analysis
- Topological sorting for safe update ordering
- Atomic multi-repository PR creation
- Coordinated deployment strategies

Components:
- dependency_analyzer.py: Dependency graph analysis and coordination

Usage:
    from lazy_bird.multi_repo import DependencyAnalyzer

    analyzer = DependencyAnalyzer(repositories=[
        '/path/to/repo1',
        '/path/to/repo2',
        '/path/to/repo3'
    ])

    # Analyze dependencies
    graph = analyzer.build_dependency_graph()

    # Get safe update order
    update_order = analyzer.get_update_order()

    # Create coordinated PRs
    analyzer.create_atomic_prs(
        feature_branch='add-auth-system',
        commit_message='Add authentication across services'
    )
"""

__version__ = "1.0.0"
__author__ = "Phantom Neural Cortex Team"

from .dependency_analyzer import DependencyAnalyzer

__all__ = ['DependencyAnalyzer']
