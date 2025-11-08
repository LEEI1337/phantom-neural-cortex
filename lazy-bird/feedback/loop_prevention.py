#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Infinite Loop Prevention

Detects and prevents infinite feedback loops through multiple strategies.
"""

import sys
import io
import time
import hashlib
import logging
from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logger = logging.getLogger(__name__)


@dataclass
class LoopMetrics:
    """Metrics for feedback loop execution."""

    iterations: int
    total_time: float  # seconds
    quality_progression: List[float] = field(default_factory=list)
    stagnation_detected: bool = False
    halt_reason: str = ""
    total_cost: float = 0.0  # $
    agent_used: str = ""


class InfiniteLoopPrevention:
    """Prevents infinite feedback loops using multiple strategies."""

    def __init__(
        self,
        max_iterations: int = 5,
        min_quality_threshold: float = 0.60,
        stagnation_window: int = 3,
        max_cost: float = 5.0,
        max_time: float = 1800.0  # 30 minutes
    ):
        """Initialize loop prevention.

        Args:
            max_iterations: Hard iteration limit
            min_quality_threshold: Minimum quality after N iterations
            stagnation_window: Window for stagnation detection
            max_cost: Maximum cost in dollars
            max_time: Maximum time in seconds
        """
        self.MAX_ITERATIONS = max_iterations
        self.MIN_QUALITY_THRESHOLD = min_quality_threshold
        self.STAGNATION_WINDOW = stagnation_window
        self.MAX_COST = max_cost
        self.MAX_TIME = max_time

        # State tracking
        self.quality_history: List[float] = []
        self.feedback_hashes: List[str] = []
        self.start_time: Optional[float] = None
        self.total_cost: float = 0.0

    def start_tracking(self):
        """Start tracking time."""
        self.start_time = time.time()
        self.quality_history = []
        self.feedback_hashes = []
        self.total_cost = 0.0

    def add_iteration(
        self,
        quality: float,
        feedback: str,
        cost: float = 0.0
    ):
        """Track iteration metrics.

        Args:
            quality: Quality score (0.0 - 1.0)
            feedback: Feedback string
            cost: Cost of this iteration ($)
        """
        self.quality_history.append(quality)
        self.total_cost += cost

        # Hash feedback to detect cycles
        h = hashlib.md5(feedback.encode()).hexdigest()
        self.feedback_hashes.append(h)

    def is_stagnating(self) -> bool:
        """Detect if quality improvements have stalled.

        Returns:
            True if stagnating, False otherwise
        """
        if len(self.quality_history) < self.STAGNATION_WINDOW:
            return False

        recent = self.quality_history[-self.STAGNATION_WINDOW:]

        # Strategy 1: Check variance (no improvement)
        variance = np.var(recent)
        if variance < 0.001:  # Almost no change
            logger.warning(f"Stagnation detected: variance={variance:.6f}")
            return True

        # Strategy 2: Check if declining
        if all(recent[i] >= recent[i+1] for i in range(len(recent)-1)):
            logger.warning("Quality degradation detected")
            return True

        # Strategy 3: Check if stuck at low quality
        if all(q < self.MIN_QUALITY_THRESHOLD for q in recent):
            logger.warning(f"Stuck at low quality: {recent}")
            return True

        return False

    def is_cycling(self) -> bool:
        """Detect if feedback is cycling (same feedback repeating).

        Returns:
            True if cycling detected, False otherwise
        """
        if len(self.feedback_hashes) < 2:
            return False

        # Check if same feedback hash appears 2x in a row
        if self.feedback_hashes[-1] == self.feedback_hashes[-2]:
            logger.warning("Feedback cycle detected (same feedback 2x)")
            return True

        # Check if same feedback appears 3x in last 5 iterations
        if len(self.feedback_hashes) >= 5:
            recent = self.feedback_hashes[-5:]
            unique = set(recent)
            if len(unique) < 3:  # Less than 3 unique feedback in 5 iterations
                logger.warning(f"Feedback cycle detected: {len(unique)} unique in 5")
                return True

        return False

    def should_abort(
        self,
        iteration: int,
        quality: float
    ) -> tuple[bool, str]:
        """Decide if loop should be aborted.

        Args:
            iteration: Current iteration number
            quality: Current quality score

        Returns:
            Tuple of (should_abort, reason)
        """
        # Strategy 1: Hard iteration limit
        if iteration >= self.MAX_ITERATIONS:
            return True, f"max_iterations_reached ({self.MAX_ITERATIONS})"

        # Strategy 2: Quality stagnation
        if self.is_stagnating():
            return True, "quality_stagnation"

        # Strategy 3: Quality too low after multiple tries
        if iteration >= 3 and quality < self.MIN_QUALITY_THRESHOLD:
            return True, f"quality_too_low ({quality:.2f} < {self.MIN_QUALITY_THRESHOLD})"

        # Strategy 4: Feedback cycling
        if self.is_cycling():
            return True, "feedback_cycling"

        # Strategy 5: Cost limit
        if self.total_cost > self.MAX_COST:
            return True, f"cost_limit_exceeded (${self.total_cost:.2f} > ${self.MAX_COST})"

        # Strategy 6: Time limit
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            if elapsed > self.MAX_TIME:
                return True, f"time_limit_exceeded ({elapsed:.0f}s > {self.MAX_TIME:.0f}s)"

        return False, ""

    def get_metrics(self, halt_reason: str, agent: str = "") -> LoopMetrics:
        """Get loop execution metrics.

        Args:
            halt_reason: Reason for halting
            agent: Agent used (claude/gemini/copilot)

        Returns:
            LoopMetrics object
        """
        total_time = 0.0
        if self.start_time is not None:
            total_time = time.time() - self.start_time

        return LoopMetrics(
            iterations=len(self.quality_history),
            total_time=total_time,
            quality_progression=self.quality_history.copy(),
            stagnation_detected=self.is_stagnating(),
            halt_reason=halt_reason,
            total_cost=self.total_cost,
            agent_used=agent
        )

    def reset(self):
        """Reset state for new loop."""
        self.quality_history = []
        self.feedback_hashes = []
        self.start_time = None
        self.total_cost = 0.0
