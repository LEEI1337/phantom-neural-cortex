# ADR-009: Multi-Repository Coordination

**Status:** Accepted
**Date:** 2025-11-09
**Decision Makers:** Phantom Neural Cortex Team
**Related:** Phase C Advanced Features #1

## Context

Current system operates within single repositories, but real-world projects often span multiple interdependent repositories:

- **Monorepo structures:** Multiple packages/services in one repo
- **Polyrepo architectures:** Core library + multiple consumer applications
- **Cross-repo dependencies:** Changes in library repo affect consumer repos
- **Atomic consistency requirement:** Cannot update library without updating consumers
- **Manual coordination overhead:** Currently requires human intervention to coordinate multi-repo changes

**Problems with current approach:**
- Cannot make changes that require updating multiple repos atomically
- Risk of breaking changes deployed to production
- Library version mismatches between repos
- No systematic way to validate cross-repo compatibility
- Feature work spanning multiple repos impossible to automate

**Examples requiring multi-repo coordination:**
1. Shared library version bump: Update in lib → Update in 3 consumer projects
2. Breaking API change: Modify interface → Update all 5 dependent codebases
3. Monorepo refactor: Move code → Update imports in 20 files across 3 packages
4. Critical security fix: Patch vulnerability → Deploy to 4 deployed services

## Decision

Implement a **Multi-Repository Coordination System** that:
1. Maps dependency graphs between repositories (NetworkX)
2. Plans atomic multi-repo changes (dependency analysis)
3. Validates cross-repo compatibility before merging
4. Creates coordinated pull requests across repositories
5. Tracks deployment status across repos

### Architecture

**Dependency Graph Modeling:**

```python
class RepositoryDependencyGraph:
    """Model repository and inter-repository dependencies"""

    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph: A depends on B → edge A → B

    def add_repository(self, repo_name: str, repo_path: str, repo_type: str):
        """Add repository as node"""
        self.graph.add_node(repo_name, {
            'path': repo_path,
            'type': repo_type,  # "library" | "service" | "consumer" | "monorepo"
            'package_manager': detect_package_manager(repo_path),
        })

    def add_dependency(self, from_repo: str, to_repo: str, version: str = "any"):
        """Add edge: from_repo depends on to_repo"""
        self.graph.add_edge(from_repo, to_repo, {'version': version})

    def build_from_manifest(self, repos: List[str]) -> None:
        """Auto-detect dependencies from package.json, go.mod, pyproject.toml, etc"""
        for repo in repos:
            self.add_repository(repo, get_path(repo), detect_type(repo))

        # Parse all package files
        for repo in repos:
            deps = extract_dependencies(repo)  # From package.json/go.mod/etc
            for dep_repo, version in deps.items():
                if dep_repo in repos:  # Internal dependency
                    self.add_dependency(repo, dep_repo, version)

    def get_dependents(self, repo: str) -> List[str]:
        """Get all repos that depend on this repo"""
        return list(self.graph.predecessors(repo))

    def get_dependencies(self, repo: str) -> List[str]:
        """Get all repos this repo depends on"""
        return list(self.graph.successors(repo))

    def get_transitive_dependents(self, repo: str) -> Set[str]:
        """Get all repos transitively affected by changes to this repo"""
        # BFS from repo backwards through edges
        affected = set()
        queue = [repo]
        while queue:
            current = queue.pop(0)
            for dependent in self.get_dependents(current):
                if dependent not in affected:
                    affected.add(dependent)
                    queue.append(dependent)
        return affected

    def validate_dependency_versions(self) -> List[str]:
        """Validate that all repos can coexist with compatible versions"""
        issues = []
        for repo in self.graph.nodes:
            for dep_repo in self.get_dependencies(repo):
                required_version = self.graph[repo][dep_repo].get('version')
                available_version = get_available_version(dep_repo)

                if not version_compatible(available_version, required_version):
                    issues.append(
                        f"{repo} requires {dep_repo}@{required_version}, "
                        f"but {available_version} available"
                    )
        return issues
```

**Change Impact Analysis:**

