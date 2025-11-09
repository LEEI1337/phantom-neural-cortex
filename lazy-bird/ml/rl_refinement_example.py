"""
Example: RL Refinement Chain Usage
===================================

Demonstrates how to use the RL-based refinement chain for adaptive code quality improvement.
"""

import sys
from pathlib import Path
import time

# Add lazy-bird to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.rl_refinement_chain import (
    RefinementState,
    RLRefinementChain,
    SimplePPOAgent,
    REFINEMENT_ACTIONS
)


def simulate_action_execution(action_id: int) -> tuple:
    """
    Simulates executing a refinement action.

    In production, this would:
    - Call actual linters, formatters, test runners
    - Measure real execution time and cost
    - Return actual quality improvements

    Args:
        action_id: ID of action to execute

    Returns:
        (new_state, execution_metrics)
    """
    action = REFINEMENT_ACTIONS[action_id]

    # Simulate execution time
    time.sleep(0.1)  # Simulated delay

    # Mock quality improvements based on action
    improvements = {
        0: {'test_coverage': 10, 'type_safety_score': 5},  # run_tests
        1: {'type_safety_score': 20, 'test_coverage': 5},  # fix_types
        2: {'security_score': 25},  # improve_security
        3: {'complexity_score': 15, 'maintainability_score': 10},  # reduce_complexity
        4: {'documentation_score': 30},  # add_docs
        5: {'performance_score': 20},  # optimize_performance
        6: {'complexity_score': 5, 'type_safety_score': 5},  # quick_fix
        7: {'test_coverage': 15, 'security_score': 15, 'type_safety_score': 10},  # comprehensive
    }

    # Create new state with improvements
    global current_state
    improvement = improvements.get(action_id, {})

    new_state = RefinementState(
        test_coverage=min(100, current_state.test_coverage + improvement.get('test_coverage', 0)),
        security_score=min(100, current_state.security_score + improvement.get('security_score', 0)),
        complexity_score=min(100, current_state.complexity_score + improvement.get('complexity_score', 0)),
        documentation_score=min(100, current_state.documentation_score + improvement.get('documentation_score', 0)),
        type_safety_score=min(100, current_state.type_safety_score + improvement.get('type_safety_score', 0)),
        performance_score=min(100, current_state.performance_score + improvement.get('performance_score', 0)),
        maintainability_score=min(100, current_state.maintainability_score + improvement.get('maintainability_score', 0)),
        current_iteration=current_state.current_iteration + 1,
        max_iterations=current_state.max_iterations,
        time_elapsed_seconds=current_state.time_elapsed_seconds + action.expected_time_seconds,
        cost_usd=current_state.cost_usd + action.expected_cost_usd,
        syntax_errors=max(0, current_state.syntax_errors - 1) if action_id in [1, 6] else current_state.syntax_errors,
        type_errors=max(0, current_state.type_errors - 2) if action_id == 1 else current_state.type_errors,
        test_failures=max(0, current_state.test_failures - 1) if action_id in [0, 7] else current_state.test_failures,
        security_vulnerabilities=max(0, current_state.security_vulnerabilities - 1) if action_id == 2 else current_state.security_vulnerabilities,
        action_history=current_state.action_history + [action_id]
    )

    execution_metrics = {
        'time_seconds': action.expected_time_seconds,
        'cost_usd': action.expected_cost_usd,
        'quality_improvement': improvement
    }

    # Update global state
    current_state = new_state

    return new_state, execution_metrics


# Global state for simulation
current_state = None


