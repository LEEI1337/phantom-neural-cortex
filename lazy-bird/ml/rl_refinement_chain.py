"""
Turing-Complete Refinement Chain - PHASE C Optimierung #11
===========================================================

Reinforcement Learning basierter Strategy Generator für Refinement Loops.
Nutzt PPO (Proximal Policy Optimization) um optimale Refinement-Strategien zu lernen.

Key Features:
- PPO-based Policy Learning
- State Encoding (Code Quality, Test Results, Complexity)
- Action Space (8 Refinement Strategies)
- Reward Shaping (Quality Improvement, Time Efficiency, Cost)
- Experience Replay & Online Learning

Use Case: Adaptive Refinement Strategy Selection
Based on: HRM Paper's adaptive computation time + Turing-complete reasoning loops
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from collections import deque
import random


@dataclass
class RefinementState:
    """
    Zustand des Refinement Prozesses.

    Encoding für RL Agent:
    - Code Quality Metrics (7 dimensions)
    - Iteration History
    - Resource Usage
    - Error Patterns
    """

    # Quality metrics (0-100)
    test_coverage: float
    security_score: float
    complexity_score: float
    documentation_score: float
    type_safety_score: float
    performance_score: float
    maintainability_score: float

    # Iteration state
    current_iteration: int
    max_iterations: int
    time_elapsed_seconds: float
    cost_usd: float

    # Error patterns
    syntax_errors: int
    type_errors: int
    test_failures: int
    security_vulnerabilities: int

    # Previous actions history (last 3)
    action_history: List[int]

    def to_vector(self) -> np.ndarray:
        """
        Konvertiert State zu Feature Vector für RL Agent.

        Returns:
            28-dimensional feature vector
        """
        features = [
            # Normalized quality metrics (7)
            self.test_coverage / 100.0,
            self.security_score / 100.0,
            self.complexity_score / 100.0,
            self.documentation_score / 100.0,
            self.type_safety_score / 100.0,
            self.performance_score / 100.0,
            self.maintainability_score / 100.0,

            # Iteration progress (3)
            self.current_iteration / self.max_iterations,
            min(self.time_elapsed_seconds / 300.0, 1.0),  # Normalize to 5min
            min(self.cost_usd / 1.0, 1.0),  # Normalize to $1

            # Error counts (normalized, 4)
            min(self.syntax_errors / 10.0, 1.0),
            min(self.type_errors / 10.0, 1.0),
            min(self.test_failures / 10.0, 1.0),
            min(self.security_vulnerabilities / 5.0, 1.0),

            # Action history one-hot encoding (3 × 8 = 24 but simplified to 6)
            # Use last 2 actions only for brevity
            *self._encode_action_history()
        ]

        return np.array(features, dtype=np.float32)

    def _encode_action_history(self) -> List[float]:
        """Encodes last 2 actions (2 values, normalized 0-1)."""
        history = self.action_history[-2:] if len(self.action_history) >= 2 else [0, 0]
        # Pad if needed
        while len(history) < 2:
            history.insert(0, 0)
        # Normalize to 0-1 (8 actions → divide by 7)
        return [h / 7.0 for h in history[-2:]]


@dataclass
class RefinementAction:
    """
    Refinement Aktion die der Agent ausführen kann.

    8 Aktionen:
    0: Run full tests
    1: Fix type errors only
    2: Improve security
    3: Refactor for complexity
    4: Add documentation
    5: Optimize performance
    6: Quick syntax fix
    7: Comprehensive review (all above)
    """

    action_id: int
    name: str
    description: str
    expected_time_seconds: float
    expected_cost_usd: float


# Define action space
REFINEMENT_ACTIONS = [
    RefinementAction(0, "run_tests", "Run full test suite", 30.0, 0.01),
    RefinementAction(1, "fix_types", "Fix type errors", 15.0, 0.05),
    RefinementAction(2, "improve_security", "Address security vulnerabilities", 20.0, 0.08),
    RefinementAction(3, "reduce_complexity", "Refactor complex code", 45.0, 0.12),
    RefinementAction(4, "add_docs", "Add missing documentation", 10.0, 0.03),
    RefinementAction(5, "optimize_performance", "Optimize slow code paths", 40.0, 0.10),
    RefinementAction(6, "quick_fix", "Quick syntax/lint fixes", 5.0, 0.02),
    RefinementAction(7, "comprehensive_review", "Full comprehensive review", 60.0, 0.15),
]


@dataclass
class RefinementReward:
    """
    Reward Signal für RL Agent.

    Komponenten:
    - Quality Improvement: +1 per 10% quality increase
    - Time Efficiency: Penalty for excessive time
    - Cost Efficiency: Penalty for high cost
    - Success Bonus: +5 if target quality reached
    """

    quality_delta: float  # Change in overall quality
    time_penalty: float
    cost_penalty: float
    success_bonus: float

    def total_reward(self) -> float:
        """Berechnet Gesamt-Reward."""
        return (
            self.quality_delta * 10.0  # 10 points per 10% quality improvement
            - self.time_penalty
            - self.cost_penalty
            + self.success_bonus
        )


class SimplePPOAgent:
    """
    Simplified PPO Agent für Refinement Strategy Learning.

    Vereinfachte Implementierung mit:
    - Neural Network approximation (simplified to linear model)
    - Experience replay buffer
    - Policy gradient updates
    """

    def __init__(
        self,
        state_dim: int = 20,
        action_dim: int = 8,
        learning_rate: float = 0.001,
        gamma: float = 0.99,
        clip_epsilon: float = 0.2
    ):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = learning_rate
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon

        # Simple linear policy (state_dim × action_dim weights)
        # In production, use PyTorch/TensorFlow neural network
        self.policy_weights = np.random.randn(state_dim, action_dim) * 0.1
        self.value_weights = np.random.randn(state_dim) * 0.1

        # Experience buffer
        self.buffer = deque(maxlen=10000)

    def get_action_probabilities(self, state: np.ndarray) -> np.ndarray:
        """
        Berechnet Action Probabilities via Policy Network.

        Args:
            state: State vector

        Returns:
            Probability distribution over actions
        """
        # Linear layer + softmax
        logits = state @ self.policy_weights
        exp_logits = np.exp(logits - np.max(logits))  # Numerical stability
        probabilities = exp_logits / np.sum(exp_logits)

        return probabilities

    def select_action(self, state: RefinementState, epsilon: float = 0.1) -> int:
        """
        Selektiert Action via ε-greedy policy.

        Args:
            state: Current refinement state
            epsilon: Exploration rate

        Returns:
            Action ID (0-7)
        """
        state_vector = state.to_vector()

        # ε-greedy exploration
        if random.random() < epsilon:
            return random.randint(0, self.action_dim - 1)

        # Exploitation: sample from policy
        probabilities = self.get_action_probabilities(state_vector)
        action = np.random.choice(self.action_dim, p=probabilities)

        return action

    def get_value(self, state: np.ndarray) -> float:
        """Estimates state value."""
        return float(state @ self.value_weights)

    def store_experience(
        self,
        state: RefinementState,
        action: int,
        reward: float,
        next_state: RefinementState,
        done: bool
    ):
        """Stores experience in replay buffer."""
        self.buffer.append({
            'state': state.to_vector(),
            'action': action,
            'reward': reward,
            'next_state': next_state.to_vector(),
            'done': done
        })

    def update_policy(self, batch_size: int = 32):
        """
        Updates policy using PPO algorithm (simplified).

        In production:
        - Use full PPO with clipped objective
        - Separate actor/critic networks
        - Multiple epochs per update
        - Advantage estimation (GAE)
        """
        if len(self.buffer) < batch_size:
            return

        # Sample batch
        batch = random.sample(self.buffer, batch_size)

        # Compute gradients (simplified gradient ascent)
        for experience in batch:
            state = experience['state']
            action = experience['action']
            reward = experience['reward']
            next_state = experience['next_state']
            done = experience['done']

            # Compute advantage (TD error)
            current_value = self.get_value(state)
            next_value = 0.0 if done else self.get_value(next_state)
            advantage = reward + self.gamma * next_value - current_value

            # Policy gradient update (simplified)
            probabilities = self.get_action_probabilities(state)
            action_prob = probabilities[action]

            # Gradient for policy (increase prob of good actions)
            grad_policy = np.outer(state, np.zeros(self.action_dim))
            grad_policy[:, action] = state * advantage / (action_prob + 1e-8)

            self.policy_weights += self.lr * grad_policy

            # Value function update
            value_error = advantage
            grad_value = state * value_error

            self.value_weights += self.lr * grad_value

    def save(self, path: Path):
        """Saves agent weights."""
        np.savez(
            path,
            policy_weights=self.policy_weights,
            value_weights=self.value_weights
        )

    def load(self, path: Path):
        """Loads agent weights."""
        data = np.load(path)
        self.policy_weights = data['policy_weights']
        self.value_weights = data['value_weights']


class RLRefinementChain:
    """
    Turing-Complete Refinement Chain with RL Strategy Selection.

    Workflow:
    1. Encode current code state
    2. Agent selects refinement action
    3. Execute action, observe reward
    4. Update policy
    5. Repeat until quality target or max iterations
    """

    def __init__(
        self,
        agent: Optional[SimplePPOAgent] = None,
        target_quality: float = 85.0,
        max_iterations: int = 10
    ):
        self.agent = agent or SimplePPOAgent()
        self.target_quality = target_quality
        self.max_iterations = max_iterations

        # Training stats
        self.episode_count = 0
        self.total_reward = 0.0
        self.success_count = 0

    def run_refinement_loop(
        self,
        initial_state: RefinementState,
        executor_callback: callable,
        exploration_rate: float = 0.1
    ) -> Dict:
        """
        Runs complete refinement loop with RL agent.

        Args:
            initial_state: Initial code quality state
            executor_callback: Function(action_id) -> (new_state, metrics)
            exploration_rate: ε for ε-greedy

        Returns:
            {
                'final_state': RefinementState,
                'total_reward': float,
                'actions_taken': List[int],
                'success': bool
            }
        """
        state = initial_state
        actions_taken = []
        total_reward = 0.0
        episode_rewards = []

        for iteration in range(self.max_iterations):
            # Select action
            action_id = self.agent.select_action(state, epsilon=exploration_rate)
            action = REFINEMENT_ACTIONS[action_id]

            print(f"Iteration {iteration + 1}: Selected action '{action.name}'")

            # Execute action
            new_state, execution_metrics = executor_callback(action_id)

            # Compute reward
            reward = self._compute_reward(
                state,
                new_state,
                action,
                execution_metrics
            )

            # Store experience
            done = (
                self._get_overall_quality(new_state) >= self.target_quality
                or iteration == self.max_iterations - 1
            )

            self.agent.store_experience(state, action_id, reward, new_state, done)

            # Update stats
            actions_taken.append(action_id)
            total_reward += reward
            episode_rewards.append(reward)

            # Check termination
            if done:
                if self._get_overall_quality(new_state) >= self.target_quality:
                    print(f"✓ Target quality {self.target_quality}% reached!")
                    self.success_count += 1
                break

            state = new_state

        # Update policy after episode
        self.agent.update_policy(batch_size=min(32, len(self.agent.buffer)))

        self.episode_count += 1
        self.total_reward += total_reward

        return {
            'final_state': state,
            'total_reward': total_reward,
            'actions_taken': actions_taken,
            'success': self._get_overall_quality(state) >= self.target_quality,
            'episode_rewards': episode_rewards
        }

    def _compute_reward(
        self,
        old_state: RefinementState,
        new_state: RefinementState,
        action: RefinementAction,
        execution_metrics: Dict
    ) -> float:
        """
        Computes reward signal for RL agent.

        Reward components:
        - Quality improvement: Primary goal
        - Time efficiency: Faster is better
        - Cost efficiency: Cheaper is better
        - Success bonus: Large bonus for reaching target
        """
        old_quality = self._get_overall_quality(old_state)
        new_quality = self._get_overall_quality(new_state)

        quality_delta = new_quality - old_quality

        # Time penalty (penalize if took longer than expected)
        actual_time = execution_metrics.get('time_seconds', action.expected_time_seconds)
        time_penalty = max(0, (actual_time - action.expected_time_seconds) / 10.0)

        # Cost penalty
        actual_cost = execution_metrics.get('cost_usd', action.expected_cost_usd)
        cost_penalty = (actual_cost - action.expected_cost_usd) * 10.0

        # Success bonus
        success_bonus = 5.0 if new_quality >= self.target_quality else 0.0

        reward_obj = RefinementReward(
            quality_delta=quality_delta,
            time_penalty=time_penalty,
            cost_penalty=max(0, cost_penalty),
            success_bonus=success_bonus
        )

        return reward_obj.total_reward()

    def _get_overall_quality(self, state: RefinementState) -> float:
        """
        Computes overall quality score from state.

        Weighted average of all quality dimensions.
        """
        weights = {
            'test_coverage': 0.20,
            'security_score': 0.20,
            'complexity_score': 0.15,
            'documentation_score': 0.10,
            'type_safety_score': 0.15,
            'performance_score': 0.10,
            'maintainability_score': 0.10,
        }

        overall = (
            state.test_coverage * weights['test_coverage'] +
            state.security_score * weights['security_score'] +
            state.complexity_score * weights['complexity_score'] +
            state.documentation_score * weights['documentation_score'] +
            state.type_safety_score * weights['type_safety_score'] +
            state.performance_score * weights['performance_score'] +
            state.maintainability_score * weights['maintainability_score']
        )

        return overall

    def get_training_stats(self) -> Dict:
        """Returns training statistics."""
        return {
            'episode_count': self.episode_count,
            'success_count': self.success_count,
            'success_rate': self.success_count / max(1, self.episode_count),
            'avg_reward': self.total_reward / max(1, self.episode_count),
            'buffer_size': len(self.agent.buffer)
        }

    def save_agent(self, path: Path):
        """Saves trained agent."""
        self.agent.save(path)
        print(f"Agent saved to {path}")

    def load_agent(self, path: Path):
        """Loads trained agent."""
        self.agent.load(path)
        print(f"Agent loaded from {path}")


# Export
__all__ = [
    'RefinementState',
    'RefinementAction',
    'RefinementReward',
    'SimplePPOAgent',
    'RLRefinementChain',
    'REFINEMENT_ACTIONS'
]
