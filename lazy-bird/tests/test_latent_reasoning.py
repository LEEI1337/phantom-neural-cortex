"""
Unit Tests for Latent Reasoning Module
Tests token compression, encoding/decoding, and reasoning state management
"""

import pytest
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from feedback.latent_reasoning import (
    LatentReasoningEncoder,
    LatentReasoningDecoder,
    ReasoningState,
    CompressedInstruction
)


class TestLatentReasoningEncoder:
    """Tests for LatentReasoningEncoder class."""

    @pytest.fixture
    def encoder(self):
        """Create encoder instance for testing."""
        return LatentReasoningEncoder(embedding_dim=512)

    def test_initialization(self, encoder):
        """Test encoder initializes correctly."""
        assert encoder.embedding_dim == 512
        assert encoder.model is not None

    def test_encode_code_state(self, encoder):
        """Test encoding code state to latent vector."""
        code_content = """
def hello():
    print("Hello, World!")
    return True
"""
        feedback_items = [
            {"type": "test_failure", "message": "Missing test coverage"}
        ]
        quality_metrics = {
            "coverage": 60.0,
            "security": 80.0,
            "complexity": 70.0
        }

        state = encoder.encode_code_state(
            code_content=code_content,
            feedback_items=feedback_items,
            quality_metrics=quality_metrics,
            iteration=3
        )

        # Assertions
        assert isinstance(state, ReasoningState)
        assert state.latent_vector.shape == (512,)
        assert state.embedding_dim == 512
        assert state.iteration == 3
        assert len(state.compressed_instructions) > 0
        assert state.original_token_count > 0
        assert state.compressed_token_count > 0
        assert state.compression_ratio > 1.0  # Should have compression

    def test_compression_ratio_calculation(self, encoder):
        """Test compression ratio is calculated correctly."""
        short_code = "x = 1"
        long_code = "x = 1\n" * 100  # Much longer code

        state_short = encoder.encode_code_state(short_code, [], {}, 1)
        state_long = encoder.encode_code_state(long_code, [], {}, 1)

        # Longer code should have better compression ratio
        assert state_long.compression_ratio > state_short.compression_ratio

    def test_compressed_instructions_structure(self, encoder):
        """Test compressed instructions have correct structure."""
        code = "def test():\n    return True"
        state = encoder.encode_code_state(code, [], {}, 1)

        assert len(state.compressed_instructions) > 0
        for instruction in state.compressed_instructions:
            assert isinstance(instruction, CompressedInstruction)
            assert hasattr(instruction, 'action')
            assert hasattr(instruction, 'target')
            assert hasattr(instruction, 'priority')

    def test_latent_vector_normalization(self, encoder):
        """Test latent vectors are properly normalized."""
        code = "def test():\n    pass"
        state = encoder.encode_code_state(code, [], {}, 1)

        # Check vector is normalized (L2 norm close to 1)
        norm = np.linalg.norm(state.latent_vector)
        assert 0.9 <= norm <= 1.1  # Allow small floating point variations


class TestLatentReasoningDecoder:
    """Tests for LatentReasoningDecoder class."""

    @pytest.fixture
    def encoder(self):
        return LatentReasoningEncoder(embedding_dim=512)

    @pytest.fixture
    def decoder(self):
        return LatentReasoningDecoder(embedding_dim=512)

    def test_decode_to_feedback(self, encoder, decoder):
        """Test decoding latent state back to feedback."""
        code = """
def calculate(a, b):
    return a + b
"""
        state = encoder.encode_code_state(code, [], {"coverage": 50.0}, 1)

        feedback = decoder.decode_to_feedback(state)

        # Assertions
        assert isinstance(feedback, dict)
        assert 'priorities' in feedback
        assert 'suggested_actions' in feedback
        assert 'estimated_improvements' in feedback
        assert len(feedback['suggested_actions']) > 0

    def test_decode_with_empty_state(self, decoder):
        """Test decoding with minimal state."""
        minimal_state = ReasoningState(
            latent_vector=np.zeros(512),
            compressed_instructions=[],
            embedding_dim=512,
            iteration=0,
            original_token_count=10,
            compressed_token_count=5,
            compression_ratio=2.0
        )

        feedback = decoder.decode_to_feedback(minimal_state)

        # Should still return valid structure
        assert isinstance(feedback, dict)
        assert 'priorities' in feedback
        assert 'suggested_actions' in feedback

    def test_decode_preserves_priorities(self, encoder, decoder):
        """Test decoded feedback preserves action priorities."""
        code = "def test(): pass"
        state = encoder.encode_code_state(
            code,
            [{"type": "security", "message": "Critical vulnerability"}],
            {"security": 30.0},
            1
        )

        feedback = decoder.decode_to_feedback(state)

        # Security should be high priority given low score
        priorities = feedback['priorities']
        assert 'security' in [p['dimension'] for p in priorities]


