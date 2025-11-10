# Guidelines Management System - Automated Fine-Tuning

**Version:** 1.0.0
**Status:** ENTERPRISE GRADE - NO COMPROMISES

Das Guidelines Management System ist der **Kern des kontinuierlichen Lernens** - automatische Fehleranalyse, intelligente Updates, Versionskontrolle, flexible Verteilung.

---

## Warum Guidelines statt Model Fine-Tuning?

### Das Problem mit Model Fine-Tuning:

```
Traditional Fine-Tuning:
  ❌ Teuer ($1000+ pro Training)
  ❌ Langsam (Tage/Wochen)
  ❌ Vendor Lock-In
  ❌ Nicht flexibel
  ❌ Schwer zu debuggen
```

### Die Lösung: Guideline Evolution

```
Guidelines Management:
  ✅ Kostenlos (nur Inference)
  ✅ Sofort wirksam (Sekunden)
  ✅ Vendor-agnostisch
  ✅ Hochflexibel
  ✅ Einfach zu debuggen
  ✅ Versioniert und rollback-fähig
```

---

## System Architecture

### Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    GUIDELINES MANAGEMENT HUB                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   ERROR      │  │  GUIDELINE   │  │   VERSION    │          │
│  │  ANALYZER    │→ │  GENERATOR   │→ │   CONTROL    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↓                  ↓                  ↓                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │           GUIDELINE DISTRIBUTION LAYER            │          │
│  └──────────────────────────────────────────────────┘          │
│         ↓          ↓           ↓            ↓                   │
│  ┌──────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐           │
│  │ Claude   │ │ Gemini  │ │ Ollama  │ │ Copilot  │           │
│  │ Layer-2  │ │ Layer-2 │ │ Layer-2 │ │ Layer-2  │           │
│  └──────────┘ └─────────┘ └─────────┘ └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### Components

1. **Error Analyzer** - Analysiert Fehler und Qualitätsprobleme
2. **Guideline Generator** - Generiert verbesserte Guidelines mittels Meta-Agent
3. **Version Control** - Git-ähnliche Versionierung für Guidelines
4. **Distribution Layer** - Verteilt Guidelines an alle Agents
5. **Feedback Loop** - Kontinuierliches Lernen aus Ergebnissen

---

## 1. Error Analysis System

### Automatic Error Detection

