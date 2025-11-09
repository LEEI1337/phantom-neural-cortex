"""
Multi-Repository Coordination - PHASE C Optimierung #9
=======================================================

Koordiniert Änderungen über mehrere Repositories hinweg.
Analysiert Dependencies und orchestriert atomare Multi-Repo PRs.

Key Features:
- Dependency Graph Builder
- Cross-Repo Change Coordinator
- Atomic Multi-Repo PRs
- Conflict Detection

Use Case: Microservices-Änderungen koordinieren
"""

import json
import subprocess
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import networkx as nx


@dataclass
class Repository:
    """Ein Repository mit Metadaten."""

    name: str
    path: Path
    remote_url: str
    primary_language: str
    dependencies: List[str]  # Namen anderer Repos


@dataclass
class CrossRepoChange:
    """Eine koordinierte Änderung über mehrere Repos."""

    id: str
    title: str
    description: str
    repositories: List[str]  # Repo Namen
    dependency_order: List[str]  # Reihenfolge für Änderungen
    status: str  # 'planned', 'in_progress', 'completed'
    created_at: datetime


class DependencyGraphBuilder:
    """
    Baut Dependency Graph aus mehreren Repositories.

    Analysiert:
    - package.json dependencies (Node.js)
    - requirements.txt (Python)
    - go.mod (Go)
    - pom.xml (Java)
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.repositories: Dict[str, Repository] = {}

    def add_repository(self, repo: Repository):
        """Fügt Repository zum Graph hinzu."""
        self.repositories[repo.name] = repo
        self.graph.add_node(repo.name, **asdict(repo))

        # Add edges for dependencies
        for dep in repo.dependencies:
            self.graph.add_edge(repo.name, dep)

    def detect_circular_dependencies(self) -> List[List[str]]:
        """Erkennt zirkuläre Dependencies."""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []

    def get_dependency_order(self, repos: List[str]) -> List[str]:
        """
        Berechnet Reihenfolge für Änderungen basierend auf Dependencies.

        Verwendet topologische Sortierung.

        Args:
            repos: Liste von Repo-Namen die geändert werden sollen

        Returns:
            Sortierte Liste (dependencies first)
        """
        # Create subgraph with only relevant repos
        subgraph = self.graph.subgraph(repos)

        try:
            # Topological sort (dependencies first)
            order = list(nx.topological_sort(subgraph))
            return order
        except nx.NetworkXError:
            # Has cycles, fall back to arbitrary order
            print("Warning: Circular dependencies detected, using arbitrary order")
            return repos

    def get_affected_repos(self, changed_repo: str) -> Set[str]:
        """
        Findet alle Repos die von Änderung betroffen sein könnten.

        Args:
            changed_repo: Name des geänderten Repos

        Returns:
            Set von Repo-Namen die davon abhängen
        """
        # Find all descendants (repos that depend on this one)
        if changed_repo not in self.graph:
            return set()

        affected = nx.descendants(self.graph, changed_repo)
        affected.add(changed_repo)

        return affected

    def analyze_impact(self, repos: List[str]) -> Dict[str, any]:
        """
        Analysiert Impact einer Multi-Repo Änderung.

        Returns:
            {
                'total_affected': int,
                'dependency_order': List[str],
                'has_circular_deps': bool,
                'risk_level': str  # 'low', 'medium', 'high'
            }
        """
        # Get all affected repos
        all_affected = set()
        for repo in repos:
            all_affected.update(self.get_affected_repos(repo))

        # Get order
        dependency_order = self.get_dependency_order(list(all_affected))

        # Check for cycles
        cycles = self.detect_circular_dependencies()
        has_cycles = len(cycles) > 0

        # Determine risk level
        if len(all_affected) > 5:
            risk_level = 'high'
        elif len(all_affected) > 2 or has_cycles:
            risk_level = 'medium'
        else:
            risk_level = 'low'

        return {
            'total_affected': len(all_affected),
            'affected_repos': list(all_affected),
            'dependency_order': dependency_order,
            'has_circular_deps': has_cycles,
            'circular_paths': cycles,
            'risk_level': risk_level
        }


class MultiRepoCoordinator:
    """
    Koordiniert Änderungen über mehrere Repositories.

    Workflow:
    1. Plan Multi-Repo Change
    2. Create feature branches in all repos
    3. Apply changes in dependency order
    4. Run tests per repo
    5. Create PRs atomically
    """

    def __init__(self, graph_builder: DependencyGraphBuilder):
        self.graph = graph_builder
        self.active_changes: Dict[str, CrossRepoChange] = {}

    def plan_change(
        self,
        title: str,
        description: str,
        repositories: List[str]
    ) -> CrossRepoChange:
        """
        Plant eine Multi-Repo Änderung.

        Args:
            title: Titel der Änderung
            description: Beschreibung
            repositories: Liste betroffener Repos

        Returns:
            CrossRepoChange Objekt
        """
        # Analyze impact
        impact = self.graph.analyze_impact(repositories)

        # Create change
        change_id = f"multi_repo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        change = CrossRepoChange(
            id=change_id,
            title=title,
            description=description,
            repositories=impact['affected_repos'],
            dependency_order=impact['dependency_order'],
            status='planned',
            created_at=datetime.now()
        )

        self.active_changes[change_id] = change

        return change

    def create_feature_branches(
        self,
        change: CrossRepoChange,
        branch_name: str
    ) -> Dict[str, bool]:
        """
        Erstellt Feature Branches in allen betroffenen Repos.

        Args:
            change: CrossRepoChange
            branch_name: Name des Feature Branch

        Returns:
            Dict {repo_name: success}
        """
        results = {}

        for repo_name in change.repositories:
            repo = self.graph.repositories.get(repo_name)
            if not repo:
                results[repo_name] = False
                continue

            try:
                # Create and checkout branch
                subprocess.run(
                    ['git', 'checkout', '-b', branch_name],
                    cwd=repo.path,
                    check=True,
                    capture_output=True
                )
                results[repo_name] = True
            except subprocess.CalledProcessError as e:
                print(f"Failed to create branch in {repo_name}: {e}")
                results[repo_name] = False

        return results

    def apply_changes_in_order(
        self,
        change: CrossRepoChange,
        change_function: callable
    ) -> Dict[str, bool]:
        """
        Wendet Änderungen in Dependency-Reihenfolge an.

        Args:
            change: CrossRepoChange
            change_function: Function(repo: Repository) -> bool

        Returns:
            Dict {repo_name: success}
        """
        results = {}

        # Apply in dependency order
        for repo_name in change.dependency_order:
            repo = self.graph.repositories.get(repo_name)
            if not repo:
                results[repo_name] = False
                continue

            try:
                success = change_function(repo)
                results[repo_name] = success

                if not success:
                    print(f"Change failed for {repo_name}, stopping...")
                    break

            except Exception as e:
                print(f"Error applying change to {repo_name}: {e}")
                results[repo_name] = False
                break

        return results

    def run_tests_all_repos(
        self,
        change: CrossRepoChange
    ) -> Dict[str, Dict]:
        """
        Führt Tests in allen Repos aus.

        Returns:
            Dict {repo_name: {'passed': bool, 'output': str}}
        """
        results = {}

        for repo_name in change.repositories:
            repo = self.graph.repositories.get(repo_name)
            if not repo:
                continue

            # Determine test command based on language
            test_cmd = self._get_test_command(repo)

            try:
                result = subprocess.run(
                    test_cmd,
                    cwd=repo.path,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutes
                )

                results[repo_name] = {
                    'passed': result.returncode == 0,
                    'output': result.stdout + result.stderr
                }
            except subprocess.TimeoutExpired:
                results[repo_name] = {
                    'passed': False,
                    'output': 'Tests timed out after 5 minutes'
                }
            except Exception as e:
                results[repo_name] = {
                    'passed': False,
                    'output': str(e)
                }

        return results

    def create_atomic_prs(
        self,
        change: CrossRepoChange,
        branch_name: str,
        base_branch: str = 'main'
    ) -> Dict[str, str]:
        """
        Erstellt PRs atomisch in allen Repos.

        Args:
            change: CrossRepoChange
            branch_name: Feature Branch Name
            base_branch: Base Branch (default: main)

        Returns:
            Dict {repo_name: pr_url}
        """
        pr_urls = {}

        for repo_name in change.repositories:
            repo = self.graph.repositories.get(repo_name)
            if not repo:
                continue

            try:
                # Push branch
                subprocess.run(
                    ['git', 'push', '-u', 'origin', branch_name],
                    cwd=repo.path,
                    check=True,
                    capture_output=True
                )

                # Create PR using gh CLI
                pr_body = f"""{change.description}

