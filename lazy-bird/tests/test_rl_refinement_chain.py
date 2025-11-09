"""
Unit Tests for RL Refinement Chain
Tests PPO agent, state encoding, action selection, and reward computation
"""

import pytest
import numpy as np
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.rl_refinement_chain import (
    RefinementState,
    RefinementAction,
    RefinementReward,
    SimplePPOAgent,
    RLRefinementChain,
    REFINEMENT_ACTIONS
)


class TestRefinementState:
    """Tests for RefinementState dataclass and vector conversion."""

    @pytest.fixture
    def sample_state(self):
        """Create sample refinement state."""
        return RefinementState(
            test_coverage=70.0,
            security_score=80.0,
            complexity_score=65.0,
            documentation_score=50.0,
            type_safety_score=75.0,
            performance_score=60.0,
            maintainability_score=70.0,
            current_iteration=3,
            max_iterations=10,
            time_elapsed_seconds=45.0,
            cost_usd=0.15,
            syntax_errors=2,
            type_errors=3,
            test_failures=1,
            security_vulnerabilities=0,
            action_history=[1, 3, 6]
        )

    def test_state_creation(self, sample_state):
        """Test creating refinement state."""
        assert sample_state.test_coverage == 70.0
        assert sample_state.current_iteration == 3
        assert len(sample_state.action_history) == 3

    def test_to_vector(self, sample_state):
        """Test converting state to feature vector."""
        vector = sample_state.to_vector()

        # Should return fixed-size vector
        assert isinstance(vector, np.ndarray)
        assert vector.shape == (20,)  # Updated: 7 quality + 3 iteration + 4 errors + 6 history
        assert vector.dtype == np.float32

        # All values should be normalized (0-1)
        assert np.all(vector >= 0.0)
        assert np.all(vector <= 1.0)

    def test_vector_normalization(self, sample_state):
        """Test feature normalization."""
        vector = sample_state.to_vector()

        # Quality metrics should be divided by 100
        assert vector[0] == pytest.approx(0.70, abs=0.01)  # test_coverage / 100
        assert vector[1] == pytest.approx(0.80, abs=0.01)  # security_score / 100

        # Iteration progress
        assert vector[7] == pytest.approx(0.30, abs=0.01)  # 3/10

    def test_action_history_encoding(self):
        """Test action history is encoded correctly."""
        state = RefinementState(
            test_coverage=70.0, security_score=80.0, complexity_score=65.0,
            documentation_score=50.0, type_safety_score=75.0,
            performance_score=60.0, maintainability_score=70.0,
            current_iteration=1, max_iterations=10,
            time_elapsed_seconds=10.0, cost_usd=0.05,
            syntax_errors=0, type_errors=0, test_failures=0,
            security_vulnerabilities=0,
            action_history=[3, 7]  # Last 2 actions
        )

        vector = state.to_vector()

        # Last 2 values should be normalized action IDs
        assert vector[-2] == pytest.approx(3/7.0, abs=0.01)
        assert vector[-1] == pytest.approx(7/7.0, abs=0.01)