```python
class ChangeImpactAnalyzer:
    """Analyze what repos are affected by proposed changes"""

    def __init__(self, graph: RepositoryDependencyGraph):
        self.graph = graph

    def analyze_change(self, changed_repo: str,
                      changed_files: List[str]) -> ChangeImpact:
        """Determine impact of changes to a repo"""

        # Analyze what was changed
        api_changes = detect_api_changes(changed_repo, changed_files)
        breaking_changes = filter_breaking_changes(api_changes)

        # If no breaking changes, impact is minimal
        if not breaking_changes:
            return ChangeImpact(
                affected_repos=[changed_repo],
                change_type="non_breaking",
                requires_coordination=False
            )

        # Breaking change: find all dependent repos
        dependent_repos = self.graph.get_transitive_dependents(changed_repo)

        # Check if changes are forward-compatible
        compatibility_issues = self._check_forward_compatibility(
            changed_repo, breaking_changes, dependent_repos
        )

        return ChangeImpact(
            affected_repos=[changed_repo] + list(dependent_repos),
            change_type="breaking",
            breaking_changes=breaking_changes,
            compatibility_issues=compatibility_issues,
            requires_coordination=len(compatibility_issues) > 0
        )

    def _check_forward_compatibility(self, source_repo: str,
                                     api_changes: List[str],
                                     dependent_repos: Set[str]) -> List[str]:
        """Check if dependent repos can handle the changes"""
        issues = []

        for dependent in dependent_repos:
            # Check if dependent uses changed APIs
            using_changed_api = check_api_usage(dependent, source_repo, api_changes)

            if using_changed_api:
                issues.append(
                    f"{dependent} uses changed API from {source_repo}: {api_changes}"
                )

        return issues
```

**Multi-Repo Change Planning:**

```python
class MultiRepoChangePlanner:
    """Plan coordinated changes across multiple repositories"""

    def __init__(self, graph: RepositoryDependencyGraph):
        self.graph = graph

    def plan_coordinated_changes(self, initial_change: RepoChange,
                                 target_quality: float = 0.85) -> MultiRepoChangeSet:
        """Plan changes required across all affected repos"""

        # Analyze impact
        impact = ChangeImpactAnalyzer(self.graph).analyze_change(
            initial_change.repo,
            initial_change.changed_files
        )

        if not impact.requires_coordination:
            return MultiRepoChangeSet(
                primary_change=initial_change,
                secondary_changes=[],
                is_atomic=True
            )

        # Plan changes to dependent repos
        secondary_changes = []

        for dependent_repo in impact.affected_repos:
            if dependent_repo == initial_change.repo:
                continue

            change = self._plan_dependent_repo_change(
                dependent_repo,
                initial_change,
                impact.breaking_changes
            )
            secondary_changes.append(change)

        # Topologically sort changes (dependencies first)
        change_order = self._topological_sort_changes(
            [initial_change] + secondary_changes
        )

        return MultiRepoChangeSet(
            primary_change=initial_change,
            secondary_changes=secondary_changes,
            change_order=change_order,
            is_atomic=True,
            requires_manual_review=(len(secondary_changes) > 0)
        )

    def _plan_dependent_repo_change(self, repo: str,
                                    source_change: RepoChange,
                                    breaking_changes: List[str]) -> RepoChange:
        """Plan what changes needed in dependent repo"""

        # Generate change description
        description = f"Update {repo} for {source_change.repo} changes\n\n"
        description += "Breaking changes:\n"
        for change in breaking_changes:
            description += f"- {change}\n"

        return RepoChange(
            repo=repo,
            change_type="dependent_update",
            description=description,
            required_for=[source_change.repo],
            priority="high"
        )

    def _topological_sort_changes(self, changes: List[RepoChange]) -> List[RepoChange]:
        """Order changes so dependencies are updated first"""
        # Build subgraph of just these repos
        subgraph = nx.subgraph(
            self.graph.graph,
            nodes=[c.repo for c in changes]
        )

        # Topological sort (dependencies before dependents)
        sorted_repos = list(nx.topological_sort(subgraph))

        return sorted([c for c in changes],
                     key=lambda c: sorted_repos.index(c.repo))
```

**Atomic Pull Request Creation:**