```python
# dashboard/backend/guidelines/error_analyzer.py

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlalchemy import select
from models import Task, QualitySnapshot, AgentSwitch
import logging

logger = logging.getLogger(__name__)


@dataclass
class ErrorPattern:
    """Detected error pattern."""
    pattern_type: str  # "low_quality", "agent_switch", "timeout", "validation_error"
    frequency: int  # How often it occurred
    severity: float  # 0.0 - 1.0
    affected_agent: str
    task_types: List[str]
    error_messages: List[str]
    sample_task_ids: List[str]
    first_seen: datetime
    last_seen: datetime


class ErrorAnalyzer:
    """
    Analyzes task execution errors and quality issues.

    Detects patterns in:
    - Low quality outputs
    - Frequent agent switches
    - Timeouts
    - Validation errors
    - Security issues
    """

    def __init__(self, lookback_hours: int = 24):
        self.lookback_hours = lookback_hours

    async def analyze_errors(self, db) -> List[ErrorPattern]:
        """
        Analyze recent errors and detect patterns.

        Returns:
            List of detected error patterns
        """
        patterns = []

        # Analyze low quality outputs
        low_quality_pattern = await self._analyze_low_quality(db)
        if low_quality_pattern:
            patterns.append(low_quality_pattern)

        # Analyze agent switches
        agent_switch_patterns = await self._analyze_agent_switches(db)
        patterns.extend(agent_switch_patterns)

        # Analyze timeouts
        timeout_pattern = await self._analyze_timeouts(db)
        if timeout_pattern:
            patterns.append(timeout_pattern)

        # Analyze validation errors
        validation_patterns = await self._analyze_validation_errors(db)
        patterns.extend(validation_patterns)

        return patterns

    async def _analyze_low_quality(self, db) -> Optional[ErrorPattern]:
        """Detect tasks with consistently low quality scores."""
        cutoff_time = datetime.utcnow() - timedelta(hours=self.lookback_hours)

        # Find tasks with final quality < 0.7
        result = await db.execute(
            select(Task)
            .filter(
                Task.created_at >= cutoff_time,
                Task.final_quality < 0.7,
                Task.status == "completed"
            )
        )
        low_quality_tasks = result.scalars().all()

        if len(low_quality_tasks) < 3:  # Need at least 3 occurrences
            return None

        # Group by agent and task type
        agent_stats = {}
        for task in low_quality_tasks:
            key = (task.assigned_agent, task.task_type)
            if key not in agent_stats:
                agent_stats[key] = []
            agent_stats[key].append(task)

        # Find most affected agent/task_type combo
        most_affected = max(agent_stats.items(), key=lambda x: len(x[1]))
        (agent, task_type), affected_tasks = most_affected

        return ErrorPattern(
            pattern_type="low_quality",
            frequency=len(affected_tasks),
            severity=1.0 - (sum(t.final_quality for t in affected_tasks) / len(affected_tasks)),
            affected_agent=agent,
            task_types=[task_type],
            error_messages=[f"Quality: {t.final_quality:.2f}" for t in affected_tasks[:5]],
            sample_task_ids=[t.id for t in affected_tasks[:5]],
            first_seen=min(t.created_at for t in affected_tasks),
            last_seen=max(t.created_at for t in affected_tasks)
        )

    async def _analyze_agent_switches(self, db) -> List[ErrorPattern]:
        """Detect frequent agent switching patterns."""
        cutoff_time = datetime.utcnow() - timedelta(hours=self.lookback_hours)

        # Find tasks with multiple agent switches
        result = await db.execute(
            select(Task)
            .filter(
                Task.created_at >= cutoff_time,
                Task.agent_switches >= 2
            )
        )
        switch_tasks = result.scalars().all()

        if len(switch_tasks) < 3:
            return []

        # Group by original agent
        patterns = []
        agent_groups = {}
        for task in switch_tasks:
            if task.assigned_agent not in agent_groups:
                agent_groups[task.assigned_agent] = []
            agent_groups[task.assigned_agent].append(task)

        for agent, tasks in agent_groups.items():
            if len(tasks) < 3:
                continue

            patterns.append(ErrorPattern(
                pattern_type="agent_switch",
                frequency=len(tasks),
                severity=min(1.0, sum(t.agent_switches for t in tasks) / (len(tasks) * 5)),
                affected_agent=agent,
                task_types=list(set(t.task_type for t in tasks)),
                error_messages=[f"{t.agent_switches} switches" for t in tasks[:5]],
                sample_task_ids=[t.id for t in tasks[:5]],
                first_seen=min(t.created_at for t in tasks),
                last_seen=max(t.created_at for t in tasks)
            ))

        return patterns

    async def _analyze_timeouts(self, db) -> Optional[ErrorPattern]:
        """Detect timeout patterns."""
        cutoff_time = datetime.utcnow() - timedelta(hours=self.lookback_hours)

        # Find failed tasks with timeout errors
        result = await db.execute(
            select(Task)
            .filter(
                Task.created_at >= cutoff_time,
                Task.status == "failed",
                Task.error_message.like("%timeout%")
            )
        )
        timeout_tasks = result.scalars().all()

        if len(timeout_tasks) < 3:
            return None

        # Most affected agent
        agent_counts = {}
        for task in timeout_tasks:
            agent_counts[task.assigned_agent] = agent_counts.get(task.assigned_agent, 0) + 1

        most_affected_agent = max(agent_counts.items(), key=lambda x: x[1])[0]
        affected_tasks = [t for t in timeout_tasks if t.assigned_agent == most_affected_agent]

        return ErrorPattern(
            pattern_type="timeout",
            frequency=len(affected_tasks),
            severity=0.8,
            affected_agent=most_affected_agent,
            task_types=list(set(t.task_type for t in affected_tasks)),
            error_messages=[t.error_message for t in affected_tasks[:5]],
            sample_task_ids=[t.id for t in affected_tasks[:5]],
            first_seen=min(t.created_at for t in affected_tasks),
            last_seen=max(t.created_at for t in affected_tasks)
        )

    async def _analyze_validation_errors(self, db) -> List[ErrorPattern]:
        """Detect validation error patterns."""
        cutoff_time = datetime.utcnow() - timedelta(hours=self.lookback_hours)

        result = await db.execute(
            select(Task)
            .filter(
                Task.created_at >= cutoff_time,
                Task.status == "failed",
                Task.error_message.like("%validation%")
            )
        )
        validation_tasks = result.scalars().all()

        if len(validation_tasks) < 2:
            return []

        # Group by error message similarity
        patterns = []
        # TODO: Implement error message clustering
        # For now, simple grouping

        return patterns

    def generate_improvement_recommendations(
        self,
        patterns: List[ErrorPattern]
    ) -> Dict[str, List[str]]:
        """
        Generate improvement recommendations based on error patterns.

        Returns:
            Dict mapping agent names to list of recommendations
        """
        recommendations = {}

        for pattern in patterns:
            agent = pattern.affected_agent
            if agent not in recommendations:
                recommendations[agent] = []

            if pattern.pattern_type == "low_quality":
                recommendations[agent].append(
                    f"Improve {pattern.task_types[0]} task quality. "
                    f"Current avg: {1.0 - pattern.severity:.2f}. "
                    f"Add more specific instructions and examples."
                )

            elif pattern.pattern_type == "agent_switch":
                recommendations[agent].append(
                    f"Reduce agent switches for {', '.join(pattern.task_types)}. "
                    f"Strengthen capability assessment or improve initial guidelines."
                )

            elif pattern.pattern_type == "timeout":
                recommendations[agent].append(
                    f"Optimize for faster responses in {', '.join(pattern.task_types)}. "
                    f"Consider breaking down complex tasks or improving prompts."
                )

        return recommendations
```

