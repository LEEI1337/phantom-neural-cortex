import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from enum import Enum

logger = logging.getLogger(__name__)

class AgentCapability(BaseModel):
    agent_id: str
    name: str
    intelligence_score: float  # 0.0 - 1.0 (e.g. Claude 3.5 Sonnet = 0.9, GPT-4o = 0.95)
    speed_score: float         # 0.0 - 1.0 (e.g. Haiku = 1.0, Sonnet = 0.6)
    cost_per_1k_tokens: float  # USD
    max_context: int           # Token count
    strengths: List[str]       # e.g. ["coding", "architecture", "summarization"]

class RoutingRecommendation(BaseModel):
    selected_agent: str
    confidence: float
    reasoning: str
    estimated_cost: float
    estimated_duration: float
    predicted_quality: float

class IntelligenceEngine:
    """
    Core AI engine for intelligent agent routing (Phase 5).
    Predicts the best agent based on task requirements vs agent capabilities.
    """
    
    def __init__(self):
        # Default capabilities - in production, these would be loaded from DB/Config
        self.agents: Dict[str, AgentCapability] = {
            "claude-quality": AgentCapability(
                agent_id="claude-3-5-sonnet",
                name="Claude 3.5 Sonnet (Quality)",
                intelligence_score=0.95,
                speed_score=0.6,
                cost_per_1k_tokens=0.015,
                max_context=200000,
                strengths=["coding", "architecture", "security", "complex_logic"]
            ),
            "gemini-bulk": AgentCapability(
                agent_id="gemini-1-5-pro",
                name="Gemini 1.5 Pro (Context)",
                intelligence_score=0.90,
                speed_score=0.5,
                cost_per_1k_tokens=0.007,
                max_context=1000000,
                strengths=["documentation", "bulk_analysis", "long_context"]
            ),
            "gpt-speed": AgentCapability(
                agent_id="gpt-4o-mini",
                name="GPT-4o Mini (Speed)",
                intelligence_score=0.75,
                speed_score=1.0,
                cost_per_1k_tokens=0.00015,
                max_context=128000,
                strengths=["simple_tasks", "boilerplate", "formatting"]
            ),
            "deepseek-cost": AgentCapability(
                agent_id="deepseek-coder",
                name="DeepSeek Coder (Cost)",
                intelligence_score=0.85,
                speed_score=0.7,
                cost_per_1k_tokens=0.0001,
                max_context=64000,
                strengths=["coding", "scripts", "unit_tests"]
            )
        }

    async def analyze_and_route(
        self, 
        task_description: str, 
        priority: str = "balanced",
        min_quality: float = 0.7
    ) -> RoutingRecommendation:
        """
        Analyze task and select best agent.
        
        Args:
            task_description: The text describing what needs to be done
            priority: 'speed', 'cost', 'quality', or 'balanced'
            min_quality: Minimum intelligence score required
            
        Returns:
            RoutingRecommendation with selected agent and metrics
        """
        logger.info(f"Analyzing routing for task: {task_description[:50]}... (Priority: {priority})")
        
        # 1. Evaluate task complexity (Simple heuristic for now)
        is_complex = any(word in task_description.lower() for word in ["architect", "secure", "refactor", "debug", "complex"])
        is_coding = any(word in task_description.lower() for word in ["code", "python", "typescript", "function", "fix"])
        is_bulk = len(task_description) > 5000 or "analyze all" in task_description.lower()

        scores: Dict[str, float] = {}
        
        for aid, agent in self.agents.items():
            # Base score is intelligence
            score = agent.intelligence_score
            
            # Filter by minimum quality
            if agent.intelligence_score < min_quality:
                score = -1.0
                continue

            # Weight by priority
            if priority == "quality":
                score *= 2.0
            elif priority == "speed":
                score += agent.speed_score * 1.5
            elif priority == "cost":
                # Invert cost - lower cost = higher score boost
                score += (1.0 / (agent.cost_per_1k_tokens * 100)) * 0.5
            
            # Strength matching
            if is_coding and "coding" in agent.strengths:
                score += 0.3
            if is_complex and "architecture" in agent.strengths:
                score += 0.5
            if is_bulk and agent.max_context > 500000:
                score += 1.0

            scores[aid] = score

        # Select highest score
        best_aid = max(scores, key=scores.get)
        best_agent = self.agents[best_aid]
        
        # Calculate heuristics for recommendation
        # Estimated 1000 tokens for prediction
        est_cost = best_agent.cost_per_1k_tokens 
        est_duration = 30.0 / (best_agent.speed_score or 0.1) # Base 30s inverted by speed
        
        return RoutingRecommendation(
            selected_agent=best_agent.agent_id,
            confidence=min(0.99, scores[best_aid] / 2.0),
            reasoning=f"Selected {best_agent.name} because it matches {'complex' if is_complex else 'standard'} {priority} requirements.",
            estimated_cost=est_cost,
            estimated_duration=est_duration,
            predicted_quality=best_agent.intelligence_score
        )
