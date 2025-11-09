"""
GitHub Spec-Kit Orchestrator - PHASE E Integration
===================================================

Integriert GitHub Spec-Kit Framework mit UltraThink-optimiertem Lazy Bird System.
Kombiniert Spec-Driven Development mit ML-basierten Optimierungen.

Key Features:
- Constitution-basierte Projektgovernance
- Spec → Plan → Tasks → Implement Pipeline
- Integration mit RL Refinement Chain
- Smart Agent Switching während Spec-Kit Workflow
- Latent Reasoning für große Spezifikationen
- Dashboard-Integration für Echtzeit-Monitoring

Architecture:
  Spec-Kit Layer (oberste Ebene)
      ↓
  UltraThink Optimizations (ML, RL, Caching)
      ↓
  Multi-Agent Execution (Gemini, Claude, Copilot)

Use Case: Enterprise-grade Spec-Driven Development mit AI-Optimierung
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import subprocess
import re


class SpecKitPhase(Enum):
    """Spec-Kit Workflow Phasen."""
    CONSTITUTION = "constitution"
    SPECIFY = "specify"
    CLARIFY = "clarify"
    PLAN = "plan"
    ANALYZE = "analyze"
    TASKS = "tasks"
    IMPLEMENT = "implement"


@dataclass
class SpecKitConfig:
    """Konfiguration für Spec-Kit Integration."""

    project_name: str
    project_path: Path
    ai_agent: str = "claude"  # claude, gemini, copilot, cursor, windsurf

    # UltraThink Optimizations
    enable_latent_reasoning: bool = True
    enable_rl_refinement: bool = True
    enable_smart_switching: bool = True
    enable_parallel_eval: bool = True
    enable_ml_iteration_prediction: bool = True

    # Spec-Kit Directories
    specify_dir: Path = None
    memory_dir: Path = None
    specs_dir: Path = None
    scripts_dir: Path = None
    templates_dir: Path = None

    def __post_init__(self):
        """Initialize directory paths."""
        if self.specify_dir is None:
            self.specify_dir = self.project_path / ".specify"
        self.memory_dir = self.specify_dir / "memory"
        self.specs_dir = self.specify_dir / "specs"
        self.scripts_dir = self.specify_dir / "scripts"
        self.templates_dir = self.specify_dir / "templates"


@dataclass
class FeatureSpec:
    """Eine Feature-Spezifikation im Spec-Kit Format."""

    feature_id: str
    name: str
    description: str

    # Spec-Kit Artifacts
    constitution: Optional[str] = None
    specification: Optional[str] = None
    plan: Optional[str] = None
    tasks: Optional[List[Dict]] = None

    # UltraThink Enhancements
    estimated_iterations: Optional[int] = None
    optimal_agent: Optional[str] = None
    complexity_score: Optional[float] = None
    latent_state: Optional[Dict] = None

    # Status
    current_phase: SpecKitPhase = SpecKitPhase.CONSTITUTION
    completed_phases: List[SpecKitPhase] = None

    def __post_init__(self):
        if self.completed_phases is None:
            self.completed_phases = []


class SpecKitOrchestrator:
    """
    Orchestriert GitHub Spec-Kit Workflow mit UltraThink-Optimierungen.

    Integration Points:
    1. Constitution → Feedbackloop Guidelines Integration
    2. Specify → Latent Reasoning Compression
    3. Plan → ML Iteration Prediction
    4. Tasks → RL-basierte Task Priorisierung
    5. Implement → Smart Agent Switching + Parallel Evaluation
    """

    def __init__(self, config: SpecKitConfig):
        self.config = config
        self.features: Dict[str, FeatureSpec] = {}

        # Initialize Spec-Kit structure
        self._initialize_speckit_structure()

        # Load UltraThink components
        if config.enable_latent_reasoning:
            from feedback.latent_reasoning import LatentReasoningEncoder, LatentReasoningDecoder
            self.latent_encoder = LatentReasoningEncoder(embedding_dim=512)
            self.latent_decoder = LatentReasoningDecoder(embedding_dim=512)

        if config.enable_ml_iteration_prediction:
            from ml.iteration_predictor import IterationPredictor
            self.iteration_predictor = IterationPredictor()

        if config.enable_rl_refinement:
            from ml.rl_refinement_chain import RLRefinementChain, SimplePPOAgent
            agent = SimplePPOAgent(state_dim=20, action_dim=8)
            self.rl_chain = RLRefinementChain(agent=agent, target_quality=85.0)

        if config.enable_smart_switching:
            # Agent switcher for optimal agent selection
            self.agent_costs = {
                "gemini": 0.001,   # $0.001 per 1k tokens
                "claude": 0.008,   # $0.008 per 1k tokens
                "copilot": 0.004,  # $0.004 per 1k tokens
            }

    def _initialize_speckit_structure(self):
        """Erstellt .specify/ Verzeichnisstruktur."""
        # Create directories
        for directory in [
            self.config.memory_dir,
            self.config.specs_dir,
            self.config.scripts_dir,
            self.config.templates_dir
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        # Create setup scripts
        self._create_setup_scripts()

        # Create templates
        self._create_templates()

    def _create_setup_scripts(self):
        """Erstellt Shell-Skripte für Spec-Kit Workflow."""

        # check-prerequisites.sh
        prereq_script = self.config.scripts_dir / "check-prerequisites.sh"
        prereq_script.write_text("""#!/bin/bash