---

## 2. Guideline Generator System

### Meta-Agent for Guideline Evolution

```python
# dashboard/backend/guidelines/generator.py

from typing import List, Dict
from dataclasses import dataclass
import asyncio
import logging

logger = logging.getLogger(__name__)


@dataclass
class GuidelineUpdate:
    """Proposed guideline update."""
    agent: str
    version: str
    changes: List[str]
    rationale: str
    new_content: str
    affected_sections: List[str]


class GuidelineGenerator:
    """
    Uses meta-agent to generate improved guidelines based on error analysis.

    The meta-agent (Claude Sonnet 4.5) analyzes:
    - Current guidelines
    - Error patterns
    - Successful task examples
    - Failed task examples

    And produces improved guidelines.
    """

    def __init__(self):
        self.meta_agent = "claude"  # Use Claude for guideline generation

    async def generate_improved_guidelines(
        self,
        agent: str,
        current_guideline: str,
        error_patterns: List[ErrorPattern],
        recommendations: List[str],
        sample_tasks: List[Dict]
    ) -> GuidelineUpdate:
        """
        Generate improved guidelines using meta-agent.

        Args:
            agent: Agent name (claude, gemini, ollama, copilot)
            current_guideline: Current Layer-2 guideline content
            error_patterns: Detected error patterns
            recommendations: Improvement recommendations
            sample_tasks: Sample successful and failed tasks

        Returns:
            Proposed guideline update
        """
        # Prepare meta-prompt
        meta_prompt = self._build_meta_prompt(
            agent,
            current_guideline,
            error_patterns,
            recommendations,
            sample_tasks
        )

        # Execute meta-agent
        logger.info(f"Generating improved guidelines for {agent} using meta-agent")

        # Call Claude to generate improved guidelines
        improved_guideline = await self._execute_meta_agent(meta_prompt)

        # Parse response
        changes, rationale, new_content, affected_sections = self._parse_meta_agent_response(
            improved_guideline
        )

        # Generate version number
        version = self._generate_version_number(agent)

        return GuidelineUpdate(
            agent=agent,
            version=version,
            changes=changes,
            rationale=rationale,
            new_content=new_content,
            affected_sections=affected_sections
        )

    def _build_meta_prompt(
        self,
        agent: str,
        current_guideline: str,
        error_patterns: List[ErrorPattern],
        recommendations: List[str],
        sample_tasks: List[Dict]
    ) -> str:
        """Build meta-prompt for guideline generation."""

        # Collect successful examples
        successful_tasks = [t for t in sample_tasks if t["final_quality"] >= 0.85]
        failed_tasks = [t for t in sample_tasks if t["final_quality"] < 0.7]

        prompt = f"""# GUIDELINE EVOLUTION META-TASK

You are an expert AI system designer tasked with improving the Layer-2 guidelines for the **{agent.upper()}** agent.

## Current Guidelines

{current_guideline}

## Detected Error Patterns

{self._format_error_patterns(error_patterns)}

## Improvement Recommendations

{chr(10).join(f"- {rec}" for rec in recommendations)}

## Performance Analysis

**Successful Tasks (Quality ≥ 0.85):**
{self._format_task_examples(successful_tasks[:5])}

**Failed Tasks (Quality < 0.7):**
{self._format_task_examples(failed_tasks[:5])}

## Your Task

Analyze the current guidelines and produce **improved Layer-2 guidelines** that:

1. **Address detected error patterns** - Fix specific issues causing low quality
2. **Maintain successful patterns** - Keep what's working well
3. **Add missing instructions** - Fill gaps revealed by errors
4. **Improve clarity** - Make instructions more precise and actionable
5. **Add examples** - Include concrete examples from successful tasks

## Output Format

Provide your response in this exact format:

### CHANGES
- List specific changes made (bullet points)
- Each change should reference a specific error pattern or recommendation

### RATIONALE
Explain why these changes will improve performance.

### AFFECTED_SECTIONS
- List which sections of the guidelines were modified

### NEW_GUIDELINES
[Complete improved Layer-2 guidelines here]

---

Begin your analysis and guideline improvement now.
"""
        return prompt

    def _format_error_patterns(self, patterns: List[ErrorPattern]) -> str:
        """Format error patterns for prompt."""
        formatted = []
        for i, pattern in enumerate(patterns, 1):
            formatted.append(f"""
**Pattern {i}: {pattern.pattern_type.upper()}**
- Frequency: {pattern.frequency} occurrences
- Severity: {pattern.severity:.2f}/1.0
- Affected Agent: {pattern.affected_agent}
- Task Types: {', '.join(pattern.task_types)}
- Sample Errors: {', '.join(pattern.error_messages[:3])}
- Time Range: {pattern.first_seen.strftime('%Y-%m-%d %H:%M')} to {pattern.last_seen.strftime('%Y-%m-%d %H:%M')}
""")
        return "\n".join(formatted)

    def _format_task_examples(self, tasks: List[Dict]) -> str:
        """Format task examples for prompt."""
        if not tasks:
            return "(No tasks in this category)"

        formatted = []
        for task in tasks:
            formatted.append(f"""
- Task Type: {task['task_type']}
- Quality: {task['final_quality']:.2f}
- Prompt: {task['prompt'][:200]}{'...' if len(task['prompt']) > 200 else ''}
- Output: {task['output'][:200]}{'...' if len(task['output']) > 200 else ''}
""")
        return "\n".join(formatted)

    async def _execute_meta_agent(self, prompt: str) -> str:
        """Execute meta-agent (Claude) to generate guidelines."""
        # Import here to avoid circular dependency
        from orchestration.orchestrator import CLIOrchestrator

        orchestrator = CLIOrchestrator()

        # Create temporary task for meta-agent
        from models import Task
        import uuid

        meta_task = Task(
            id=f"meta_{uuid.uuid4()}",
            project_id="system",
            prompt=prompt,
            task_type="guideline_generation",
            status="pending",
            assigned_agent="claude"
        )

        # Execute with Claude (meta-agent)
        response = await orchestrator._execute_claude(meta_task, "meta_session")

        return response.content

    def _parse_meta_agent_response(self, response: str) -> tuple:
        """Parse meta-agent response."""
        import re

        # Extract sections using regex
        changes_match = re.search(r'### CHANGES\n(.*?)(?=###|$)', response, re.DOTALL)
        rationale_match = re.search(r'### RATIONALE\n(.*?)(?=###|$)', response, re.DOTALL)
        sections_match = re.search(r'### AFFECTED_SECTIONS\n(.*?)(?=###|$)', response, re.DOTALL)
        guidelines_match = re.search(r'### NEW_GUIDELINES\n(.*?)$', response, re.DOTALL)

        changes = []
        if changes_match:
            changes_text = changes_match.group(1).strip()
            changes = [line.strip('- ').strip() for line in changes_text.split('\n') if line.strip().startswith('-')]

        rationale = rationale_match.group(1).strip() if rationale_match else ""

        affected_sections = []
        if sections_match:
            sections_text = sections_match.group(1).strip()
            affected_sections = [line.strip('- ').strip() for line in sections_text.split('\n') if line.strip().startswith('-')]

        new_content = guidelines_match.group(1).strip() if guidelines_match else ""

        return changes, rationale, new_content, affected_sections

    def _generate_version_number(self, agent: str) -> str:
        """Generate semantic version number for guidelines."""
        # TODO: Implement proper version tracking
        from datetime import datetime
        return f"2.{datetime.utcnow().strftime('%Y%m%d')}.0"
```

