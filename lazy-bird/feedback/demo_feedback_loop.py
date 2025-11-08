#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feedback Loop Demo

Demonstrates the hierarchical feedback loop system.
"""

import sys
import io
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from feedback_orchestrator import FeedbackOrchestrator
from quality_evaluator import QualityMetrics


def simulate_refinement_scenario():
    """Simulate a refinement scenario with improving quality."""

    print("=" * 70)
    print("🎯 Feedback Loop Demo - Simulated Refinement Scenario")
    print("=" * 70)
    print()

    # Simulate project path
    project_path = Path("../../projects/Projekt-A")

    # Create orchestrator
    orchestrator = FeedbackOrchestrator(
        agent_name="gemini",
        min_coverage=0.70,
        min_quality=0.75,
        max_iterations=5,
        max_cost=5.0
    )

    print(f"📂 Project: {project_path}")
    print(f"🤖 Agent: gemini (FREE)")
    print(f"🎯 Quality Goal: 75%")
    print(f"📊 Min Coverage: 70%")
    print()

    # Simulate iterations manually to show progression
    print("🔄 Simulating Refinement Iterations...")
    print()

    # Iteration 1: Initial implementation (poor quality)
    print("📊 Iteration 1: Initial Implementation")
    print("-" * 70)
    metrics_1 = QualityMetrics(
        test_coverage=0.55,      # 55% - below target
        tests_passing=False,      # 3 tests failing
        test_count=15,
        failed_test_count=3,
        code_quality_score=0.65,
        security_score=0.80,      # 1 vulnerability
        vulnerabilities=1,
        type_coverage=0.90,
        doc_coverage=0.40
    )
    print(f"  Test Coverage: {metrics_1.test_coverage*100:.1f}% ❌")
    print(f"  Tests Passing: {'✅' if metrics_1.tests_passing else '❌'}")
    print(f"  Security: {metrics_1.security_score*100:.1f}/100")
    print(f"  Overall Quality: {metrics_1.overall_quality*100:.1f}%")
    print()
    print(f"  Q(HALT): {orchestrator.evaluator.compute_halt_q_value(metrics_1):.3f}")
    print(f"  Decision: CONTINUE (quality too low)")
    print()

    # Iteration 2: First refinement
    print("📊 Iteration 2: First Refinement")
    print("-" * 70)
    metrics_2 = QualityMetrics(
        test_coverage=0.68,      # Improved to 68%
        tests_passing=False,      # 1 test still failing
        test_count=18,            # Added 3 more tests
        failed_test_count=1,
        code_quality_score=0.75,
        security_score=1.0,       # Fixed vulnerability
        vulnerabilities=0,
        type_coverage=0.95,
        doc_coverage=0.60
    )
    print(f"  Test Coverage: {metrics_2.test_coverage*100:.1f}% (↑13%)")
    print(f"  Tests Passing: {'✅' if metrics_2.tests_passing else '❌'} (↑ 2 tests fixed)")
    print(f"  Security: {metrics_2.security_score*100:.1f}/100 ✅")
    print(f"  Overall Quality: {metrics_2.overall_quality*100:.1f}% (↑{(metrics_2.overall_quality - metrics_1.overall_quality)*100:.1f}%)")
    print()
    print(f"  Q(HALT): {orchestrator.evaluator.compute_halt_q_value(metrics_2):.3f}")
    print(f"  Decision: CONTINUE (1 test failing)")
    print()

    # Iteration 3: Second refinement
    print("📊 Iteration 3: Second Refinement")
    print("-" * 70)
    metrics_3 = QualityMetrics(
        test_coverage=0.78,      # 78%
        tests_passing=True,       # All tests passing! ✅
        test_count=20,
        failed_test_count=0,
        code_quality_score=0.82,
        security_score=1.0,
        vulnerabilities=0,
        type_coverage=1.0,
        doc_coverage=0.75
    )
    print(f"  Test Coverage: {metrics_3.test_coverage*100:.1f}% (↑10%)")
    print(f"  Tests Passing: {'✅' if metrics_3.tests_passing else '❌'} ✅ All passing!")
    print(f"  Security: {metrics_3.security_score*100:.1f}/100 ✅")
    print(f"  Overall Quality: {metrics_3.overall_quality*100:.1f}% (↑{(metrics_3.overall_quality - metrics_2.overall_quality)*100:.1f}%)")
    print()
    print(f"  Q(HALT): {orchestrator.evaluator.compute_halt_q_value(metrics_3):.3f}")
    print(f"  Q(CONTINUE): {1.0 - orchestrator.evaluator.compute_halt_q_value(metrics_3):.3f}")
    print()
    print(f"  ✅ HALT: Q(HALT) > Q(CONTINUE) AND Tests Passing!")
    print()

    # Summary
    print("=" * 70)
    print("✅ FEEDBACK LOOP COMPLETE")
    print("=" * 70)
    print(f"Status: SUCCESS")
    print(f"Iterations: 3")
    print(f"Final Quality: {metrics_3.overall_quality*100:.1f}%")
    print(f"Quality Improvement: {(metrics_3.overall_quality - metrics_1.overall_quality)*100:.1f}%")
    print(f"Agent: gemini (FREE)")
    print(f"Total Cost: $0.00")
    print(f"Time: ~8 minutes")
    print("=" * 70)
    print()


def demonstrate_infinite_loop_prevention():
    """Demonstrate infinite loop prevention strategies."""

    print("=" * 70)
    print("🛡️ Infinite Loop Prevention Demo")
    print("=" * 70)
    print()

    from loop_prevention import InfiniteLoopPrevention

    preventer = InfiniteLoopPrevention(
        max_iterations=5,
        min_quality_threshold=0.60,
        stagnation_window=3
    )

    preventer.start_tracking()

    print("Scenario 1: Quality Stagnation")
    print("-" * 70)

    # Simulate stagnating quality
    qualities = [0.55, 0.56, 0.555, 0.556, 0.555]
    for i, q in enumerate(qualities, 1):
        preventer.add_iteration(
            quality=q,
            feedback=f"iteration {i} feedback",
            cost=0.0
        )
        print(f"  Iteration {i}: Quality = {q:.3f}")

        if preventer.is_stagnating():
            print(f"    ⚠️ Stagnation detected! (variance < 0.001)")

        should_abort, reason = preventer.should_abort(i, q)
        if should_abort:
            print(f"    🛑 ABORT: {reason}")
            break

    print()
    print("Scenario 2: Quality Degradation")
    print("-" * 70)

    preventer.reset()
    preventer.start_tracking()

    # Simulate declining quality
    qualities = [0.75, 0.70, 0.65, 0.60, 0.55]
    for i, q in enumerate(qualities, 1):
        preventer.add_iteration(
            quality=q,
            feedback=f"iteration {i} feedback",
            cost=0.0
        )
        print(f"  Iteration {i}: Quality = {q:.3f}")

        if preventer.is_stagnating():
            print(f"    ⚠️ Quality degradation detected!")

        should_abort, reason = preventer.should_abort(i, q)
        if should_abort:
            print(f"    🛑 ABORT: {reason}")
            break

    print()
    print("Scenario 3: Feedback Cycling")
    print("-" * 70)

    preventer.reset()
    preventer.start_tracking()

    # Simulate cycling feedback
    feedbacks = [
        "Fix test_auth.py line 42",
        "Fix test_products.py line 15",
        "Fix test_auth.py line 42",  # Cycle!
        "Fix test_auth.py line 42",  # Cycle!
    ]

    for i, fb in enumerate(feedbacks, 1):
        preventer.add_iteration(
            quality=0.65,
            feedback=fb,
            cost=0.0
        )
        print(f"  Iteration {i}: Feedback = '{fb[:30]}...'")

        if preventer.is_cycling():
            print(f"    🔄 Feedback cycle detected!")

        should_abort, reason = preventer.should_abort(i, 0.65)
        if should_abort:
            print(f"    🛑 ABORT: {reason}")
            break

    print()
    print("=" * 70)
    print("✅ Infinite Loop Prevention Demo Complete")
    print("=" * 70)
    print()


def main():
    """Run all demos."""

    print("\n")
    simulate_refinement_scenario()
    print("\n")
    demonstrate_infinite_loop_prevention()
    print("\n")


if __name__ == "__main__":
    main()
