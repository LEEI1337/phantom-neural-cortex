"""
Machine Learning & Reinforcement Learning Optimizations

This package implements ML/RL enhancements for Phantom Neural Cortex:
- ML Iteration Prediction (ADR-002)
- RL Refinement Chain (ADR-011)
- Bayesian Weight Optimization (ADR-008)

Components:
- iteration_predictor.py: Random Forest prediction of optimal iterations
- rl_refinement_chain.py: PPO agent for adaptive task strategies
- weight_optimizer.py: Bayesian optimization of quality metric weights

Usage:
    from lazy_bird.ml import IterationPredictor, RLRefinementChain

    # Predict optimal iterations
    predictor = IterationPredictor()
    predicted_iterations = predictor.predict(task_features)

    # Use RL agent for refinement
    rl_agent = RLRefinementChain(state_dim=20, action_dim=8)
    action = rl_agent.select_action(state)
"""

__version__ = "1.0.0"
__author__ = "Phantom Neural Cortex Team"

from .iteration_predictor import IterationPredictor
from .rl_refinement_chain import RLRefinementChain, PPOAgent
from .weight_optimizer import BayesianWeightOptimizer

__all__ = [
    'IterationPredictor',
    'RLRefinementChain',
    'PPOAgent',
    'BayesianWeightOptimizer',
]