---

## 3. Version Control System

### Git-Like Versioning for Guidelines

```python
# dashboard/backend/guidelines/version_control.py

from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import hashlib
import logging

logger = logging.getLogger(__name__)


@dataclass
class GuidelineVersion:
    """A specific version of guidelines."""
    agent: str
    version: str
    content: str
    hash: str
    timestamp: datetime
    changes: List[str]
    rationale: str
    author: str  # "meta-agent" or "manual"
    parent_version: Optional[str]
    performance_metrics: Optional[Dict] = None


class GuidelineVersionControl:
    """
    Git-like version control for guidelines.

    Features:
    - Version history
    - Rollback capability
    - Diff generation
    - Branch/merge (future)
    """

    def __init__(self, guidelines_dir: str = "guidelines/versions"):
        self.guidelines_dir = Path(guidelines_dir)
        self.guidelines_dir.mkdir(parents=True, exist_ok=True)

    def commit(self, update: GuidelineUpdate, author: str = "meta-agent") -> GuidelineVersion:
        """
        Commit a new guideline version.

        Args:
            update: Guideline update to commit
            author: Author of the update

        Returns:
            Created version object
        """
        # Get current version as parent
        parent_version = self.get_latest_version(update.agent)

        # Calculate content hash
        content_hash = self._hash_content(update.new_content)

        # Create version object
        version = GuidelineVersion(
            agent=update.agent,
            version=update.version,
            content=update.new_content,
            hash=content_hash,
            timestamp=datetime.utcnow(),
            changes=update.changes,
            rationale=update.rationale,
            author=author,
            parent_version=parent_version.version if parent_version else None
        )

        # Save to disk
        self._save_version(version)

        # Update current symlink
        self._update_current(update.agent, update.version)

        logger.info(f"Committed {update.agent} guidelines v{update.version}")

        return version

    def get_version(self, agent: str, version: str) -> Optional[GuidelineVersion]:
        """Get specific version of guidelines."""
        version_file = self.guidelines_dir / agent / f"{version}.json"

        if not version_file.exists():
            return None

        with open(version_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return GuidelineVersion(**data)

    def get_latest_version(self, agent: str) -> Optional[GuidelineVersion]:
        """Get latest version of guidelines."""
        current_link = self.guidelines_dir / agent / "current.txt"

        if not current_link.exists():
            return None

        with open(current_link, 'r') as f:
            current_version = f.read().strip()

        return self.get_version(agent, current_version)

    def get_history(self, agent: str, limit: int = 10) -> List[GuidelineVersion]:
        """Get version history for agent."""
        agent_dir = self.guidelines_dir / agent

        if not agent_dir.exists():
            return []

        # List all version files
        version_files = sorted(
            agent_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        versions = []
        for version_file in version_files[:limit]:
            with open(version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                versions.append(GuidelineVersion(**data))

        return versions

    def rollback(self, agent: str, target_version: str) -> GuidelineVersion:
        """
        Rollback to previous version.

        Args:
            agent: Agent name
            target_version: Version to rollback to

        Returns:
            Activated version
        """
        version = self.get_version(agent, target_version)

        if not version:
            raise ValueError(f"Version {target_version} not found for {agent}")

        # Update current symlink
        self._update_current(agent, target_version)

        logger.info(f"Rolled back {agent} to version {target_version}")

        return version

    def diff(self, agent: str, version1: str, version2: str) -> Dict:
        """
        Generate diff between two versions.

        Returns:
            Dict with added/removed/modified sections
        """
        v1 = self.get_version(agent, version1)
        v2 = self.get_version(agent, version2)

        if not v1 or not v2:
            raise ValueError("One or both versions not found")

        # Simple line-by-line diff
        lines1 = v1.content.split('\n')
        lines2 = v2.content.split('\n')

        import difflib
        diff = difflib.unified_diff(
            lines1,
            lines2,
            fromfile=f"v{version1}",
            tofile=f"v{version2}",
            lineterm=''
        )

        return {
            "agent": agent,
            "from_version": version1,
            "to_version": version2,
            "diff": '\n'.join(diff)
        }

    def _save_version(self, version: GuidelineVersion):
        """Save version to disk."""
        agent_dir = self.guidelines_dir / version.agent
        agent_dir.mkdir(parents=True, exist_ok=True)

        version_file = agent_dir / f"{version.version}.json"

        # Convert to dict
        version_dict = {
            "agent": version.agent,
            "version": version.version,
            "content": version.content,
            "hash": version.hash,
            "timestamp": version.timestamp.isoformat(),
            "changes": version.changes,
            "rationale": version.rationale,
            "author": version.author,
            "parent_version": version.parent_version,
            "performance_metrics": version.performance_metrics
        }

        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_dict, f, indent=2, ensure_ascii=False)

    def _update_current(self, agent: str, version: str):
        """Update current version pointer."""
        agent_dir = self.guidelines_dir / agent
        agent_dir.mkdir(parents=True, exist_ok=True)

        current_file = agent_dir / "current.txt"

        with open(current_file, 'w') as f:
            f.write(version)

    def _hash_content(self, content: str) -> str:
        """Calculate SHA-256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
```