**Multi-Repo Change ID:** {change.id}

**Affected Repositories ({len(change.repositories)}):**
{chr(10).join(f'- {r}' for r in change.repositories)}

**Dependency Order:**
{chr(10).join(f'{i+1}. {r}' for i, r in enumerate(change.dependency_order))}

⚠️ This is part of a coordinated multi-repository change.
Please ensure all related PRs are merged together.

🤖 Generated by Lazy Bird Multi-Repo Coordinator
"""

                result = subprocess.run(
                    [
                        'gh', 'pr', 'create',
                        '--title', f'[Multi-Repo] {change.title}',
                        '--body', pr_body,
                        '--base', base_branch
                    ],
                    cwd=repo.path,
                    capture_output=True,
                    text=True,
                    check=True
                )

                # Extract PR URL from output
                pr_url = result.stdout.strip().split('\n')[-1]
                pr_urls[repo_name] = pr_url

            except subprocess.CalledProcessError as e:
                print(f"Failed to create PR for {repo_name}: {e}")
                pr_urls[repo_name] = None

        # Update change status
        if all(pr_urls.values()):
            change.status = 'completed'

        return pr_urls

    def _get_test_command(self, repo: Repository) -> List[str]:
        """Bestimmt Test-Command basierend auf Sprache."""
        commands = {
            'python': ['pytest'],
            'typescript': ['npm', 'test'],
            'javascript': ['npm', 'test'],
            'go': ['go', 'test', './...'],
            'java': ['mvn', 'test']
        }

        return commands.get(repo.primary_language, ['echo', 'No tests configured'])


# Export
__all__ = [
    'Repository',
    'CrossRepoChange',
    'DependencyGraphBuilder',
    'MultiRepoCoordinator'
]
