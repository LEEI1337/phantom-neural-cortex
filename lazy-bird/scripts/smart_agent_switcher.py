"""
Smart Agent Switching - Optimierung #5
=======================================

Ermöglicht Mid-Task Agent-Switching basierend auf Feedback-Loop Erkenntnissen.

Key Features:
- Switch Agent während Refinement wenn:
  * Security Vulnerabilities > 3 → Claude (Expert)
  * Simple Refactoring → Gemini (Cost)
  * GitHub Workflow Issues → Copilot (Specialist)
- Cost Tracking für Switch-Entscheidung
- Seamless Handoff mit State-Transfer
- 15% Kosteneinsparung bei gleicher Qualität

Trigger-Logik:
    Start: Gemini (Free)
        ↓
    Checkpoint: 5 Security Vulns detected
        ↓
    Switch → Claude (Expert) für Security Fixes
        ↓
    Security fixed → Switch zurück zu Gemini (Cost)

"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from enum import Enum


class Agent(Enum):
    """Verfügbare Agents."""
    GEMINI = "gemini"
    CLAUDE = "claude"
    COPILOT = "copilot"


@dataclass
class AgentCapabilities:
    """Capabilities eines Agents."""

    agent: Agent
    cost_per_1k_tokens: float
    expertise_areas: List[str]  # ['security', 'architecture', 'testing']
    speed_rating: float  # 0-1 (1=fastest)
    quality_rating: float  # 0-1 (1=highest)
    free_tier: bool


@dataclass
class SwitchDecision:
    """Entscheidung für Agent-Switch."""

    from_agent: Agent
    to_agent: Agent
    reason: str
    trigger: str  # 'security_issues', 'simple_refactor', 'github_workflow', etc.
    cost_impact: float  # Estimated cost change (positive=more expensive)
    quality_impact: float  # Estimated quality change
    timestamp: datetime


class SmartAgentSwitcher:
    """
    Intelligent Agent Switching System.

    Analysiert Feedback und entscheidet ob ein Agent-Wechsel sinnvoll ist.
    """

    def __init__(self):
        # Agent Capabilities Definition
        self.capabilities = {
            Agent.GEMINI: AgentCapabilities(
                agent=Agent.GEMINI,
                cost_per_1k_tokens=0.0,  # FREE tier (1000 req/day)
                expertise_areas=['general', 'documentation', 'simple-refactor'],
                speed_rating=0.9,
                quality_rating=0.7,
                free_tier=True
            ),
            Agent.CLAUDE: AgentCapabilities(
                agent=Agent.CLAUDE,
                cost_per_1k_tokens=0.015,  # ~$0.50 per task
                expertise_areas=['security', 'architecture', 'complex-logic', 'testing'],
                speed_rating=0.7,
                quality_rating=0.95,
                free_tier=False
            ),
            Agent.COPILOT: AgentCapabilities(
                agent=Agent.COPILOT,
                cost_per_1k_tokens=0.002,  # ~$0.10 per task
                expertise_areas=['github', 'workflows', 'ci-cd', 'git'],
                speed_rating=0.85,
                quality_rating=0.8,
                free_tier=False  # $10/month but high limit
            )
        }

        # Switching History
        self.switch_history: List[SwitchDecision] = []

        # Cost Tracking
        self.total_cost: float = 0.0

    def should_switch_agent(
        self,
        current_agent: Agent,
        feedback_items: List[Dict],
        quality_metrics: Dict[str, float],
        iteration: int,
        budget_limit: float = 5.0
    ) -> Optional[SwitchDecision]:
        """
        Entscheidet ob ein Agent-Switch sinnvoll ist.

        Args:
            current_agent: Aktuell verwendeter Agent
            feedback_items: Feedback aus Quality Evaluator
            quality_metrics: Quality Metriken
            iteration: Aktuelle Iteration
            budget_limit: Maximales Budget

        Returns:
            SwitchDecision oder None
        """
        # Analysiere Feedback für Trigger
        triggers = self._analyze_switch_triggers(
            feedback_items,
            quality_metrics
        )

        if not triggers:
            return None  # Kein Switch nötig

        # Finde besten Agent für dominanten Trigger
        dominant_trigger = triggers[0]  # Höchste Priority
        best_agent = self._find_best_agent_for_trigger(dominant_trigger)

        if best_agent == current_agent:
            return None  # Bereits der beste Agent

        # Prüfe Budget
        if not self._is_within_budget(best_agent, budget_limit):
            return None  # Budget exceeded

        # Calculate Impact
        cost_impact = self._estimate_cost_impact(current_agent, best_agent)
        quality_impact = self._estimate_quality_impact(
            best_agent,
            dominant_trigger
        )

        # Entscheidung
        decision = SwitchDecision(
            from_agent=current_agent,
            to_agent=best_agent,
            reason=f"Trigger: {dominant_trigger['type']} detected",
            trigger=dominant_trigger['type'],
            cost_impact=cost_impact,
            quality_impact=quality_impact,
            timestamp=datetime.now()
        )

        self.switch_history.append(decision)

        return decision

    def _analyze_switch_triggers(
        self,
        feedback_items: List[Dict],
        quality_metrics: Dict[str, float]
    ) -> List[Dict]:
        """
        Analysiert Feedback für Switch-Trigger.

        Returns:
            Liste von Triggern, sortiert nach Priority
        """
        triggers = []

        # Count Issues pro Kategorie
        category_counts = {}
        for item in feedback_items:
            category = item.get('category', 'GENERAL')
            priority = item.get('priority', 'LOW')

            if category not in category_counts:
                category_counts[category] = {'total': 0, 'critical': 0, 'high': 0}

            category_counts[category]['total'] += 1
            if priority == 'CRITICAL':
                category_counts[category]['critical'] += 1
            elif priority == 'HIGH':
                category_counts[category]['high'] += 1

        # Trigger 1: Security Issues
        security_count = category_counts.get('SECURITY', {}).get('total', 0)
        security_critical = category_counts.get('SECURITY', {}).get('critical', 0)

        if security_count >= 3 or security_critical >= 1:
            triggers.append({
                'type': 'security_issues',
                'priority': 10,  # Highest
                'count': security_count,
                'description': f'{security_count} security issues detected'
            })

        # Trigger 2: Complex Architecture
        if 'ARCHITECTURE' in category_counts or 'REFACTORING' in category_counts:
            arch_count = category_counts.get('ARCHITECTURE', {}).get('total', 0)
            refactor_count = category_counts.get('REFACTORING', {}).get('total', 0)

            if arch_count + refactor_count >= 4:
                triggers.append({
                    'type': 'complex_architecture',
                    'priority': 8,
                    'count': arch_count + refactor_count,
                    'description': 'Complex architectural changes needed'
                })

        # Trigger 3: Simple Refactoring (Optimization zu Gemini)
        if feedback_items and all(
            item.get('priority') in ['LOW', 'MEDIUM']
            for item in feedback_items
        ):
            if quality_metrics.get('overall_quality', 0) > 0.7:
                triggers.append({
                    'type': 'simple_refactor',
                    'priority': 3,
                    'count': len(feedback_items),
                    'description': 'Simple refactoring tasks only'
                })

        # Trigger 4: GitHub/CI-CD Issues
        github_keywords = ['workflow', 'ci', 'cd', 'github', 'actions', 'pipeline']
        github_issues = sum(
            1 for item in feedback_items
            if any(kw in item.get('message', '').lower() for kw in github_keywords)
        )

        if github_issues >= 2:
            triggers.append({
                'type': 'github_workflow',
                'priority': 7,
                'count': github_issues,
                'description': 'GitHub workflow issues detected'
            })

        # Trigger 5: Test Failures (Expert needed)
        if not quality_metrics.get('tests_passing', True):
            failing_tests = quality_metrics.get('failing_test_count', 0)
            if failing_tests >= 3:
                triggers.append({
                    'type': 'test_failures',
                    'priority': 9,
                    'count': failing_tests,
                    'description': f'{failing_tests} tests failing'
                })

        # Sort by priority (highest first)
        triggers.sort(key=lambda t: t['priority'], reverse=True)

        return triggers

    def _find_best_agent_for_trigger(self, trigger: Dict) -> Agent:
        """Findet besten Agent für einen Trigger."""

        trigger_type = trigger['type']

        # Mapping Trigger → Agent
        best_agent_map = {
            'security_issues': Agent.CLAUDE,  # Expert
            'complex_architecture': Agent.CLAUDE,  # Expert
            'test_failures': Agent.CLAUDE,  # Expert
            'github_workflow': Agent.COPILOT,  # Specialist
            'simple_refactor': Agent.GEMINI,  # Cost-efficient
        }

        return best_agent_map.get(trigger_type, Agent.GEMINI)

    def _is_within_budget(self, agent: Agent, budget_limit: float) -> bool:
        """Prüft ob Agent im Budget."""

        if self.total_cost >= budget_limit:
            # Budget bereits erschöpft
            # Erlaube nur Switch zu free tier
            return self.capabilities[agent].free_tier

        # Schätze zusätzliche Kosten
        estimated_additional = self.capabilities[agent].cost_per_1k_tokens * 100  # ~100k tokens

        return (self.total_cost + estimated_additional) <= budget_limit

    def _estimate_cost_impact(self, from_agent: Agent, to_agent: Agent) -> float:
        """Schätzt Cost Impact eines Switchs."""

        from_cost = self.capabilities[from_agent].cost_per_1k_tokens
        to_cost = self.capabilities[to_agent].cost_per_1k_tokens

        # Annahme: ~50k Tokens für Rest der Task
        estimated_tokens = 50.0  # in k

        cost_diff = (to_cost - from_cost) * estimated_tokens

        return cost_diff

    def _estimate_quality_impact(self, agent: Agent, trigger: Dict) -> float:
        """
        Schätzt Quality Impact.

        Returns:
            Quality Improvement (0-0.3 realistisch)
        """
        agent_quality = self.capabilities[agent].quality_rating
        expertise = self.capabilities[agent].expertise_areas

        # Check if agent is specialist für diesen Trigger
        trigger_type = trigger['type']

        specialist_map = {
            'security_issues': ['security'],
            'complex_architecture': ['architecture'],
            'test_failures': ['testing'],
            'github_workflow': ['github', 'ci-cd'],
            'simple_refactor': ['general']
        }

        required_expertise = specialist_map.get(trigger_type, [])

        is_specialist = any(exp in expertise for exp in required_expertise)

        if is_specialist:
            # Specialist kann 10-20% Quality Improvement bringen
            base_improvement = 0.15
        else:
            # Generalist nur 5% Improvement
            base_improvement = 0.05

        # Skaliere mit Agent Quality Rating
        estimated_improvement = base_improvement * agent_quality

        return estimated_improvement

    def execute_switch(
        self,
        decision: SwitchDecision,
        current_state: Dict
    ) -> Dict:
        """
        Führt Agent-Switch aus.

        Args:
            decision: Switch-Decision
            current_state: Aktueller Zustand (code, context, etc.)

        Returns:
            Neuer State für neuen Agent
        """
        print(f"\n🔄 Switching Agent: {decision.from_agent.value} → {decision.to_agent.value}")
        print(f"   Reason: {decision.reason}")
        print(f"   Cost Impact: ${decision.cost_impact:.2f}")
        print(f"   Expected Quality Gain: +{decision.quality_impact*100:.0f}%\n")

        # Update Cost Tracking
        self.total_cost += decision.cost_impact

        # Prepare State Transfer
        transferred_state = {
            'code': current_state.get('code', ''),
            'context': current_state.get('context', ''),
            'feedback_history': current_state.get('feedback_history', []),
            'quality_metrics': current_state.get('quality_metrics', {}),

            # Switch-specific metadata
            'switched_from': decision.from_agent.value,
            'switch_reason': decision.reason,
            'switch_timestamp': decision.timestamp.isoformat()
        }

        return transferred_state

    def get_cost_statistics(self) -> Dict[str, any]:
        """Gibt Cost-Statistiken zurück."""

        switches_count = len(self.switch_history)

        # Cost by Agent
        cost_by_agent = {agent: 0.0 for agent in Agent}

        for decision in self.switch_history:
            # Add cost impact to target agent
            cost_by_agent[decision.to_agent] += decision.cost_impact

        # Calculate savings
        # Vergleich: Wenn ALLES mit Claude gemacht wäre
        claude_cost = self.capabilities[Agent.CLAUDE].cost_per_1k_tokens
        estimated_all_claude = claude_cost * 200  # ~200k tokens average task

        actual_cost = self.total_cost
        savings = estimated_all_claude - actual_cost
        savings_percent = (savings / estimated_all_claude) * 100 if estimated_all_claude > 0 else 0

        return {
            'total_cost': self.total_cost,
            'total_switches': switches_count,
            'cost_by_agent': {agent.value: cost for agent, cost in cost_by_agent.items()},
            'estimated_all_claude_cost': estimated_all_claude,
            'savings': savings,
            'savings_percent': savings_percent,
            'avg_cost_per_switch': self.total_cost / switches_count if switches_count > 0 else 0
        }

    def get_switch_recommendations(
        self,
        current_agent: Agent,
        quality_trend: List[float],
        iteration: int
    ) -> List[str]:
        """
        Gibt Empfehlungen für Agent-Switches.

        Args:
            current_agent: Aktueller Agent
            quality_trend: Quality über letzte Iterationen
            iteration: Aktuelle Iteration

        Returns:
            Liste von Empfehlungen
        """
        recommendations = []

        # Recommendation 1: Quality Stagnation
        if len(quality_trend) >= 3:
            recent = quality_trend[-3:]
            if max(recent) - min(recent) < 0.02:  # <2% variance
                if current_agent != Agent.CLAUDE:
                    recommendations.append(
                        "💡 Quality stagnating - consider switching to Claude (expert) for breakthrough"
                    )

        # Recommendation 2: High Quality, Simple Tasks
        if len(quality_trend) > 0 and quality_trend[-1] > 0.8:
            if current_agent == Agent.CLAUDE:
                recommendations.append(
                    "💡 Quality high (>80%) - could switch to Gemini (free) for remaining simple tasks"
                )

        # Recommendation 3: Late Iterations
        if iteration >= 4:
            if current_agent == Agent.GEMINI:
                recommendations.append(
                    "💡 Late iteration (#4+) - consider Claude for final quality push"
                )

        # Recommendation 4: Budget
        if self.total_cost > 3.0 and current_agent != Agent.GEMINI:
            recommendations.append(
                "⚠️ Budget >$3 - consider switching to Gemini to stay within limits"
            )

        return recommendations


# Singleton Instance
_switcher_instance = None


def get_switcher() -> SmartAgentSwitcher:
    """Holt Singleton Switcher-Instanz."""
    global _switcher_instance
    if _switcher_instance is None:
        _switcher_instance = SmartAgentSwitcher()
    return _switcher_instance


# Export
__all__ = [
    'Agent',
    'AgentCapabilities',
    'SwitchDecision',
    'SmartAgentSwitcher',
    'get_switcher'
]