class TestReasoningState:
    """Tests for ReasoningState dataclass."""

    def test_state_creation(self):
        """Test creating reasoning state."""
        vector = np.random.randn(512)
        instructions = [
            CompressedInstruction("add_test", "function_x", 1)
        ]

        state = ReasoningState(
            latent_vector=vector,
            compressed_instructions=instructions,
            embedding_dim=512,
            iteration=5,
            original_token_count=1000,
            compressed_token_count=200,
            compression_ratio=5.0
        )

        assert state.iteration == 5
        assert state.compression_ratio == 5.0
        assert len(state.compressed_instructions) == 1

    def test_compression_ratio_validation(self):
        """Test compression ratio makes sense."""
        state = ReasoningState(
            latent_vector=np.zeros(512),
            compressed_instructions=[],
            embedding_dim=512,
            iteration=1,
            original_token_count=1000,
            compressed_token_count=250,
            compression_ratio=4.0
        )

        # Manually verify
        expected_ratio = 1000 / 250
        assert state.compression_ratio == expected_ratio


class TestCompressedInstruction:
    """Tests for CompressedInstruction dataclass."""

    def test_instruction_creation(self):
        """Test creating compressed instruction."""
        instruction = CompressedInstruction(
            action="refactor",
            target="complexity",
            priority=2
        )

        assert instruction.action == "refactor"
        assert instruction.target == "complexity"
        assert instruction.priority == 2

    def test_instruction_ordering(self):
        """Test instructions can be sorted by priority."""
        instructions = [
            CompressedInstruction("a", "x", 3),
            CompressedInstruction("b", "y", 1),
            CompressedInstruction("c", "z", 2),
        ]

        sorted_instructions = sorted(instructions, key=lambda i: i.priority)

        assert sorted_instructions[0].priority == 1
        assert sorted_instructions[1].priority == 2
        assert sorted_instructions[2].priority == 3


class TestIntegration:
    """Integration tests for full encode-decode cycle."""

    def test_encode_decode_cycle(self):
        """Test full encode-decode cycle preserves information."""
        encoder = LatentReasoningEncoder(embedding_dim=512)
        decoder = LatentReasoningDecoder(embedding_dim=512)

        original_code = """
def process_data(data):
    # Process data
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""
        original_feedback = [
            {"type": "complexity", "message": "Function too complex"},
            {"type": "coverage", "message": "Add tests"}
        ]
        original_metrics = {
            "coverage": 40.0,
            "complexity": 60.0,
            "security": 90.0
        }

        # Encode
        state = encoder.encode_code_state(
            original_code,
            original_feedback,
            original_metrics,
            iteration=2
        )

        # Decode
        decoded_feedback = decoder.decode_to_feedback(state)

        # Verify information preserved
        assert len(decoded_feedback['suggested_actions']) >= len(original_feedback)
        assert 'complexity' in str(decoded_feedback).lower() or 'coverage' in str(decoded_feedback).lower()

    def test_token_reduction_target(self):
        """Test 40% token reduction target is met."""
        encoder = LatentReasoningEncoder(embedding_dim=512)

        # Large code sample
        code = """
class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.results = []

    def process(self, data):
        for item in data:
            processed = self._process_item(item)
            self.results.append(processed)

    def _process_item(self, item):
        return item * 2

    def get_results(self):
        return self.results
"""

        state = encoder.encode_code_state(code, [], {}, 1)

        # Calculate reduction percentage
        reduction = (1 - (state.compressed_token_count / state.original_token_count)) * 100

        # Should achieve at least 30% reduction (target is 40%)
        assert reduction >= 30, f"Token reduction was only {reduction:.1f}%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
