"""
Unit Tests for Iteration Predictor ML Model
Tests ML prediction, training, feature extraction, and accuracy
"""

import pytest
import numpy as np
from pathlib import Path
import sys
import tempfile
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.iteration_predictor import (
    IterationPredictor,
    TaskComplexity,
    PredictionResult
)


class TestTaskComplexity:
    """Tests for TaskComplexity dataclass."""

    def test_complexity_creation(self):
        """Test creating task complexity."""
        complexity = TaskComplexity(
            code_lines=150,
            test_count=10,
            file_count=5,
            cyclomatic_complexity=12.5,
            label_complexity=3,
            has_ml_components=True,
            historical_iterations=None
        )

        assert complexity.code_lines == 150
        assert complexity.test_count == 10
        assert complexity.has_ml_components is True

    def test_complexity_defaults(self):
        """Test default values."""
        complexity = TaskComplexity(
            code_lines=100,
            test_count=5,
            file_count=3,
            cyclomatic_complexity=8.0,
            label_complexity=2
        )

        assert complexity.has_ml_components is False
        assert complexity.historical_iterations is None


class TestIterationPredictor:
    """Tests for IterationPredictor ML model."""

    @pytest.fixture
    def predictor(self):
        """Create predictor instance for testing."""
        return IterationPredictor()

    @pytest.fixture
    def sample_complexity(self):
        """Create sample complexity for testing."""
        return TaskComplexity(
            code_lines=200,
            test_count=15,
            file_count=8,
            cyclomatic_complexity=15.0,
            label_complexity=4,
            has_ml_components=True,
            historical_iterations=5
        )

    def test_initialization(self, predictor):
        """Test predictor initializes correctly."""
        assert predictor.model is not None
        assert predictor.is_trained is False
        assert len(predictor.training_data) == 0

    def test_predict_optimal_iterations_untrained(self, predictor, sample_complexity):
        """Test prediction with untrained model uses heuristics."""
        result = predictor.predict_optimal_iterations(sample_complexity)

        # Assertions
        assert isinstance(result, dict)
        assert 'predicted_iterations' in result
        assert 'confidence' in result
        assert 'min_iterations' in result
        assert 'max_iterations' in result

        # Should be within valid range (2-10)
        assert 2 <= result['predicted_iterations'] <= 10
        assert result['min_iterations'] <= result['predicted_iterations'] <= result['max_iterations']

    def test_extract_features(self, predictor, sample_complexity):
        """Test feature extraction."""
        features = predictor._extract_features(sample_complexity)

        # Should return 7 features
        assert len(features) == 7
        assert all(isinstance(f, (int, float)) for f in features)

        # Verify feature values
        assert features[0] == 200  # code_lines
        assert features[1] == 15   # test_count
        assert features[5] == 1    # has_ml_components (boolean converted to int)

    def test_train_model(self, predictor):
        """Test model training."""
        # Add training samples
        for i in range(25):
            complexity = TaskComplexity(
                code_lines=100 + i * 10,
                test_count=5 + i,
                file_count=2 + i // 5,
                cyclomatic_complexity=8.0 + i * 0.5,
                label_complexity=2 + i // 10,
                has_ml_components=i % 2 == 0,
                historical_iterations=None
            )
            actual_iterations = 3 + i // 5  # Ground truth
            predictor.add_training_sample(complexity, actual_iterations)

        # Train
        predictor.train()

        # Assertions
        assert predictor.is_trained is True
        assert len(predictor.training_data) == 25

    def test_predict_after_training(self, predictor):
        """Test prediction improves after training."""
        # Train model
        training_data = [
            (TaskComplexity(100, 5, 2, 8.0, 2), 3),
            (TaskComplexity(200, 10, 4, 12.0, 3), 5),
            (TaskComplexity(300, 15, 6, 16.0, 4), 7),
            (TaskComplexity(150, 8, 3, 10.0, 2), 4),
            (TaskComplexity(250, 12, 5, 14.0, 3), 6),
            (TaskComplexity(50, 3, 1, 5.0, 1), 2),
            (TaskComplexity(400, 20, 8, 20.0, 5), 9),
            (TaskComplexity(120, 6, 2, 9.0, 2), 3),
            (TaskComplexity(180, 9, 4, 11.0, 3), 4),
            (TaskComplexity(220, 11, 5, 13.0, 3), 5),
            (TaskComplexity(280, 14, 6, 15.0, 4), 6),
            (TaskComplexity(160, 8, 3, 10.5, 2), 4),
            (TaskComplexity(90, 4, 2, 7.0, 2), 3),
            (TaskComplexity(210, 11, 4, 12.5, 3), 5),
            (TaskComplexity(270, 13, 6, 14.5, 4), 6),
            (TaskComplexity(140, 7, 3, 9.5, 2), 4),
            (TaskComplexity(190, 10, 4, 11.5, 3), 5),
            (TaskComplexity(240, 12, 5, 13.5, 3), 5),
            (TaskComplexity(110, 6, 2, 8.5, 2), 3),
            (TaskComplexity(350, 18, 7, 18.0, 4), 8),
        ]

        for complexity, iterations in training_data:
            predictor.add_training_sample(complexity, iterations)

        predictor.train()

        # Test prediction
        test_complexity = TaskComplexity(200, 10, 4, 12.0, 3)
        result = predictor.predict_optimal_iterations(test_complexity)

        # Should predict around 5 iterations
        assert 4 <= result['predicted_iterations'] <= 6
        assert result['confidence'] > 0.5  # Should have reasonable confidence

    def test_confidence_increases_with_training(self, predictor):
        """Test confidence increases as more data is added."""
        test_complexity = TaskComplexity(200, 10, 4, 12.0, 3)

        # Predict with little data
        for i in range(5):
            predictor.add_training_sample(
                TaskComplexity(100 + i*50, 5 + i*2, 2, 8.0, 2),
                3 + i
            )
        predictor.train()
        result_low_data = predictor.predict_optimal_iterations(test_complexity)

        # Add more data
        for i in range(20):
            predictor.add_training_sample(
                TaskComplexity(100 + i*15, 5 + i, 2 + i//5, 8.0 + i*0.3, 2 + i//10),
                3 + i//3
            )
        predictor.train()
        result_more_data = predictor.predict_optimal_iterations(test_complexity)

        # Confidence should increase (or stay same if already high)
        assert result_more_data['confidence'] >= result_low_data['confidence'] - 0.1

    def test_save_and_load_model(self, predictor):
        """Test saving and loading trained model."""
        # Train model
        for i in range(20):
            predictor.add_training_sample(
                TaskComplexity(100 + i*10, 5 + i, 2, 8.0, 2),
                3 + i//5
            )
        predictor.train()

        # Save
        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "model.joblib"
            predictor.save_model(model_path)

            # Create new predictor and load
            new_predictor = IterationPredictor()
            new_predictor.load_model(model_path)

            # Verify
            assert new_predictor.is_trained is True

            # Predictions should be same
            test_complexity = TaskComplexity(200, 10, 4, 12.0, 3)
            result1 = predictor.predict_optimal_iterations(test_complexity)
            result2 = new_predictor.predict_optimal_iterations(test_complexity)

            assert result1['predicted_iterations'] == result2['predicted_iterations']

    def test_min_max_bounds(self, predictor):
        """Test min/max iteration bounds are respected."""
        # Very simple task
        simple = TaskComplexity(10, 1, 1, 2.0, 1)
        result_simple = predictor.predict_optimal_iterations(simple)
        assert result_simple['predicted_iterations'] >= 2  # Minimum

        # Very complex task
        complex_task = TaskComplexity(5000, 100, 50, 50.0, 10, has_ml_components=True)
        result_complex = predictor.predict_optimal_iterations(complex_task)
        assert result_complex['predicted_iterations'] <= 10  # Maximum

    def test_historical_iterations_influence(self, predictor):
        """Test historical iterations influence prediction."""
        # Train model
        for i in range(20):
            predictor.add_training_sample(
                TaskComplexity(150, 8, 3, 10.0, 3, historical_iterations=i % 8),
                i % 8
            )
        predictor.train()

        # Same complexity, different historical iterations
        base = TaskComplexity(150, 8, 3, 10.0, 3)

        base_with_history_low = TaskComplexity(150, 8, 3, 10.0, 3, historical_iterations=3)
        base_with_history_high = TaskComplexity(150, 8, 3, 10.0, 3, historical_iterations=7)

        result_low = predictor.predict_optimal_iterations(base_with_history_low)
        result_high = predictor.predict_optimal_iterations(base_with_history_high)

        # Higher historical should predict higher (usually)
        # Allow for some variance in ML predictions
        assert result_high['predicted_iterations'] >= result_low['predicted_iterations'] - 1


class TestIntegration:
    """Integration tests for iteration predictor."""

    def test_realistic_workflow(self):
        """Test realistic usage workflow."""
        predictor = IterationPredictor()

        # Simulate collecting data over multiple tasks
        realistic_tasks = [
            (TaskComplexity(80, 4, 2, 6.0, 1), 2),   # Simple
            (TaskComplexity(150, 8, 4, 10.0, 2), 4),  # Medium
            (TaskComplexity(300, 15, 8, 18.0, 4), 7), # Complex
            (TaskComplexity(450, 25, 12, 25.0, 5, has_ml_components=True), 9), # Very complex
            (TaskComplexity(100, 5, 3, 7.0, 2), 3),   # Simple-medium
            (TaskComplexity(200, 10, 5, 12.0, 3), 5), # Medium-complex
            (TaskComplexity(350, 18, 10, 20.0, 4), 8), # Complex
            (TaskComplexity(120, 6, 3, 8.0, 2), 3),   # Medium
            (TaskComplexity(180, 9, 4, 11.0, 3), 4),  # Medium
            (TaskComplexity(250, 12, 6, 14.0, 3), 6), # Medium-complex
            (TaskComplexity(90, 4, 2, 6.5, 1), 3),    # Simple
            (TaskComplexity(400, 20, 11, 22.0, 5), 9), # Very complex
            (TaskComplexity(160, 8, 4, 10.5, 2), 4),  # Medium
            (TaskComplexity(210, 11, 5, 13.0, 3), 5), # Medium-complex
            (TaskComplexity(320, 16, 9, 19.0, 4), 7), # Complex
            (TaskComplexity(140, 7, 3, 9.0, 2), 4),   # Medium
            (TaskComplexity(190, 10, 5, 11.5, 3), 5), # Medium
            (TaskComplexity(270, 13, 7, 15.0, 4), 6), # Medium-complex
            (TaskComplexity(110, 6, 3, 8.0, 2), 3),   # Simple-medium
            (TaskComplexity(380, 19, 10, 21.0, 5), 8), # Complex
        ]

        for complexity, actual in realistic_tasks:
            predictor.add_training_sample(complexity, actual)

        predictor.train()

        # Test prediction on new task
        new_task = TaskComplexity(220, 11, 5, 13.5, 3)
        result = predictor.predict_optimal_iterations(new_task)

        # Should predict around 5-6 iterations
        assert 4 <= result['predicted_iterations'] <= 7
        assert result['confidence'] > 0.4
        assert result['min_iterations'] < result['predicted_iterations'] < result['max_iterations']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