class TestSimplePPOAgent:
    """Tests for SimplePPOAgent."""

    @pytest.fixture
    def agent(self):
        """Create PPO agent for testing."""
        return SimplePPOAgent(state_dim=20, action_dim=8)

    @pytest.fixture
    def sample_state(self):
        """Create sample state."""
        return RefinementState(
            test_coverage=60.0, security_score=70.0, complexity_score=65.0,
            documentation_score=40.0, type_safety_score=65.0,
            performance_score=55.0, maintainability_score=60.0,
            current_iteration=2, max_iterations=10,
            time_elapsed_seconds=30.0, cost_usd=0.10,
            syntax_errors=1, type_errors=2, test_failures=1,
            security_vulnerabilities=0,
            action_history=[0, 1]
        )

    def test_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent.state_dim == 20
        assert agent.action_dim == 8
        assert agent.policy_weights.shape == (20, 8)
        assert agent.value_weights.shape == (20,)
        assert len(agent.buffer) == 0

    def test_get_action_probabilities(self, agent, sample_state):
        """Test action probability computation."""
        state_vector = sample_state.to_vector()
        probs = agent.get_action_probabilities(state_vector)

        # Should return probability distribution
        assert probs.shape == (8,)
        assert np.all(probs >= 0.0)
        assert np.all(probs <= 1.0)
        assert np.abs(np.sum(probs) - 1.0) < 0.01  # Should sum to 1

    def test_select_action_exploration(self, agent, sample_state):
        """Test action selection with exploration."""
        # High epsilon → random actions
        action = agent.select_action(sample_state, epsilon=1.0)
        assert 0 <= action < 8

        # Zero epsilon → greedy
        action = agent.select_action(sample_state, epsilon=0.0)
        assert 0 <= action < 8

    def test_get_value(self, agent, sample_state):
        """Test state value estimation."""
        state_vector = sample_state.to_vector()
        value = agent.get_value(state_vector)

        assert isinstance(value, float)

    def test_store_experience(self, agent, sample_state):
        """Test storing experience in buffer."""
        next_state = RefinementState(
            test_coverage=65.0, security_score=75.0, complexity_score=70.0,
            documentation_score=45.0, type_safety_score=70.0,
            performance_score=60.0, maintainability_score=65.0,
            current_iteration=3, max_iterations=10,
            time_elapsed_seconds=45.0, cost_usd=0.15,
            syntax_errors=0, type_errors=1, test_failures=0,
            security_vulnerabilities=0,
            action_history=[0, 1, 2]
        )

        agent.store_experience(sample_state, 2, 5.0, next_state, False)

        assert len(agent.buffer) == 1
        assert agent.buffer[0]['action'] == 2
        assert agent.buffer[0]['reward'] == 5.0

    def test_update_policy(self, agent, sample_state):
        """Test policy update."""
        # Add some experiences
        for i in range(40):
            next_state = RefinementState(
                test_coverage=60.0 + i, security_score=70.0, complexity_score=65.0,
                documentation_score=40.0, type_safety_score=65.0,
                performance_score=55.0, maintainability_score=60.0,
                current_iteration=i % 10, max_iterations=10,
                time_elapsed_seconds=30.0, cost_usd=0.10,
                syntax_errors=0, type_errors=0, test_failures=0,
                security_vulnerabilities=0,
                action_history=[i % 8]
            )
            agent.store_experience(sample_state, i % 8, i * 0.1, next_state, i % 10 == 9)

        # Store weights before
        weights_before = agent.policy_weights.copy()

        # Update
        agent.update_policy(batch_size=32)

        # Weights should have changed
        assert not np.allclose(weights_before, agent.policy_weights)

    def test_save_load(self, agent):
        """Test saving and loading agent."""
        # Train a bit
        agent.policy_weights += 1.0  # Modify weights

        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = Path(tmpdir) / "agent.npz"

            # Save
            agent.save(save_path)
            assert save_path.exists()

            # Load into new agent
            new_agent = SimplePPOAgent(state_dim=20, action_dim=8)
            new_agent.load(save_path)

            # Weights should match
            assert np.allclose(agent.policy_weights, new_agent.policy_weights)
            assert np.allclose(agent.value_weights, new_agent.value_weights)