# Check prerequisites for Spec-Kit + UltraThink

echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ required"
    exit 1
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git required"
    exit 1
fi

# Check UltraThink dependencies
python3 -c "import numpy, sklearn, networkx" 2>/dev/null || {
    echo "❌ UltraThink dependencies missing. Run: pip install -r requirements.txt"
    exit 1
}

echo "✓ All prerequisites met"
""")
        prereq_script.chmod(0o755)

        # create-new-feature.sh
        feature_script = self.config.scripts_dir / "create-new-feature.sh"
        feature_script.write_text("""#!/bin/bash
# Create new feature with UltraThink optimization analysis

FEATURE_ID=$1

if [ -z "$FEATURE_ID" ]; then
    echo "Usage: ./create-new-feature.sh <FEATURE_ID>"
    exit 1
fi

FEATURE_DIR=".specify/specs/$FEATURE_ID"
mkdir -p "$FEATURE_DIR/contracts"

# Create spec files from templates
cp .specify/templates/spec-template.md "$FEATURE_DIR/spec.md"
cp .specify/templates/plan-template.md "$FEATURE_DIR/plan.md"
cp .specify/templates/tasks-template.md "$FEATURE_DIR/tasks.md"

# Initialize with UltraThink analysis
python3 -m lazy-bird.speckit.analyze_feature "$FEATURE_ID"

echo "✓ Feature $FEATURE_ID created with UltraThink optimization"
""")
        feature_script.chmod(0o755)

    def _create_templates(self):
        """Erstellt Spec-Kit Templates mit UltraThink-Erweiterungen."""

        # spec-template.md
        spec_template = self.config.templates_dir / "spec-template.md"
        spec_template.write_text("""# Feature Specification: [FEATURE_NAME]

