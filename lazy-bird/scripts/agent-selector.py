#!/usr/bin/env python3
"""
Agent Selector - Intelligent AI agent routing for cost optimization

Selects the appropriate AI agent (Claude, Gemini, Copilot) based on:
- GitHub issue labels
- Project configuration defaults
- Cost optimization rules
- Agent capabilities

Cost Strategy:
    - Gemini (FREE): 60-70% of tasks - bulk operations, docs, large-scale
    - Copilot (FREE/$10): 20-30% of tasks - GitHub workflows, quick fixes
    - Claude ($20): 10-20% of tasks - security, architecture, complex debugging
"""

import json
from typing import List, Dict, Optional
from pathlib import Path


class AgentSelector:
    """Intelligent AI agent selection for cost-optimized task routing."""
    
    # Cost levels for budgeting
    COST_LEVELS = {
        "free": 0,
        "low": 10,
        "high": 20
    }
    
    # Agent capabilities and cost
    AGENTS = {
        "gemini": {
            "cost_level": "free",
            "strengths": ["bulk-operations", "documentation", "large-scale", "analysis"],
            "context_window": 2_000_000,
            "rate_limit": "1000/day"
        },
        "copilot": {
            "cost_level": "low",
            "strengths": ["github-workflow", "quick-fix", "pr-review", "ci-cd"],
            "context_window": 128_000,
            "rate_limit": "2000/month (free), unlimited (pro)"
        },
        "claude": {
            "cost_level": "high",
            "strengths": ["security", "architecture", "complex-debug", "expert-review"],
            "context_window": 200_000,
            "rate_limit": "Pro subscription"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize agent selector with configuration.
        
        Args:
            config_path: Path to rover-mapping.json configuration file
        """
        self.config = self._load_config(config_path)
        self.usage_stats = {
            "gemini": 0,
            "copilot": 0,
            "claude": 0
        }
    
    def select_agent(
        self,
        issue_labels: List[str],
        project_id: str,
        project_type: Optional[str] = None
    ) -> str:
        """
        Select optimal AI agent based on issue labels and project config.
        
        Args:
            issue_labels: List of GitHub issue labels
            project_id: Project identifier for default lookup
            project_type: Optional project type (python, javascript, etc.)
        
        Returns:
            Agent name: "claude", "gemini", or "copilot"
        
        Examples:
            >>> selector = AgentSelector()
            >>> agent = selector.select_agent(["security", "bug"], "my-app")
            >>> print(agent)  # "claude" - security issues need expert
            
            >>> agent = selector.select_agent(["documentation"], "my-app")
            >>> print(agent)  # "gemini" - docs are bulk work, use free tier
            
            >>> agent = selector.select_agent(["github-workflow"], "my-app")
            >>> print(agent)  # "copilot" - GitHub specialist
        """
        # 1. Check label-based rules (highest priority)
        for rule in self.config.get("label_rules", []):
            rule_labels = set(rule["labels"])
            if rule_labels.intersection(set(issue_labels)):
                agent = rule["agent"]
                print(f"Selected {agent} based on label rule: {rule_labels}")
                self._track_usage(agent)
                return agent
        
        # 2. Check project-specific defaults
        project_defaults = self.config.get("project_defaults", {})
        if project_id in project_defaults:
            agent = project_defaults[project_id]
            print(f"Selected {agent} based on project default for {project_id}")
            self._track_usage(agent)
            return agent
        
        # 3. Fallback to cost-optimized default (Gemini free tier)
        fallback = self.config.get("fallback_agent", "gemini")
        print(f"Selected fallback agent: {fallback}")
        self._track_usage(fallback)
        return fallback
    
    def get_agent_info(self, agent_name: str) -> Dict:
        """
        Get detailed information about an AI agent.
        
        Args:
            agent_name: Name of agent (claude, gemini, copilot)
        
        Returns:
            Dictionary with agent capabilities and cost info
        """
        return self.AGENTS.get(agent_name, {})
    
    def estimate_cost(self, agent_name: str, task_count: int = 1) -> float:
        """
        Estimate monthly cost for using specific agent.
        
        Args:
            agent_name: Name of agent
            task_count: Number of tasks per month
        
        Returns:
            Estimated monthly cost in USD
        
        Example:
            >>> cost = selector.estimate_cost("claude", 100)
            >>> print(f"${cost}/month")  # "$20/month" (Pro subscription)
        """
        cost_level = self.AGENTS.get(agent_name, {}).get("cost_level", "free")
        base_cost = self.COST_LEVELS.get(cost_level, 0)
        
        # Gemini and Copilot have usage-based free tiers
        if agent_name == "gemini" and task_count <= 1000:
            return 0.0
        elif agent_name == "copilot" and task_count <= 2000:
            return 0.0
        elif agent_name == "copilot":
            return 10.0
        
        return float(base_cost)
    
    def get_usage_stats(self) -> Dict:
        """
        Get agent usage statistics.
        
        Returns:
            Dictionary with usage counts and percentages
        """
        total = sum(self.usage_stats.values())
        if total == 0:
            return self.usage_stats
        
        stats = {}
        for agent, count in self.usage_stats.items():
            percentage = (count / total) * 100
            stats[agent] = {
                "count": count,
                "percentage": percentage,
                "cost_level": self.AGENTS[agent]["cost_level"]
            }
        
        return stats
    
    def suggest_optimization(self) -> List[str]:
        """
        Suggest cost optimizations based on usage patterns.
        
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        stats = self.get_usage_stats()
        
        # Check if using too much Claude (paid tier)
        claude_pct = stats.get("claude", {}).get("percentage", 0)
        if claude_pct > 20:
            suggestions.append(
                f"⚠️  Claude usage at {claude_pct:.1f}% (target: 10-20%). "
                "Consider routing more tasks to Gemini/Copilot."
            )
        
        # Check if under-utilizing free tiers
        gemini_pct = stats.get("gemini", {}).get("percentage", 0)
        if gemini_pct < 50:
            suggestions.append(
                f"💡 Gemini usage at {gemini_pct:.1f}% (target: 60-70%). "
                "Route more bulk/doc tasks to free tier."
            )
        
        # Cost efficiency praise
        if 60 <= gemini_pct <= 80 and claude_pct <= 20:
            suggestions.append("✅ Excellent cost optimization! Usage pattern is ideal.")
        
        return suggestions
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load agent selection configuration from JSON file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Return default configuration
        return {
            "label_rules": [
                {
                    "labels": ["security", "architecture", "complex"],
                    "agent": "claude",
                    "cost_level": "high"
                },
                {
                    "labels": ["documentation", "bulk-refactor", "large-scale"],
                    "agent": "gemini",
                    "cost_level": "free"
                },
                {
                    "labels": ["github-workflow", "quick-fix", "pr"],
                    "agent": "copilot",
                    "cost_level": "free-low"
                }
            ],
            "project_defaults": {},
            "fallback_agent": "gemini"
        }
    
    def _track_usage(self, agent_name: str):
        """Track agent usage for statistics."""
        if agent_name in self.usage_stats:
            self.usage_stats[agent_name] += 1


def main():
    """Example usage and testing."""
    selector = AgentSelector()
    
    print("=== Agent Selection Examples ===\n")
    
    # Example 1: Security issue
    print("1. Security Issue")
    agent = selector.select_agent(["security", "bug"], "my-app")
    info = selector.get_agent_info(agent)
    print(f"   Selected: {agent}")
    print(f"   Cost: {info['cost_level']}")
    print(f"   Strengths: {', '.join(info['strengths'])}\n")
    
    # Example 2: Documentation task
    print("2. Documentation Task")
    agent = selector.select_agent(["documentation"], "my-app")
    info = selector.get_agent_info(agent)
    print(f"   Selected: {agent}")
    print(f"   Cost: {info['cost_level']}")
    print(f"   Context: {info['context_window']:,} tokens\n")
    
    # Example 3: GitHub workflow
    print("3. GitHub Workflow")
    agent = selector.select_agent(["github-workflow", "ci-cd"], "my-app")
    info = selector.get_agent_info(agent)
    print(f"   Selected: {agent}")
    print(f"   Cost: {info['cost_level']}\n")
    
    # Example 4: No specific labels (fallback)
    print("4. Generic Issue (fallback)")
    agent = selector.select_agent(["enhancement"], "my-app")
    print(f"   Selected: {agent}\n")
    
    # Show usage stats
    print("=== Usage Statistics ===")
    stats = selector.get_usage_stats()
    for agent, data in stats.items():
        print(f"{agent}: {data['count']} tasks ({data['percentage']:.1f}%)")
    
    # Cost optimization suggestions
    print("\n=== Cost Optimization ===")
    suggestions = selector.suggest_optimization()
    for suggestion in suggestions:
        print(suggestion)


if __name__ == "__main__":
    main()
