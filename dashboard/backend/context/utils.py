"""
Context Management Utilities

Token counting and helper functions for context management.
"""

import logging
from typing import Optional
from functools import lru_cache

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logging.warning("tiktoken not available - using estimation for token counting")

from .models import ModelType

logger = logging.getLogger(__name__)


# Model context limits (in tokens)
MODEL_LIMITS = {
    ModelType.CLAUDE: 200000,  # Claude 3.5 Sonnet
    ModelType.GEMINI: 1000000,  # Gemini 2.0 Flash
    ModelType.GPT4: 128000,     # GPT-4 Turbo
    ModelType.GPT35: 16385,     # GPT-3.5 Turbo
    ModelType.OLLAMA: 8192,     # Default for Ollama models
}


# Encoding names for tiktoken
MODEL_ENCODINGS = {
    ModelType.CLAUDE: "cl100k_base",  # Claude uses cl100k_base
    ModelType.GPT4: "cl100k_base",
    ModelType.GPT35: "cl100k_base",
    ModelType.GEMINI: "cl100k_base",  # Use cl100k_base for estimation
    ModelType.OLLAMA: "cl100k_base",  # Use cl100k_base for estimation
}


@lru_cache(maxsize=10)
def get_encoding(model: ModelType) -> Optional[any]:
    """
    Get tiktoken encoding for a model.
    
    Args:
        model: Model type
        
    Returns:
        Tiktoken encoding or None if not available
    """
    if not TIKTOKEN_AVAILABLE:
        return None
    
    try:
        encoding_name = MODEL_ENCODINGS.get(model, "cl100k_base")
        return tiktoken.get_encoding(encoding_name)
    except Exception as e:
        logger.error(f"Failed to get tiktoken encoding: {e}")
        return None


def count_tokens(text: str, model: ModelType = ModelType.CLAUDE) -> int:
    """
    Count tokens in text for a given model.
    
    Uses tiktoken for accurate counting when available,
    falls back to estimation based on characters.
    
    Args:
        text: Text to count tokens for
        model: Model type to use for counting
        
    Returns:
        Number of tokens
    """
    if not text:
        return 0
    
    # Try tiktoken first
    if TIKTOKEN_AVAILABLE:
        try:
            encoding = get_encoding(model)
            if encoding:
                return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"tiktoken encoding failed: {e}, falling back to estimation")
    
    # Fallback: estimate tokens
    # Rough estimation: 1 token ≈ 4 characters for English text
    return len(text) // 4


def get_model_limit(model: ModelType) -> int:
    """
    Get context window limit for a model.
    
    Args:
        model: Model type
        
    Returns:
        Maximum tokens for model's context window
    """
    return MODEL_LIMITS.get(model, 8192)


def estimate_tokens_from_messages(messages: list, model: ModelType = ModelType.CLAUDE) -> int:
    """
    Estimate total tokens from a list of messages.
    
    Args:
        messages: List of message dicts with 'content' key
        model: Model type to use for counting
        
    Returns:
        Estimated total tokens
    """
    total = 0
    for msg in messages:
        content = msg.get("content", "")
        total += count_tokens(content, model)
        # Add overhead for message formatting (role, etc.)
        total += 4  # Rough estimate for message overhead
    
    return total


def format_token_count(tokens: int) -> str:
    """
    Format token count for display.
    
    Args:
        tokens: Number of tokens
        
    Returns:
        Formatted string (e.g., "1.5K", "2.3M")
    """
    if tokens < 1000:
        return str(tokens)
    elif tokens < 1000000:
        return f"{tokens / 1000:.1f}K"
    else:
        return f"{tokens / 1000000:.1f}M"


def calculate_usage_color(usage_percent: float) -> str:
    """
    Get color indicator for usage percentage.
    
    Args:
        usage_percent: Usage percentage (0-100)
        
    Returns:
        Color name: 'green', 'yellow', 'red'
    """
    if usage_percent < 60:
        return 'green'
    elif usage_percent < 80:
        return 'yellow'
    else:
        return 'red'
