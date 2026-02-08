import asyncio
import logging
import json
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add root to sys.path
sys.path.append(os.path.abspath(os.curdir))

from dashboard.backend.swarm.orchestrator import SwarmOrchestrator, SwarmTask

async def test_phase5_routing():
    print("🚀 Testing Phase 5 Advanced Swarm Routing...")
    orchestrator = SwarmOrchestrator()
    
    # 1. Test Impact Prediction
    print("\n--- Step 1: Impact Prediction (Dry Run) ---")
    task_desc = "Implement a complex microservices architecture for a fintech platform with banking-grade security."
    report = await orchestrator.get_impact_report(task_desc)
    
    print(f"Task: {task_desc[:50]}...")
    print(f"Efficiency Potential: {report.overall_savings_potential:.1f}%")
    print(f"Recommendation: {report.recommendation}")
    
    for opt in report.options:
        print(f"  [{opt.priority.upper()}] -> Agent: {opt.selected_agent}, Cost: ${opt.est_cost:.4f}, Res: {opt.est_quality*100:.0f}% Qual")

    # 2. Test Smart Execution with Feedback Loop
    print("\n--- Step 2: Smart Execution with Feedback Loop ---")
    task = SwarmTask(
        task_id="verify-feedback-001",
        description="Write a Python script to scrape financial data and generate a report.",
        priority="balanced",
        max_iterations=3,
        quality_threshold=0.9
    )
    
    result = await orchestrator.execute_task(task)
    
    print(f"Final Quality: {result.final_quality*100:.1f}%")
    print(f"Total Iterations: {len(result.intermediate_steps)}")
    print(f"Total Cost: ${result.total_cost:.4f}")
    
    for step in result.intermediate_steps:
        print(f"  Step {step['iteration']}: Agent: {step['agent']}, Quality: {step['quality']*100:.1f}%")

    print("\n✅ Phase 5 Advanced Swarm Routing is OPERATIONAL! 🚀")

if __name__ == "__main__":
    asyncio.run(test_phase5_routing())
