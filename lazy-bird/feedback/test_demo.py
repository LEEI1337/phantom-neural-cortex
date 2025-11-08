#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Feedback Loop Test - Without circular imports
"""

import sys
import io

# Set UTF-8 encoding for Windows console ONCE
if sys.platform == 'win32':
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🎯 Feedback Loop Demo - Simulated Refinement Scenario")
print("=" * 70)
print()

# Simulated quality progression over iterations
iterations = [
    {
        "num": 1,
        "name": "Initial Implementation",
        "test_coverage": 0.55,
        "tests_passing": False,
        "test_count": 15,
        "failed_count": 3,
        "code_quality": 0.65,
        "security": 0.80,
        "overall": 0.58,
    },
    {
        "num": 2,
        "name": "First Refinement",
        "test_coverage": 0.68,
        "tests_passing": False,
        "test_count": 18,
        "failed_count": 1,
        "code_quality": 0.75,
        "security": 1.0,
        "overall": 0.72,
    },
    {
        "num": 3,
        "name": "Second Refinement",
        "test_coverage": 0.78,
        "tests_passing": True,
        "test_count": 20,
        "failed_count": 0,
        "code_quality": 0.82,
        "security": 1.0,
        "overall": 0.82,
    },
]

print("📂 Project: projects/Projekt-A")
print("🤖 Agent: gemini (FREE)")
print("🎯 Quality Goal: 75%")
print("📊 Min Coverage: 70%")
print()

print("🔄 Refinement Iterations:")
print()

for it in iterations:
    print(f"📊 Iteration {it['num']}: {it['name']}")
    print("-" * 70)
    print(f"  Test Coverage: {it['test_coverage']*100:.1f}% {'❌' if it['test_coverage'] < 0.70 else '✅'}")
    print(f"  Tests Passing: {'✅' if it['tests_passing'] else '❌'} ({it['test_count'] - it['failed_count']}/{it['test_count']})")
    print(f"  Security: {it['security']*100:.1f}/100 {'✅' if it['security'] >= 0.9 else '⚠️'}")
    print(f"  Code Quality: {it['code_quality']*100:.1f}/100")
    print(f"  Overall Quality: {it['overall']*100:.1f}%")
    print()

    # Q-learning decision
    q_halt = it['overall']
    q_continue = 1.0 - q_halt

    print(f"  Q(HALT): {q_halt:.3f}")
    print(f"  Q(CONTINUE): {q_continue:.3f}")
    print()

    if it['tests_passing'] and q_halt > 0.75:
        print(f"  ✅ HALT: Tests passing & quality >= 0.75!")
        print()
        break
    else:
        reason = []
        if not it['tests_passing']:
            reason.append(f"{it['failed_count']} tests failing")
        if q_halt < 0.75:
            reason.append(f"quality < 0.75")

        print(f"  🔄 CONTINUE: {', '.join(reason)}")
        print()

# Summary
final = iterations[-1]
initial = iterations[0]

print("=" * 70)
print("✅ FEEDBACK LOOP COMPLETE")
print("=" * 70)
print(f"Status: SUCCESS")
print(f"Iterations: {len(iterations)}")
print(f"Final Quality: {final['overall']*100:.1f}%")
print(f"Quality Improvement: +{(final['overall'] - initial['overall'])*100:.1f}%")
print(f"Agent: gemini (FREE)")
print(f"Total Cost: $0.00")
print(f"Time: ~8 minutes")
print("=" * 70)
print()

# Infinite Loop Prevention Demo
print("=" * 70)
print("🛡️ Infinite Loop Prevention Strategies")
print("=" * 70)
print()

print("✅ Strategy 1: Hard Iteration Limit")
print("   → MAX_ITERATIONS = 5 (never exceed)")
print()

print("✅ Strategy 2: Quality Stagnation Detection")
print("   → If variance(quality[-3:]) < 0.001 → ABORT")
print("   → Example: [0.55, 0.56, 0.555] → variance = 0.0001 → STAGNANT")
print()

print("✅ Strategy 3: Quality Degradation Detection")
print("   → If quality is declining → ABORT")
print("   → Example: [0.75, 0.70, 0.65] → DEGRADING")
print()

print("✅ Strategy 4: Minimum Quality Gate")
print("   → After 3 iterations, quality must be > 60%")
print("   → Example: iter=4, quality=0.55 → ABORT")
print()

print("✅ Strategy 5: Cost Limit")
print("   → Don't spend more than $5 on refinements")
print("   → Example: total_cost=$5.50 → ABORT")
print()

print("✅ Strategy 6: Time Limit")
print("   → Max 30 minutes total")
print("   → Example: elapsed=1850s → ABORT")
print()

print("✅ Strategy 7: Feedback Cycle Detection")
print("   → Detect if same feedback repeats")
print("   → Example: hash(feedback) in hash_history[-2:] → CYCLING")
print()

print("=" * 70)
print("✅ Demo Complete!")
print("=" * 70)
print()
