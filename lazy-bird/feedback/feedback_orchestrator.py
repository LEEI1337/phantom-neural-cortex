#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feedback Orchestrator

Main orchestrator for the hierarchical feedback loop system.
"""

import sys
import io
import logging
from pathlib import Path
from typing import Dict, Optional

try:
    from .quality_evaluator import QualityEvaluator, QualityMetrics
    from .refinement_agent import RefinementAgent
    from .loop_prevention import InfiniteLoopPrevention, LoopMetrics
except ImportError:
    from quality_evaluator import QualityEvaluator, QualityMetrics
    from refinement_agent import RefinementAgent
    from loop_prevention import InfiniteLoopPrevention, LoopMetrics

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FeedbackOrchestrator:
    """Orchestrates the hierarchical feedback loop."""

    def __init__(
        self,
        agent_name: str = "gemini",
        min_coverage: float = 0.60,
        min_quality: float = 0.75,
        max_iterations: int = 5,
        max_cost: float = 5.0
    ):
        """Initialize feedback orchestrator.

        Args:
            agent_name: Agent to use (claude/gemini/copilot)
            min_coverage: Minimum test coverage
            min_quality: Minimum overall quality
            max_iterations: Maximum refinement iterations
            max_cost: Maximum cost in dollars
        """
        self.agent_name = agent_name

        # Initialize components
        self.evaluator = QualityEvaluator(
            min_coverage=min_coverage,
            min_quality=min_quality,
            max_iterations=max_iterations
        )

        self.refiner = RefinementAgent(agent_name=agent_name)

        self.loop_prevention = InfiniteLoopPrevention(
            max_iterations=max_iterations,
            min_quality_threshold=min_quality,
            max_cost=max_cost
        )

    def execute_feedback_loop(
        self,
        project_path: Path,
        quality_goals: Optional[Dict] = None
    ) -> Dict:
        """Execute feedback loop until halt condition.

        Args:
            project_path: Path to project directory
            quality_goals: Optional quality goals override

        Returns:
            Dict with final results and metrics
        """
        if quality_goals is None:
            quality_goals = {
                "min_coverage": self.evaluator.min_coverage,
                "min_quality": self.evaluator.min_quality,
            }

        logger.info("=" * 60)
        logger.info("🔄 Starting Feedback Loop")
        logger.info("=" * 60)
        logger.info(f"Project: {project_path}")
        logger.info(f"Agent: {self.agent_name}")
        logger.info(f"Quality Goals: {quality_goals}")
        logger.info("=" * 60)

        # Start tracking
        self.loop_prevention.start_tracking()

        iteration = 0
        state = {
            "quality_goals": quality_goals,
            "feedback": [],
            "failed_tests": []
        }

        while True:
            iteration += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"📊 ITERATION {iteration}")
            logger.info(f"{'='*60}\n")

            # L-Module: Refine implementation
            logger.info("🔧 L-Module: Executing refinement...")
            refinement_result = self.refiner.refine_implementation(
                project_path=project_path,
                feedback=state.get("feedback", []),
                previous_state=state,
                iteration=iteration
            )

            # H-Module: Evaluate quality
            logger.info("📈 H-Module: Evaluating quality...")
            metrics = self.evaluator.evaluate_implementation({
                "tests": refinement_result["tests"],
                "code_analysis": refinement_result["code_analysis"],
                "security": refinement_result["security"],
            })

            logger.info(f"\n📊 Quality Metrics:")
            logger.info(f"  Test Coverage: {metrics.test_coverage*100:.1f}%")
            logger.info(f"  Tests Passing: {'✅' if metrics.tests_passing else '❌'}")
            logger.info(f"  Security Score: {metrics.security_score*100:.1f}/100")
            logger.info(f"  Code Quality: {metrics.code_quality_score*100:.1f}/100")
            logger.info(f"  Overall Quality: {metrics.overall_quality*100:.1f}/100\n")

            # Track iteration
            feedback_str = "\n".join(state.get("feedback", []))
            iteration_cost = self._estimate_iteration_cost(iteration)
            self.loop_prevention.add_iteration(
                quality=metrics.overall_quality,
                feedback=feedback_str,
                cost=iteration_cost
            )

            # Adaptive Halting Decision (H-Module)
            should_halt = self.evaluator.should_halt(metrics, iteration)

            # Infinite Loop Prevention Check
            should_abort, abort_reason = self.loop_prevention.should_abort(
                iteration=iteration,
                quality=metrics.overall_quality
            )

            # Decision: HALT
            if should_halt:
                logger.info("=" * 60)
                logger.info("✅ HALTING: Quality sufficient!")
                logger.info("=" * 60)

                loop_metrics = self.loop_prevention.get_metrics(
                    halt_reason="quality_sufficient",
                    agent=self.agent_name
                )

                return self._build_result(
                    status="success",
                    metrics=metrics,
                    loop_metrics=loop_metrics,
                    project_path=project_path
                )

            # Decision: ABORT
            if should_abort:
                logger.warning("=" * 60)
                logger.warning(f"⚠️ ABORTING: {abort_reason}")
                logger.warning("=" * 60)

                loop_metrics = self.loop_prevention.get_metrics(
                    halt_reason=abort_reason,
                    agent=self.agent_name
                )

                return self._build_result(
                    status="aborted",
                    metrics=metrics,
                    loop_metrics=loop_metrics,
                    project_path=project_path,
                    abort_reason=abort_reason
                )

            # Decision: CONTINUE
            logger.info("🔄 CONTINUING to next iteration...\n")

            # Generate feedback for next iteration (H-Module)
            feedback = self.evaluator.generate_feedback(
                metrics=metrics,
                test_results=refinement_result["tests"]
            )

            # Update state for next iteration
            state.update({
                "feedback": feedback,
                "failed_tests": refinement_result["tests"].get("errors", []),
                "metrics": metrics,
                "iteration": iteration
            })

    def _estimate_iteration_cost(self, iteration: int) -> float:
        """Estimate cost of iteration based on agent.

        Args:
            iteration: Iteration number

        Returns:
            Estimated cost in dollars
        """
        # Cost per iteration (rough estimates)
        costs = {
            "gemini": 0.0,      # Free tier
            "copilot": 0.0,     # Free with Pro
            "claude": 0.5,      # ~$0.50 per refinement
        }

        return costs.get(self.agent_name, 0.0)

    def _build_result(
        self,
        status: str,
        metrics: QualityMetrics,
        loop_metrics: LoopMetrics,
        project_path: Path,
        abort_reason: str = ""
    ) -> Dict:
        """Build final result dict.

        Args:
            status: "success" or "aborted"
            metrics: Final quality metrics
            loop_metrics: Loop execution metrics
            project_path: Project path
            abort_reason: Abort reason (if aborted)

        Returns:
            Result dict
        """
        result = {
            "status": status,
            "project_path": str(project_path),
            "agent": self.agent_name,
            "quality_metrics": {
                "test_coverage": metrics.test_coverage,
                "tests_passing": metrics.tests_passing,
                "security_score": metrics.security_score,
                "code_quality": metrics.code_quality_score,
                "overall_quality": metrics.overall_quality,
            },
            "loop_metrics": {
                "iterations": loop_metrics.iterations,
                "total_time": loop_metrics.total_time,
                "quality_progression": loop_metrics.quality_progression,
                "stagnation_detected": loop_metrics.stagnation_detected,
                "halt_reason": loop_metrics.halt_reason,
                "total_cost": loop_metrics.total_cost,
            }
        }

        if status == "aborted":
            result["abort_reason"] = abort_reason

        # Log summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 FEEDBACK LOOP SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Status: {status.upper()}")
        logger.info(f"Iterations: {loop_metrics.iterations}")
        logger.info(f"Total Time: {loop_metrics.total_time:.1f}s")
        logger.info(f"Final Quality: {metrics.overall_quality*100:.1f}%")
        logger.info(f"Total Cost: ${loop_metrics.total_cost:.2f}")
        logger.info(f"Agent: {self.agent_name}")
        logger.info("=" * 60 + "\n")

        return result