---

## 4. Distribution Layer

### Flexible Guideline Distribution

```python
# dashboard/backend/guidelines/distribution.py

from typing import Dict, List, Optional
from pathlib import Path
import logging
import asyncio

logger = logging.getLogger(__name__)


class GuidelineDistributor:
    """
    Distributes guidelines to agents dynamically.

    Supports:
    - Per-agent customization
    - Per-project overrides
    - Per-task-type specialization
    - Hot-reload (no restart needed)
    """

    def __init__(self, version_control: GuidelineVersionControl):
        self.vc = version_control
        self.cache = {}  # In-memory cache
        self.overrides = {}  # Project/task-type overrides

    async def get_guideline(
        self,
        agent: str,
        project_id: Optional[str] = None,
        task_type: Optional[str] = None
    ) -> str:
        """
        Get guideline for agent with optional overrides.

        Priority:
        1. Project + Task-Type specific override
        2. Project-specific override
        3. Task-Type specific override
        4. Base guideline (latest version)

        Args:
            agent: Agent name (claude, gemini, ollama, copilot)
            project_id: Optional project ID
            task_type: Optional task type

        Returns:
            Guideline content
        """
        # Check cache first
        cache_key = f"{agent}:{project_id}:{task_type}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Try project + task-type override
        if project_id and task_type:
            override = self._get_override(agent, project_id, task_type)
            if override:
                self.cache[cache_key] = override
                return override

        # Try project-specific override
        if project_id:
            override = self._get_override(agent, project_id, None)
            if override:
                self.cache[cache_key] = override
                return override

        # Try task-type override
        if task_type:
            override = self._get_override(agent, None, task_type)
            if override:
                self.cache[cache_key] = override
                return override

        # Fall back to base guideline
        version = self.vc.get_latest_version(agent)

        if not version:
            raise ValueError(f"No guidelines found for agent: {agent}")

        guideline = version.content
        self.cache[cache_key] = guideline

        return guideline

    def set_override(
        self,
        agent: str,
        guideline: str,
        project_id: Optional[str] = None,
        task_type: Optional[str] = None
    ):
        """
        Set guideline override for specific project/task-type.

        Args:
            agent: Agent name
            guideline: Override guideline content
            project_id: Optional project ID
            task_type: Optional task type
        """
        key = self._override_key(agent, project_id, task_type)
        self.overrides[key] = guideline

        # Clear cache
        self.cache.clear()

        logger.info(f"Set override for {agent} (project={project_id}, task_type={task_type})")

    def remove_override(
        self,
        agent: str,
        project_id: Optional[str] = None,
        task_type: Optional[str] = None
    ):
        """Remove guideline override."""
        key = self._override_key(agent, project_id, task_type)

        if key in self.overrides:
            del self.overrides[key]
            self.cache.clear()
            logger.info(f"Removed override for {agent}")

    def invalidate_cache(self):
        """Invalidate cache (call after version update)."""
        self.cache.clear()
        logger.info("Guideline cache invalidated")

    def _get_override(
        self,
        agent: str,
        project_id: Optional[str],
        task_type: Optional[str]
    ) -> Optional[str]:
        """Get override if exists."""
        key = self._override_key(agent, project_id, task_type)
        return self.overrides.get(key)

    def _override_key(
        self,
        agent: str,
        project_id: Optional[str],
        task_type: Optional[str]
    ) -> str:
        """Generate override key."""
        return f"{agent}:{project_id or '*'}:{task_type or '*'}"


# Global distributor instance
_distributor: Optional[GuidelineDistributor] = None


def get_distributor() -> GuidelineDistributor:
    """Get global distributor instance."""
    global _distributor

    if _distributor is None:
        from guidelines.version_control import GuidelineVersionControl
        vc = GuidelineVersionControl()
        _distributor = GuidelineDistributor(vc)

    return _distributor
```

