"""
Langfuse Observability Integration (Optional)

Provides observability for multi-agent orchestration:
- Trace agent execution flows
- Monitor token usage and costs
- Track performance metrics
- Debug agent chains

Requires: pip install langfuse
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class LangfuseObserver:
    """
    Optional Langfuse integration for agent observability.

    Features:
    - Trace agent execution
    - Monitor costs and tokens
    - Track performance metrics
    - Debug multi-agent chains

    Environment Variables:
    - LANGFUSE_PUBLIC_KEY: Langfuse public key
    - LANGFUSE_SECRET_KEY: Langfuse secret key
    - LANGFUSE_HOST: Langfuse host (default: https://cloud.langfuse.com)
    """

    def __init__(self):
        self.enabled = False
        self.langfuse = None

        # Try to import and initialize Langfuse
        try:
            from langfuse import Langfuse

            public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
            secret_key = os.getenv("LANGFUSE_SECRET_KEY")
            host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

            if public_key and secret_key:
                self.langfuse = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=host
                )
                self.enabled = True
                logger.info(f"Langfuse observability enabled (host: {host})")
            else:
                logger.info("Langfuse keys not found - observability disabled")

        except ImportError:
            logger.info("Langfuse not installed - observability disabled")
        except Exception as e:
            logger.warning(f"Failed to initialize Langfuse: {e}")

    @asynccontextmanager
    async def trace_agent_execution(
        self,
        task_id: str,
        agent: str,
        prompt: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Trace agent execution with context manager.

        Usage:
            async with observer.trace_agent_execution(
                task_id="task_1",
                agent="claude",
                prompt="Review code for security",
                metadata={"task_type": "security"}
            ) as trace:
                response = await execute_agent()
                trace.update(
                    output=response.content,
                    tokens=response.tokens,
                    cost=response.cost
                )
        """
        if not self.enabled:
            # No-op if disabled
            yield _NoOpTrace()
            return

        try:
            # Create trace
            trace = self.langfuse.trace(
                name=f"{agent}_execution",
                id=task_id,
                metadata=metadata or {},
                input={"prompt": prompt}
            )

            # Create span for the execution
            span = trace.span(
                name=f"{agent}_cli_call",
                start_time=datetime.utcnow()
            )

            yield _LangfuseTrace(trace, span)

            # Finalize span
            span.end()

        except Exception as e:
            logger.warning(f"Langfuse tracing error: {e}")
            yield _NoOpTrace()

    def track_agent_selection(
        self,
        task_id: str,
        selected_agent: str,
        reason: str,
        all_rewards: Dict[str, float]
    ):
        """Track smart agent selection decisions"""
        if not self.enabled:
            return

        try:
            self.langfuse.event(
                name="agent_selection",
                trace_id=task_id,
                metadata={
                    "selected_agent": selected_agent,
                    "selection_reason": reason,
                    "reward_scores": all_rewards
                }
            )
        except Exception as e:
            logger.warning(f"Failed to track agent selection: {e}")

    def track_circuit_breaker_event(
        self,
        agent: str,
        state: str,
        failure_count: int
    ):
        """Track circuit breaker state changes"""
        if not self.enabled:
            return

        try:
            self.langfuse.event(
                name="circuit_breaker_state_change",
                metadata={
                    "agent": agent,
                    "state": state,
                    "failure_count": failure_count
                }
            )
        except Exception as e:
            logger.warning(f"Failed to track circuit breaker event: {e}")

    def flush(self):
        """Flush pending events to Langfuse"""
        if self.enabled and self.langfuse:
            try:
                self.langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to flush Langfuse events: {e}")


class _LangfuseTrace:
    """Wrapper for Langfuse trace with update capability"""

    def __init__(self, trace, span):
        self.trace = trace
        self.span = span

    def update(
        self,
        output: str = None,
        tokens: int = None,
        cost: float = None,
        metadata: Dict[str, Any] = None
    ):
        """Update trace with execution results"""
        try:
            if output:
                self.span.update(output={"content": output})

            if tokens or cost:
                usage_data = {}
                if tokens:
                    usage_data["total_tokens"] = tokens
                if cost:
                    usage_data["cost"] = cost

                self.span.update(usage=usage_data)

            if metadata:
                self.span.update(metadata=metadata)

        except Exception as e:
            logger.warning(f"Failed to update trace: {e}")


class _NoOpTrace:
    """No-op trace for when Langfuse is disabled"""

    def update(self, **kwargs):
        """No-op update"""
        pass


# Global observer instance
_observer: Optional[LangfuseObserver] = None


def get_langfuse_observer() -> LangfuseObserver:
    """Get or create global Langfuse observer"""
    global _observer
    if _observer is None:
        _observer = LangfuseObserver()
    return _observer
