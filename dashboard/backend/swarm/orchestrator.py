import logging
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .intelligence import IntelligenceEngine, RoutingRecommendation
from .impact import ImpactPredictor, ImpactReport

logger = logging.getLogger(__name__)

class SwarmTask(BaseModel):
    task_id: str
    description: str
    priority: str = "balanced"
    max_iterations: int = 3
    quality_threshold: float = 0.8

class SwarmResult(BaseModel):
    task_id: str
    final_output: str
    intermediate_steps: List[Dict[str, Any]]
    total_cost: float
    total_duration: float
    final_quality: float

class SwarmOrchestrator:
    """
    The main coordinator for Phase 5 Advanced Swarm Routing.
    Handles the execution lifecycle, feedback loops, and intelligent switching.
    """
    
    def __init__(self):
        self.intelligence = IntelligenceEngine()
        self.impact = ImpactPredictor(self.intelligence)
        self.active_tasks: Dict[str, SwarmTask] = {}
        
    async def get_impact_report(self, description: str) -> ImpactReport:
        """Get a preview of how swarm would handle this task"""
        return await self.impact.predict_impact(description)

    async def execute_task(self, task: SwarmTask) -> SwarmResult:
        """
        Execute a swarm task with feedback loops and intelligent fallback.
        1. Select agent
        2. Execute
        3. Evaluate quality
        4. Re-route if quality is low (Feedback Loop)
        """
        logger.info(f"🚀 Starting Swarm Execution for task: {task.task_id}")
        
        steps = []
        current_iteration = 0
        current_quality = 0.0
        total_cost = 0.0
        start_time = asyncio.get_event_loop().time()
        
        final_output = ""
        
        while current_iteration < task.max_iterations and current_quality < task.quality_threshold:
            current_iteration += 1
            
            # 1. Routing Decision
            # If previous quality was low, shift priority to 'quality' for next iteration
            iter_priority = "quality" if current_iteration > 1 else task.priority
            
            recommendation = await self.intelligence.analyze_and_route(
                task.description, 
                priority=iter_priority,
                min_quality=max(current_quality, 0.5)
            )
            
            logger.info(f"Iteration {current_iteration}: Routing to {recommendation.selected_agent}")
            
            # 2. Execution (Simulated for Phase 5 Logic verification)
            # In Phase 8, this calls the actual Gateway/Agent execution
            step_duration = np_simulate_latency(recommendation.selected_agent)
            await asyncio.sleep(0.1) # Small sleep for async simulation
            
            # Mock output and quality assignment
            step_output = f"Output from {recommendation.selected_agent} at iteration {current_iteration}"
            step_quality = recommendation.predicted_quality * (0.8 + 0.2 * current_iteration) # Improves over time
            
            current_quality = min(0.99, step_quality)
            total_cost += recommendation.estimated_cost
            final_output = step_output if current_quality > 0.8 else final_output or step_output
            
            steps.append({
                "iteration": current_iteration,
                "agent": recommendation.selected_agent,
                "quality": current_quality,
                "cost": recommendation.estimated_cost,
                "reasoning": recommendation.reasoning
            })
            
            if current_quality >= task.quality_threshold:
                logger.info(f"✅ Quality threshold {task.quality_threshold} met at iteration {current_iteration}")
                break

        end_time = asyncio.get_event_loop().time()
        
        result = SwarmResult(
            task_id=task.task_id,
            final_output=final_output,
            intermediate_steps=steps,
            total_cost=total_cost,
            total_duration=end_time - start_time,
            final_quality=current_quality
        )
        
        logger.info(f"🏁 Swarm task {task.task_id} completed. Total cost: ${total_cost:.4f}")
        return result

def np_simulate_latency(agent_id: str) -> float:
    """Helper for simulation"""
    if "mini" in agent_id: return 2.0
    if "sonnet" in agent_id: return 15.0
    if "pro" in agent_id: return 25.0
    return 10.0