---

## 5. Automatic Evolution Loop

### Continuous Learning System

```python
# dashboard/backend/guidelines/evolution_loop.py

from guidelines.error_analyzer import ErrorAnalyzer
from guidelines.generator import GuidelineGenerator
from guidelines.version_control import GuidelineVersionControl
from guidelines.distribution import get_distributor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)


class GuidelineEvolutionLoop:
    """
    Automatic guideline evolution loop.

    Runs periodically (e.g., daily) to:
    1. Analyze recent errors
    2. Generate improved guidelines
    3. Version and deploy updates
    """

    def __init__(
        self,
        run_interval_hours: int = 24,
        auto_deploy: bool = False
    ):
        self.analyzer = ErrorAnalyzer(lookback_hours=run_interval_hours)
        self.generator = GuidelineGenerator()
        self.vc = GuidelineVersionControl()
        self.distributor = get_distributor()
        self.run_interval_hours = run_interval_hours
        self.auto_deploy = auto_deploy
        self.scheduler = AsyncIOScheduler()

    def start(self):
        """Start evolution loop."""
        self.scheduler.add_job(
            self.run_evolution_cycle,
            'interval',
            hours=self.run_interval_hours,
            id='guideline_evolution'
        )
        self.scheduler.start()
        logger.info(f"Guideline evolution loop started (interval: {self.run_interval_hours}h)")

    async def run_evolution_cycle(self):
        """Run one complete evolution cycle."""
        logger.info("=== Starting Guideline Evolution Cycle ===")

        async with AsyncSessionLocal() as db:
            # 1. Analyze errors
            logger.info("Step 1: Analyzing errors...")
            error_patterns = await self.analyzer.analyze_errors(db)

            if not error_patterns:
                logger.info("No significant error patterns detected. Skipping evolution.")
                return

            logger.info(f"Detected {len(error_patterns)} error patterns")

            # 2. Generate recommendations
            recommendations = self.analyzer.generate_improvement_recommendations(error_patterns)

            # 3. For each affected agent, generate improved guidelines
            for agent, agent_recommendations in recommendations.items():
                logger.info(f"Step 2: Generating improved guidelines for {agent}...")

                # Get current guideline
                current_version = self.vc.get_latest_version(agent)
                if not current_version:
                    logger.warning(f"No current guidelines for {agent}, skipping")
                    continue

                # Get sample tasks for this agent
                agent_patterns = [p for p in error_patterns if p.affected_agent == agent]
                sample_tasks = await self._get_sample_tasks(db, agent, agent_patterns)

                # Generate improved guidelines
                try:
                    update = await self.generator.generate_improved_guidelines(
                        agent=agent,
                        current_guideline=current_version.content,
                        error_patterns=agent_patterns,
                        recommendations=agent_recommendations,
                        sample_tasks=sample_tasks
                    )

                    logger.info(f"Generated {len(update.changes)} improvements for {agent}")

                    # 4. Version the update
                    logger.info("Step 3: Versioning update...")
                    new_version = self.vc.commit(update, author="meta-agent-auto")

                    logger.info(f"Committed {agent} v{new_version.version}")

                    # 5. Deploy if auto-deploy enabled
                    if self.auto_deploy:
                        logger.info("Step 4: Auto-deploying...")
                        self.distributor.invalidate_cache()
                        logger.info(f"Deployed {agent} v{new_version.version}")
                    else:
                        logger.info("Auto-deploy disabled. Manual approval required.")

                        # Emit event for manual review
                        await self._emit_review_notification(agent, new_version)

                except Exception as e:
                    logger.error(f"Failed to evolve guidelines for {agent}: {e}", exc_info=True)

        logger.info("=== Guideline Evolution Cycle Complete ===")

    async def _get_sample_tasks(self, db, agent: str, patterns: List) -> List[Dict]:
        """Get sample tasks for guideline generation."""
        from sqlalchemy import select, or_
        from models import Task

        # Get sample task IDs from patterns
        sample_ids = []
        for pattern in patterns:
            sample_ids.extend(pattern.sample_task_ids[:3])

        # Fetch tasks
        result = await db.execute(
            select(Task).filter(Task.id.in_(sample_ids))
        )
        tasks = result.scalars().all()

        # Convert to dicts
        return [
            {
                "task_type": t.task_type,
                "prompt": t.prompt,
                "output": t.output or "",
                "final_quality": t.final_quality or 0.0
            }
            for t in tasks
        ]

    async def _emit_review_notification(self, agent: str, version: GuidelineVersion):
        """Emit notification for manual review."""
        # TODO: Implement WebSocket notification
        # await emit_guideline_update_pending(agent, version.version)
        pass


# Global evolution loop instance
_evolution_loop: Optional[GuidelineEvolutionLoop] = None


def get_evolution_loop() -> GuidelineEvolutionLoop:
    """Get global evolution loop instance."""
    global _evolution_loop

    if _evolution_loop is None:
        import os
        auto_deploy = os.getenv("GUIDELINES_AUTO_DEPLOY", "false").lower() == "true"
        interval_hours = int(os.getenv("GUIDELINES_EVOLUTION_INTERVAL_HOURS", "24"))

        _evolution_loop = GuidelineEvolutionLoop(
            run_interval_hours=interval_hours,
            auto_deploy=auto_deploy
        )

    return _evolution_loop
```

Fortsetzung folgt mit Ollama CLI Integration...