```python
class AtomicMultiRepoPullRequestCreator:
    """Create coordinated PRs across multiple repositories"""

    def __init__(self, github_client):
        self.gh = github_client

    async def create_coordinated_prs(self,
                                    change_set: MultiRepoChangeSet) -> MultiRepoPullRequest:
        """Create PRs for all repos in change set"""

        pr_info = MultiRepoPullRequest()

        # Create primary PR
        primary_pr = await self._create_single_pr(
            change_set.primary_change,
            pr_info
        )
        pr_info.primary_pr = primary_pr

        # Create secondary PRs with reference to primary
        for secondary_change in change_set.secondary_changes:
            secondary_pr = await self._create_single_pr(
                secondary_change,
                pr_info,
                depends_on=primary_pr
            )
            pr_info.secondary_prs.append(secondary_pr)

        # Create meta-PR (rollup) if multiple repos
        if len(change_set.secondary_changes) > 0:
            meta_pr = await self._create_meta_pr(pr_info)
            pr_info.meta_pr = meta_pr

        return pr_info

    async def _create_single_pr(self, change: RepoChange,
                               context: MultiRepoPullRequest,
                               depends_on: Optional[PR] = None) -> PR:
        """Create single PR with cross-references"""

        branch_name = f"multi-repo/{change.repo}/{context.change_id}"

        pr = await self.gh.create_pull_request(
            repo=change.repo,
            title=change.description.split('\n')[0],
            body=self._format_pr_body(change, context, depends_on),
            branch=branch_name,
            base='main'
        )

        return pr

    def _format_pr_body(self, change: RepoChange,
                       context: MultiRepoPullRequest,
                       depends_on: Optional[PR] = None) -> str:
        """Format PR body with multi-repo context"""

        body = f"{change.description}\n\n"

        if depends_on:
            body += f"**Depends on:** {depends_on.html_url}\n\n"

        body += f"**Part of coordinated change set:** {context.change_id}\n"
        body += f"**Total affected repos:** {context.total_repos()}\n"

        return body
```

### Implementation Details

**File:** `lazy-bird/multi-repo/dependency_analyzer.py`

**Core Classes:**

```python
class MultiRepoOrchestrator:
    """Main orchestrator for multi-repo coordination"""

    def __init__(self, repos: List[str]):
        self.repos = repos
        self.graph = RepositoryDependencyGraph()
        self.impact_analyzer = ChangeImpactAnalyzer(self.graph)
        self.planner = MultiRepoChangePlanner(self.graph)
        self.pr_creator = AtomicMultiRepoPullRequestCreator()

    def initialize(self):
        """Build dependency graph from manifests"""
        self.graph.build_from_manifest(self.repos)

    async def coordinate_change(self, issue: Issue,
                               initial_change: RepoChange) -> MultiRepoPullRequest:
        """Coordinate a single issue across multiple repos"""

        # Analyze impact
        impact = self.impact_analyzer.analyze_change(
            initial_change.repo,
            initial_change.changed_files
        )

        # Plan coordinated changes
        change_set = self.planner.plan_coordinated_changes(initial_change)

        # Create coordinated PRs
        multi_pr = await self.pr_creator.create_coordinated_prs(change_set)

        return multi_pr

    def get_dependency_report(self) -> str:
        """Generate human-readable dependency report"""
        report = "Repository Dependency Graph\n"
        report += "="*50 + "\n\n"

        for repo in self.repos:
            report += f"**{repo}**\n"
            deps = self.graph.get_dependencies(repo)
            if deps:
                report += f"  Dependencies: {', '.join(deps)}\n"
            dependents = self.graph.get_dependents(repo)
            if dependents:
                report += f"  Dependents: {', '.join(dependents)}\n"
            report += "\n"

        return report
```

## Consequences

### Positive

1. **Atomic Multi-Repo Updates:** Safe cross-repo changes
   - Library version bump updates all consumers atomically
   - Breaking API changes coordinated across dependents
   - No partial deployments (either all succeed or all rollback)
   - Prevents version mismatches

2. **Automated Dependency Analysis:** Removes manual coordination
   - Automatic detection of affected repos
   - Prevents missing a dependent repo
   - Saves engineering time (2-4 hours per coordinated change)
   - Reduces human error

3. **Cross-Repo Compatibility Validation:** Early error detection
   - Check if changes are forward-compatible before merging
   - Validate version constraints
   - Prevent breaking changes reaching production
   - Catch issues in code review, not production

4. **Scalable Polyrepo Architecture:** Enables larger systems
   - Can confidently manage 10+ interdependent repositories
   - Systematic approach to cross-repo refactoring
   - Enables feature work spanning multiple repos
   - Supports gradual migration strategies

5. **Audit Trail:** Complete history of coordinated changes
   - Track what changed where and why
   - Linked PRs across repos
   - Easy rollback if needed
   - Compliance/regulatory friendly

### Negative

1. **Complexity of Dependency Analysis:** Hard to model all cases
   - Transitive dependencies tricky (A→B→C)
   - Version constraints complex (^1.0.0 vs ~1.0.0)
   - Different package managers (npm, pip, go, cargo)
   - Manual dependencies not detected
   - **Mitigation:** Conservative assumptions, manual override capability