class TestRLRefinementChain:
    """Tests for RLRefinementChain."""

    @pytest.fixture
    def chain(self):
        """Create refinement chain."""
        agent = SimplePPOAgent(state_dim=20, action_dim=8)
        return RLRefinementChain(agent=agent, target_quality=85.0, max_iterations=10)

    @pytest.fixture
    def initial_state(self):
        """Create initial state."""
        return RefinementState(
            test_coverage=50.0, security_score=60.0, complexity_score=55.0,
            documentation_score=30.0, type_safety_score=55.0,
            performance_score=50.0, maintainability_score=50.0,
            current_iteration=0, max_iterations=10,
            time_elapsed_seconds=0.0, cost_usd=0.0,
            syntax_errors=3, type_errors=5, test_failures=4,
            security_vulnerabilities=2,
            action_history=[]
        )

    def test_initialization(self, chain):
        """Test chain initializes correctly."""
        assert chain.target_quality == 85.0
        assert chain.max_iterations == 10
        assert chain.episode_count == 0

    def test_compute_reward(self, chain):
        """Test reward computation."""
        old_state = RefinementState(
            test_coverage=50.0, security_score=60.0, complexity_score=55.0,
            documentation_score=30.0, type_safety_score=55.0,
            performance_score=50.0, maintainability_score=50.0,
            current_iteration=1, max_iterations=10,
            time_elapsed_seconds=10.0, cost_usd=0.05,
            syntax_errors=3, type_errors=5, test_failures=4,
            security_vulnerabilities=2,
            action_history=[0]
        )

        new_state = RefinementState(
            test_coverage=60.0, security_score=70.0, complexity_score=60.0,
            documentation_score=35.0, type_safety_score=60.0,
            performance_score=55.0, maintainability_score=55.0,
            current_iteration=2, max_iterations=10,
            time_elapsed_seconds=25.0, cost_usd=0.08,
            syntax_errors=2, type_errors=3, test_failures=2,
            security_vulnerabilities=1,
            action_history=[0, 1]
        )

        action = REFINEMENT_ACTIONS[1]  # fix_types
        execution_metrics = {'time_seconds': 15.0, 'cost_usd': 0.03}

        reward = chain._compute_reward(old_state, new_state, action, execution_metrics)

        # Reward should be positive (quality improved)
        assert isinstance(reward, float)
        # Quality improved, so reward should be positive
        assert reward > 0

    def test_get_overall_quality(self, chain, initial_state):
        """Test overall quality calculation."""
        quality = chain._get_overall_quality(initial_state)

        # Should be weighted average
        assert isinstance(quality, float)
        assert 0.0 <= quality <= 100.0

        # Should be around 48.5 given the input values
        assert 45.0 <= quality <= 55.0

    def test_run_refinement_loop(self, chain, initial_state):
        """Test running full refinement loop."""
        # Simple executor that improves quality
        iteration_count = 0

        def mock_executor(action_id):
            nonlocal iteration_count
            iteration_count += 1

            # Improve all metrics by 5 each iteration
            new_state = RefinementState(
                test_coverage=min(100, initial_state.test_coverage + iteration_count * 5),
                security_score=min(100, initial_state.security_score + iteration_count * 5),
                complexity_score=min(100, initial_state.complexity_score + iteration_count * 5),
                documentation_score=min(100, initial_state.documentation_score + iteration_count * 6),
                type_safety_score=min(100, initial_state.type_safety_score + iteration_count * 5),
                performance_score=min(100, initial_state.performance_score + iteration_count * 5),
                maintainability_score=min(100, initial_state.maintainability_score + iteration_count * 5),
                current_iteration=iteration_count,
                max_iterations=10,
                time_elapsed_seconds=iteration_count * 10.0,
                cost_usd=iteration_count * 0.05,
                syntax_errors=max(0, initial_state.syntax_errors - iteration_count),
                type_errors=max(0, initial_state.type_errors - iteration_count),
                test_failures=max(0, initial_state.test_failures - iteration_count),
                security_vulnerabilities=max(0, initial_state.security_vulnerabilities - iteration_count),
                action_history=initial_state.action_history + [action_id]
            )

            metrics = {'time_seconds': 10.0, 'cost_usd': 0.05}
            return new_state, metrics

        result = chain.run_refinement_loop(
            initial_state=initial_state,
            executor_callback=mock_executor,
            exploration_rate=0.1
        )

        # Assertions
        assert 'final_state' in result
        assert 'total_reward' in result
        assert 'actions_taken' in result
        assert 'success' in result

        # Should have taken some actions
        assert len(result['actions_taken']) > 0

        # Final quality should be higher
        final_quality = chain._get_overall_quality(result['final_state'])
        initial_quality = chain._get_overall_quality(initial_state)
        assert final_quality > initial_quality

    def test_training_stats(self, chain):
        """Test training statistics tracking."""
        stats = chain.get_training_stats()

        assert 'episode_count' in stats
        assert 'success_count' in stats
        assert 'success_rate' in stats
        assert 'avg_reward' in stats
        assert 'buffer_size' in stats


class TestRefinementActions:
    """Tests for predefined refinement actions."""

    def test_actions_defined(self):
        """Test all actions are defined."""
        assert len(REFINEMENT_ACTIONS) == 8

    def test_action_structure(self):
        """Test action structure."""
        for action in REFINEMENT_ACTIONS:
            assert isinstance(action, RefinementAction)
            assert hasattr(action, 'action_id')
            assert hasattr(action, 'name')
            assert hasattr(action, 'description')
            assert hasattr(action, 'expected_time_seconds')
            assert hasattr(action, 'expected_cost_usd')
            assert action.expected_time_seconds > 0
            assert action.expected_cost_usd > 0

    def test_action_ids_unique(self):
        """Test action IDs are unique."""
        ids = [action.action_id for action in REFINEMENT_ACTIONS]
        assert len(ids) == len(set(ids))

    def test_action_costs(self):
        """Test action costs are reasonable."""
        for action in REFINEMENT_ACTIONS:
            assert 0.01 <= action.expected_cost_usd <= 0.20
            assert 5 <= action.expected_time_seconds <= 120


class TestRefinementReward:
    """Tests for RefinementReward calculation."""

    def test_reward_creation(self):
        """Test creating reward."""
        reward = RefinementReward(
            quality_delta=10.0,
            time_penalty=2.0,
            cost_penalty=1.0,
            success_bonus=5.0
        )

        assert reward.quality_delta == 10.0
        assert reward.time_penalty == 2.0

    def test_total_reward_calculation(self):
        """Test total reward calculation."""
        reward = RefinementReward(
            quality_delta=10.0,   # +100 points (×10)
            time_penalty=2.0,      # -2 points
            cost_penalty=1.0,      # -1 point
            success_bonus=5.0      # +5 points
        )

        total = reward.total_reward()

        # 100 - 2 - 1 + 5 = 102
        assert total == pytest.approx(102.0)

    def test_negative_quality_delta(self):
        """Test reward with quality decrease."""
        reward = RefinementReward(
            quality_delta=-5.0,   # -50 points
            time_penalty=1.0,
            cost_penalty=0.5,
            success_bonus=0.0
        )

        total = reward.total_reward()

        # -50 - 1 - 0.5 + 0 = -51.5
        assert total == pytest.approx(-51.5)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