## Overview
[High-level description of what this feature does and why it's needed]

## User Stories

### Story 1: [User Action]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

## UltraThink Analysis

**Estimated Complexity:** [Auto-generated by ML]
**Recommended Agent:** [Auto-selected: Gemini/Claude/Copilot]
**Predicted Iterations:** [ML-predicted: 2-10]
**Quality Target:** [85%+ overall]

## Requirements
1. Functional requirement 1
2. Functional requirement 2

## Non-Functional Requirements
- Performance: [metrics]
- Security: [requirements]
- Accessibility: [standards]

## Out of Scope
- [Items explicitly not included]
""")

        # plan-template.md
        plan_template = self.config.templates_dir / "plan-template.md"
        plan_template.write_text("""# Technical Plan: [FEATURE_NAME]

## Architecture Overview
[High-level architecture diagram and explanation]

## Technology Stack
- **Frontend:** [Technology + rationale]
- **Backend:** [Technology + rationale]
- **Database:** [Technology + rationale]
- **AI Agent:** [Gemini/Claude/Copilot - auto-selected by UltraThink]

## UltraThink Optimization Strategy

**Latent Reasoning:** [Enabled/Disabled]
- Token compression target: 40%
- Large spec compression ratio: 5-10x

**RL Refinement Chain:** [Enabled/Disabled]
- Adaptive strategy learning
- Optimal action sequences

**Smart Agent Switching:** [Enabled/Disabled]
- Agent switches based on task complexity
- Cost optimization via multi-agent strategy

**Parallel Evaluation:** [Enabled/Disabled]
- Concurrent quality checks (tests, security, types)
- 30-40% speed improvement

## Component Breakdown

### Component 1: [Name]
**Responsibility:** [What it does]
**Dependencies:** [Other components]
**UltraThink Agent:** [Optimal agent for this component]

## Data Model
[Schema definitions - can be in data-model.md]

## API Contracts
[API specifications - can be in contracts/api-spec.json]

## Implementation Approach
1. Phase 1: [Description]
2. Phase 2: [Description]

## Testing Strategy
- Unit tests: [Coverage target]
- Integration tests: [Scenarios]
- E2E tests: [User journeys]

## Deployment Strategy
[How this will be deployed - CI/CD, environments, rollout]
""")

        # tasks-template.md
        tasks_template = self.config.templates_dir / "tasks-template.md"
        tasks_template.write_text("""# Implementation Tasks: [FEATURE_NAME]

## Task Breakdown

### Setup & Configuration
- [ ] [P] Setup project structure
- [ ] [P] Install dependencies
- [ ] Configure environment variables

### Backend Development
- [ ] Implement data models
- [ ] Create API endpoints
- [ ] Add authentication/authorization
- [ ] Write unit tests

### Frontend Development
- [ ] Create UI components
- [ ] Implement state management
- [ ] Add API integration
- [ ] Write component tests

### Integration & Testing
- [ ] Integration tests
- [ ] E2E tests
- [ ] Performance testing
- [ ] Security audit

### UltraThink Refinement
- [ ] Run RL-optimized refinement loop
- [ ] Apply deep supervision checkpoints (33%, 66%, 100%)
- [ ] Execute parallel quality evaluation
- [ ] Verify quality targets (85%+)

### Deployment
- [ ] Build production artifacts
- [ ] Deploy to staging
- [ ] Production deployment
- [ ] Post-deployment verification

## Task Dependencies
[Automatically analyzed by UltraThink dependency analyzer]

## Parallel Execution Groups
Tasks marked with [P] can be executed in parallel.

## Estimated Timeline
**Total Iterations (ML-predicted):** [X iterations]
**Expected Duration:** [Y minutes - based on timeframe config]
**Quality Target:** [85%+ overall score]
""")

    # ============================================================
    # Spec-Kit Workflow Methods
    # ============================================================

    def create_feature(
        self,
        feature_id: str,
        name: str,
        description: str
    ) -> FeatureSpec:
        """
        Erstellt neue Feature-Spezifikation mit UltraThink-Analyse.

        Args:
            feature_id: Unique feature identifier (e.g., "auth-system")
            name: Feature name
            description: Brief description

        Returns:
            FeatureSpec mit initialer Analyse
        """
        # Create feature directory
        feature_dir = self.config.specs_dir / feature_id
        feature_dir.mkdir(parents=True, exist_ok=True)
        (feature_dir / "contracts").mkdir(exist_ok=True)

        # Create feature spec
        feature = FeatureSpec(
            feature_id=feature_id,
            name=name,
            description=description
        )

        # UltraThink: Predict complexity and optimal agent
        if self.config.enable_ml_iteration_prediction:
            # Estimate based on description
            from ml.iteration_predictor import TaskComplexity

            complexity = TaskComplexity(
                code_lines=len(description) * 10,  # Rough estimate
                test_count=5,
                file_count=3,
                cyclomatic_complexity=8.0,
                label_complexity=self._estimate_label_complexity(description)
            )

            prediction = self.iteration_predictor.predict_optimal_iterations(complexity)
            feature.estimated_iterations = prediction['predicted_iterations']
            feature.complexity_score = complexity.cyclomatic_complexity

        # UltraThink: Select optimal agent
        if self.config.enable_smart_switching:
            feature.optimal_agent = self._select_optimal_agent(description)

        self.features[feature_id] = feature

        # Save to disk
        self._save_feature(feature)

        print(f"✓ Created feature '{name}' ({feature_id})")
        print(f"  Estimated iterations: {feature.estimated_iterations}")
        print(f"  Optimal agent: {feature.optimal_agent}")
        print(f"  Complexity: {feature.complexity_score:.1f}")

        return feature

    def execute_constitution_phase(
        self,
        feature_id: str,
        constitution_principles: List[str]
    ) -> Dict:
        """
        Phase 1: Constitution - Etabliert Projekt-Prinzipien.

        Integriert mit Lazy Bird Guidelines System.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        # Create constitution
        constitution_text = self._format_constitution(constitution_principles)

        # Save to memory
        constitution_file = self.config.memory_dir / "constitution.md"
        constitution_file.write_text(constitution_text)

        feature.constitution = constitution_text
        feature.current_phase = SpecKitPhase.SPECIFY
        feature.completed_phases.append(SpecKitPhase.CONSTITUTION)

        self._save_feature(feature)

        return {
            'feature_id': feature_id,
            'phase': 'constitution',
            'status': 'completed',
            'principles_count': len(constitution_principles)
        }

    def execute_specify_phase(
        self,
        feature_id: str,
        user_stories: List[Dict],
        requirements: List[str]
    ) -> Dict:
        """
        Phase 2: Specify - Definiert Requirements und User Stories.

        UltraThink: Verwendet Latent Reasoning für große Spezifikationen.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        # Format specification
        spec_text = self._format_specification(user_stories, requirements)

        # UltraThink: Latent Reasoning Compression für große Specs
        if self.config.enable_latent_reasoning and len(spec_text) > 5000:
            print(f"  Applying latent reasoning compression (spec size: {len(spec_text)} chars)")

            # Encode to latent state
            latent_state = self.latent_encoder.encode_code_state(
                code_content=spec_text,
                feedback_items=[],
                quality_metrics={},
                iteration=0
            )

            feature.latent_state = {
                'compression_ratio': latent_state.compression_ratio,
                'original_tokens': latent_state.original_token_count,
                'compressed_tokens': latent_state.compressed_token_count
            }

            print(f"  Compression ratio: {latent_state.compression_ratio:.1f}x")
            print(f"  Token reduction: {latent_state.original_token_count} → {latent_state.compressed_token_count}")

        # Save specification
        spec_file = self.config.specs_dir / feature_id / "spec.md"
        spec_file.write_text(spec_text)

        feature.specification = spec_text
        feature.current_phase = SpecKitPhase.PLAN
        feature.completed_phases.append(SpecKitPhase.SPECIFY)

        self._save_feature(feature)

        return {
            'feature_id': feature_id,
            'phase': 'specify',
            'status': 'completed',
            'user_stories_count': len(user_stories),
            'requirements_count': len(requirements),
            'latent_compression': feature.latent_state if feature.latent_state else None
        }

    def execute_plan_phase(
        self,
        feature_id: str,
        architecture: str,
        tech_stack: Dict[str, str],
        components: List[Dict]
    ) -> Dict:
        """
        Phase 3: Plan - Erstellt technischen Plan.

        UltraThink: ML-basierte Iteration Prediction und Agent Selection.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        # Format plan
        plan_text = self._format_plan(architecture, tech_stack, components, feature)

        # Save plan
        plan_file = self.config.specs_dir / feature_id / "plan.md"
        plan_file.write_text(plan_text)

        feature.plan = plan_text
        feature.current_phase = SpecKitPhase.TASKS
        feature.completed_phases.append(SpecKitPhase.PLAN)

        self._save_feature(feature)

        return {
            'feature_id': feature_id,
            'phase': 'plan',
            'status': 'completed',
            'estimated_iterations': feature.estimated_iterations,
            'optimal_agent': feature.optimal_agent,
            'components_count': len(components)
        }

    def execute_tasks_phase(
        self,
        feature_id: str,
        tasks: List[Dict]
    ) -> Dict:
        """
        Phase 4: Tasks - Generiert Task-Liste.

        UltraThink: RL-basierte Task-Priorisierung.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        # Optimize task order with RL (if enabled)
        if self.config.enable_rl_refinement:
            tasks = self._optimize_task_order_with_rl(tasks)

        # Format tasks
        tasks_text = self._format_tasks(tasks)

        # Save tasks
        tasks_file = self.config.specs_dir / feature_id / "tasks.md"
        tasks_file.write_text(tasks_text)

        feature.tasks = tasks
        feature.current_phase = SpecKitPhase.IMPLEMENT
        feature.completed_phases.append(SpecKitPhase.TASKS)

        self._save_feature(feature)

        return {
            'feature_id': feature_id,
            'phase': 'tasks',
            'status': 'completed',
            'tasks_count': len(tasks),
            'parallel_tasks': sum(1 for t in tasks if t.get('parallel', False))
        }

    def execute_implement_phase(
        self,
        feature_id: str,
        executor_callback: callable
    ) -> Dict:
        """
        Phase 5: Implement - Führt alle Tasks aus.

        UltraThink: Smart Agent Switching + Parallel Evaluation + Deep Supervision.
        """
        feature = self.features.get(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        if not feature.tasks:
            raise ValueError(f"Feature {feature_id} has no tasks defined")

        results = {
            'completed_tasks': [],
            'failed_tasks': [],
            'agent_switches': [],
            'quality_checkpoints': [],
            'total_time': 0.0,
            'total_cost': 0.0
        }

        current_agent = feature.optimal_agent or self.config.ai_agent

        for i, task in enumerate(feature.tasks):
            task_name = task.get('name', f'Task {i+1}')

            print(f"\n[{i+1}/{len(feature.tasks)}] Executing: {task_name}")
            print(f"  Agent: {current_agent}")

            # UltraThink: Smart Agent Switching
            if self.config.enable_smart_switching:
                optimal_agent = self._should_switch_agent(task, current_agent)
                if optimal_agent != current_agent:
                    print(f"  → Switching agent: {current_agent} → {optimal_agent}")
                    results['agent_switches'].append({
                        'from': current_agent,
                        'to': optimal_agent,
                        'task': task_name,
                        'reason': 'Task complexity optimization'
                    })
                    current_agent = optimal_agent

            # Execute task
            try:
                task_result = executor_callback(task, current_agent)
                results['completed_tasks'].append(task_name)
                results['total_time'] += task_result.get('time', 0)
                results['total_cost'] += task_result.get('cost', 0)
            except Exception as e:
                print(f"  ✗ Failed: {e}")
                results['failed_tasks'].append({'task': task_name, 'error': str(e)})

            # UltraThink: Deep Supervision Checkpoints
            progress = (i + 1) / len(feature.tasks)
            if progress >= 0.33 and len([c for c in results['quality_checkpoints'] if c['checkpoint'] == '33%']) == 0:
                checkpoint = self._run_quality_checkpoint('33%', feature_id)
                results['quality_checkpoints'].append(checkpoint)
            elif progress >= 0.66 and len([c for c in results['quality_checkpoints'] if c['checkpoint'] == '66%']) == 0:
                checkpoint = self._run_quality_checkpoint('66%', feature_id)
                results['quality_checkpoints'].append(checkpoint)

        # Final checkpoint
        final_checkpoint = self._run_quality_checkpoint('100%', feature_id)
        results['quality_checkpoints'].append(final_checkpoint)

        feature.completed_phases.append(SpecKitPhase.IMPLEMENT)
        self._save_feature(feature)

        return results

    # ============================================================
    # Helper Methods
    # ============================================================

    def _estimate_label_complexity(self, description: str) -> int:
        """Schätzt Label-Komplexität basierend auf Beschreibung."""
        complexity_keywords = {
            1: ['simple', 'basic', 'easy'],
            2: ['standard', 'normal', 'typical'],
            3: ['moderate', 'medium', 'average'],
            4: ['complex', 'advanced', 'difficult'],
            5: ['very complex', 'critical', 'enterprise']
        }

        description_lower = description.lower()
        for level, keywords in reversed(list(complexity_keywords.items())):
            if any(kw in description_lower for kw in keywords):
                return level

        return 3  # Default: moderate

    def _select_optimal_agent(self, description: str) -> str:
        """Wählt optimalen AI Agent basierend auf Task-Beschreibung."""
        description_lower = description.lower()

        # Security-kritische Tasks → Claude
        if any(kw in description_lower for kw in ['security', 'auth', 'encryption', 'vulnerability']):
            return 'claude'

        # Einfache Refactorings → Gemini (cost-effective)
        if any(kw in description_lower for kw in ['refactor', 'format', 'style', 'lint']):
            return 'gemini'

        # Standard Tasks → Copilot (balanced)
        return 'copilot'

    def _should_switch_agent(self, task: Dict, current_agent: str) -> str:
        """Entscheidet ob Agent-Switch sinnvoll ist."""
        task_desc = task.get('description', '').lower()

        # Security-kritisch → Claude
        if 'security' in task_desc and current_agent != 'claude':
            return 'claude'

        # Einfach → Gemini
        if 'simple' in task_desc and current_agent != 'gemini':
            return 'gemini'

        return current_agent

    def _optimize_task_order_with_rl(self, tasks: List[Dict]) -> List[Dict]:
        """Optimiert Task-Reihenfolge mit RL Agent."""
        # Simplified: In production, use full RL optimization
        # For now, prioritize by estimated impact

        def task_priority(task):
            desc = task.get('description', '').lower()
            if 'critical' in desc or 'security' in desc:
                return 3
            elif 'important' in desc:
                return 2
            else:
                return 1

        return sorted(tasks, key=task_priority, reverse=True)

    def _run_quality_checkpoint(self, checkpoint: str, feature_id: str) -> Dict:
        """Führt Quality Checkpoint aus (Deep Supervision)."""
        print(f"\n  Running quality checkpoint: {checkpoint}")

        # Simplified quality check
        # In production: run actual tests, linters, security scans

        return {
            'checkpoint': checkpoint,
            'timestamp': datetime.now().isoformat(),
            'quality_score': 75.0,  # Mock
            'issues_found': 0,
            'warnings': []
        }

    def _format_constitution(self, principles: List[str]) -> str:
        """Formatiert Constitution Markdown."""
        md = ["# Project Constitution\n"]
        md.append("## Governing Principles\n")
        for i, principle in enumerate(principles, 1):
            md.append(f"{i}. {principle}")
        return "\n".join(md)

    def _format_specification(self, user_stories: List[Dict], requirements: List[str]) -> str:
        """Formatiert Specification Markdown."""
        md = ["# Feature Specification\n"]
        md.append("## User Stories\n")
        for story in user_stories:
            md.append(f"### {story['title']}")
            md.append(f"**As a** {story['as_a']}")
            md.append(f"**I want to** {story['i_want']}")
            md.append(f"**So that** {story['so_that']}\n")

        md.append("## Requirements\n")
        for i, req in enumerate(requirements, 1):
            md.append(f"{i}. {req}")

        return "\n".join(md)

    def _format_plan(self, architecture: str, tech_stack: Dict, components: List[Dict], feature: FeatureSpec) -> str:
        """Formatiert Plan Markdown mit UltraThink-Analyse."""
        md = ["# Technical Plan\n"]
        md.append("## Architecture\n")
        md.append(architecture + "\n")

        md.append("## Technology Stack\n")
        for key, value in tech_stack.items():
            md.append(f"- **{key}:** {value}")

        md.append("\n## UltraThink Optimization\n")
        md.append(f"- **Estimated Iterations:** {feature.estimated_iterations}")
        md.append(f"- **Optimal Agent:** {feature.optimal_agent}")
        md.append(f"- **Complexity Score:** {feature.complexity_score:.1f}")

        md.append("\n## Components\n")
        for comp in components:
            md.append(f"### {comp['name']}")
            md.append(f"{comp.get('description', '')}\n")

        return "\n".join(md)

    def _format_tasks(self, tasks: List[Dict]) -> str:
        """Formatiert Tasks Markdown."""
        md = ["# Implementation Tasks\n"]
        for i, task in enumerate(tasks, 1):
            parallel = "[P] " if task.get('parallel', False) else ""
            md.append(f"- [ ] {parallel}{task['name']}")
        return "\n".join(md)

    def _save_feature(self, feature: FeatureSpec):
        """Speichert Feature-State zu Disk."""
        feature_file = self.config.specs_dir / feature.feature_id / "state.json"
        with open(feature_file, 'w') as f:
            json.dump(asdict(feature), f, indent=2, default=str)


# Export
__all__ = [
    'SpecKitOrchestrator',
    'SpecKitConfig',
    'FeatureSpec',
    'SpecKitPhase'
]
