"""
Quality Feedback Aggregator

Aggregates quality analysis data for guideline evolution.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


class FeedbackAggregator:
    """
    Aggregates quality feedback for guideline evolution.

    Provides insights into agent performance patterns based on
    quality analyzer rewards/penalties.
    """

    def __init__(self, lookback_hours: int = 24):
        self.lookback_hours = lookback_hours

    async def aggregate_feedback(self, db: AsyncSession) -> Dict:
        """
        Aggregate quality feedback from recent tasks.

        Returns:
            Dict with high_reward_patterns, high_penalty_patterns, guideline_gaps
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=self.lookback_hours)

        # This would query the quality_feedback table (to be added to models.py)
        # For now, return structure template

        insights = {
            "high_reward_patterns": [],
            "high_penalty_patterns": [],
            "guideline_gaps": [],
            "agent_performance": {}
        }

        logger.info(f"Aggregated feedback from last {self.lookback_hours} hours")

        return insights


# Global aggregator instance
_aggregator: Optional[FeedbackAggregator] = None


def get_feedback_aggregator() -> FeedbackAggregator:
    """Get global feedback aggregator instance."""
    global _aggregator

    if _aggregator is None:
        _aggregator = FeedbackAggregator()

    return _aggregator