2. **PR Creation at Scale:** Too many PRs
   - 10 affected repos = 10 PRs to review
   - Coordination overhead
   - Risk of approval getting out of sync
   - **Mitigation:** Meta-PR with status dashboard, batch review

3. **Test Execution Parallelism:** Tests conflict
   - Multiple PRs running tests in parallel
   - Shared test databases/services may conflict
   - Race conditions possible
   - **Mitigation:** Isolated test environments, serial test execution

4. **Rollback Complexity:** Harder to rollback atomically
   - If one PR merges but another doesn't, inconsistent state
   - Coordinated rollback needed across repos
   - Complex manual process
   - **Mitigation:** Meta-PR orchestration, automated rollback

5. **Breaking Change Detection:** Not always automatic
   - Some breaking changes subtle (semantic)
   - May require manual specification
   - False positives cause unnecessary reviews
   - **Mitigation:** Conservative heuristics, developer override

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Incorrect dependency analysis | Medium | High | Validate graph, manual review, unit tests |
| Incomplete change propagation | Low | High | Comprehensive dependency tracing, validation |
| Orphaned PRs if coordination fails | Medium | Medium | Automated cleanup, status monitoring |
| Complex rollback failures | Low | High | Atomic transaction approach, automated recovery |

## Alternatives Considered

### 1. Manual Multi-Repo Coordination
**Rejected Reason:** Error-prone, time-consuming, doesn't scale

### 2. Monorepo (Single Repository)
**Rejected Reason:** May not be feasible, adds operational complexity

### 3. Semantic Versioning Only (No Coordination)
**Rejected Reason:** Doesn't catch bugs, allows version mismatches

### 4. Async Updates (Eventual Consistency)
**Rejected Reason:** Introduces bugs and inconsistencies, hard to debug

## Implementation Status

✅ **Completed:**
- RepositoryDependencyGraph with NetworkX ([dependency_analyzer.py](../../lazy-bird/multi-repo/dependency_analyzer.py))
- ChangeImpactAnalyzer
- MultiRepoChangePlanner with topological sorting
- AtomicMultiRepoPullRequestCreator
- Multi-repo orchestration
- Dependency report generation
- Unit tests ([test_dependency_analyzer.py](../../lazy-bird/tests/test_dependency_analyzer.py))

⏳ **Pending:**
- Production deployment with real polyrepo systems
- Integration with GitHub API for PR creation
- Automated meta-PR creation and management
- Rollback automation

## Validation

**Success Criteria:**
- [x] Dependency graph construction works
- [x] Transitive dependent detection accurate
- [x] Change impact analysis complete
- [ ] Production validation: 10+ multi-repo changes
- [ ] Coordinated PR success rate ≥95%

**Monitoring:**
- Prometheus metric: `lazybird_multi_repo_pr_created_total`
- Metric: `lazybird_multi_repo_change_success_rate_percent`
- Metric: `lazybird_multi_repo_affected_repos_count`

**Example Scenario:**

```
Library Repository: shared-utils
├─ Version: 1.0.0
├─ Exports: Logger, Cache, Queue

Dependent Repositories:
├─ api-service (depends on shared-utils@^1.0.0)
├─ web-ui (depends on shared-utils@^1.0.0)
└─ worker-service (depends on shared-utils@^1.0.0)

Proposed Change:
├─ Rename: Logger.log() → Logger.write()
├─ Impact: Breaking change to API
├─ Affected repos: api-service, web-ui, worker-service

Coordinated Changes:
1. Create PR in shared-utils: Rename method, bump to 1.1.0
2. Create PR in api-service: Update Logger usage
3. Create PR in web-ui: Update Logger usage
4. Create PR in worker-service: Update Logger usage
5. Create meta-PR linking all 4 PRs

Result:
├─ All 4 PRs reviewed together
├─ All 4 PRs merged together
└─ No version mismatches possible
```

## Related Decisions

- **ADR-001:** Latent Reasoning (helps with change analysis)
- **ADR-002:** Iteration Prediction (scales to multi-repo changes)
- **ADR-004:** Deep Supervision (validates each repo change)

## References

- NetworkX: https://networkx.org/
- Dependency management: https://semver.org/
- Multi-repo strategies: https://monorepo.tools/
- Implementation: `lazy-bird/multi-repo/dependency_analyzer.py`