def run_single_episode():
    """Runs a single refinement episode."""
    global current_state

    # Initialize with poor quality code
    current_state = RefinementState(
        test_coverage=40.0,
        security_score=50.0,
        complexity_score=55.0,
        documentation_score=30.0,
        type_safety_score=45.0,
        performance_score=60.0,
        maintainability_score=50.0,
        current_iteration=0,
        max_iterations=10,
        time_elapsed_seconds=0.0,
        cost_usd=0.0,
        syntax_errors=3,
        type_errors=5,
        test_failures=4,
        security_vulnerabilities=2,
        action_history=[]
    )

    print("\n" + "=" * 60)
    print("Starting Refinement Episode")
    print("=" * 60)
    print(f"\nInitial Quality Scores:")
    print(f"  Test Coverage: {current_state.test_coverage}%")
    print(f"  Security: {current_state.security_score}%")
    print(f"  Complexity: {current_state.complexity_score}%")
    print(f"  Documentation: {current_state.documentation_score}%")
    print(f"  Type Safety: {current_state.type_safety_score}%")
    print(f"  Performance: {current_state.performance_score}%")
    print(f"  Maintainability: {current_state.maintainability_score}%")
    print(f"\nErrors: Syntax={current_state.syntax_errors}, Type={current_state.type_errors}, "
          f"Tests={current_state.test_failures}, Security={current_state.security_vulnerabilities}")

    # Create RL refinement chain
    chain = RLRefinementChain(
        target_quality=85.0,
        max_iterations=10
    )

    # Run refinement loop
    result = chain.run_refinement_loop(
        initial_state=current_state,
        executor_callback=simulate_action_execution,
        exploration_rate=0.2  # 20% exploration
    )

    # Print results
    print("\n" + "=" * 60)
    print("Episode Complete")
    print("=" * 60)
    print(f"\nFinal Quality Scores:")
    final_state = result['final_state']
    print(f"  Test Coverage: {final_state.test_coverage}%")
    print(f"  Security: {final_state.security_score}%")
    print(f"  Complexity: {final_state.complexity_score}%")
    print(f"  Documentation: {final_state.documentation_score}%")
    print(f"  Type Safety: {final_state.type_safety_score}%")
    print(f"  Performance: {final_state.performance_score}%")
    print(f"  Maintainability: {final_state.maintainability_score}%")

    print(f"\nActions Taken ({len(result['actions_taken'])}):")
    for i, action_id in enumerate(result['actions_taken']):
        action = REFINEMENT_ACTIONS[action_id]
        reward = result['episode_rewards'][i]
        print(f"  {i + 1}. {action.name} (reward: {reward:.2f})")

    print(f"\nTotal Reward: {result['total_reward']:.2f}")
    print(f"Success: {'✓' if result['success'] else '✗'}")
    print(f"Total Time: {final_state.time_elapsed_seconds:.1f}s")
    print(f"Total Cost: ${final_state.cost_usd:.3f}")

    return chain, result


def run_training_episodes(num_episodes: int = 10):
    """
    Runs multiple training episodes to train the RL agent.

    Args:
        num_episodes: Number of episodes to run
    """
    # Create persistent agent
    agent = SimplePPOAgent(state_dim=20, action_dim=8)
    chain = RLRefinementChain(agent=agent, target_quality=85.0)

    print("\n" + "=" * 60)
    print(f"Training RL Agent - {num_episodes} Episodes")
    print("=" * 60)

    for episode in range(num_episodes):
        global current_state

        # Reset initial state with some randomness
        import random
        current_state = RefinementState(
            test_coverage=random.uniform(30, 50),
            security_score=random.uniform(40, 60),
            complexity_score=random.uniform(45, 65),
            documentation_score=random.uniform(20, 40),
            type_safety_score=random.uniform(35, 55),
            performance_score=random.uniform(50, 70),
            maintainability_score=random.uniform(40, 60),
            current_iteration=0,
            max_iterations=10,
            time_elapsed_seconds=0.0,
            cost_usd=0.0,
            syntax_errors=random.randint(0, 5),
            type_errors=random.randint(0, 8),
            test_failures=random.randint(0, 6),
            security_vulnerabilities=random.randint(0, 3),
            action_history=[]
        )

        # Run episode
        result = chain.run_refinement_loop(
            initial_state=current_state,
            executor_callback=simulate_action_execution,
            exploration_rate=max(0.1, 0.5 - episode * 0.04)  # Decay exploration
        )

        # Print progress
        stats = chain.get_training_stats()
        print(f"\nEpisode {episode + 1}/{num_episodes}:")
        print(f"  Reward: {result['total_reward']:.2f}")
        print(f"  Success: {'✓' if result['success'] else '✗'}")
        print(f"  Actions: {len(result['actions_taken'])}")
        print(f"  Success Rate: {stats['success_rate']:.1%}")
        print(f"  Avg Reward: {stats['avg_reward']:.2f}")

    # Final stats
    print("\n" + "=" * 60)
    print("Training Complete")
    print("=" * 60)
    final_stats = chain.get_training_stats()
    print(f"\nFinal Statistics:")
    print(f"  Total Episodes: {final_stats['episode_count']}")
    print(f"  Success Count: {final_stats['success_count']}")
    print(f"  Success Rate: {final_stats['success_rate']:.1%}")
    print(f"  Average Reward: {final_stats['avg_reward']:.2f}")
    print(f"  Buffer Size: {final_stats['buffer_size']}")

    # Save trained agent
    save_path = Path(__file__).parent / "trained_rl_agent.npz"
    chain.save_agent(save_path)

    return chain


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "train":
        # Training mode
        num_episodes = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        chain = run_training_episodes(num_episodes)
    else:
        # Single episode demo
        chain, result = run_single_episode()

        # Show training stats
        print("\n" + "=" * 60)
        print("Training Statistics")
        print("=" * 60)
        stats = chain.get_training_stats()
        print(f"Episodes: {stats['episode_count']}")
        print(f"Success Rate: {stats['success_rate']:.1%}")
        print(f"Buffer Size: {stats['buffer_size']}")
