"""
Prometheus Metrics Endpoint
Exposes metrics in Prometheus text format
"""

from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
import sys
from pathlib import Path

# Add lazy-bird to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'lazy-bird'))

from monitoring.prometheus_exporter import (
    LazyBirdPrometheusExporter,
    MetricConfig,
    MetricsAggregator
)
from ..database import get_db

router = APIRouter(prefix="/metrics", tags=["prometheus"])

# Global exporter instance (singleton)
_exporter = None
_aggregator = None


def get_exporter() -> LazyBirdPrometheusExporter:
    """Get or create singleton exporter instance."""
    global _exporter, _aggregator
    if _exporter is None:
        config = MetricConfig(
            enable_histograms=True,
            enable_summaries=True
        )
        _exporter = LazyBirdPrometheusExporter(config=config)
        _aggregator = MetricsAggregator(_exporter)
    return _exporter


def get_aggregator() -> MetricsAggregator:
    """Get singleton aggregator instance."""
    get_exporter()  # Ensure both are initialized
    return _aggregator


@router.get("")
async def metrics_endpoint(
    db: Session = Depends(get_db),
    exporter: LazyBirdPrometheusExporter = Depends(get_exporter),
    aggregator: MetricsAggregator = Depends(get_aggregator)
):
    """
    Prometheus metrics endpoint.

    Returns metrics in Prometheus text exposition format.

    Example Prometheus config:
    ```yaml
    scrape_configs:
      - job_name: 'lazy-bird'
        static_configs:
          - targets: ['localhost:8000']
        metrics_path: '/api/metrics'
        scrape_interval: 15s
    ```
    """
    # Aggregate latest metrics (with rate limiting)
    if aggregator.should_update(interval_seconds=15):
        try:
            aggregator.aggregate_from_database(db)

            # TODO: Add cache_manager and ml_state when available
            # aggregator.aggregate_from_cache(cache_manager)
            # aggregator.aggregate_from_ml_components(ml_state)

        except Exception as e:
            print(f"Error aggregating metrics: {e}")

    # Generate Prometheus formatted output
    metrics_output = exporter.generate_metrics()

    return Response(
        content=metrics_output,
        media_type=exporter.get_content_type()
    )


@router.post("/task-completion")
async def record_task_completion_metric(
    project_id: str,
    task_id: str,
    project_type: str,
    quality_score: float,
    duration_seconds: float,
    iteration_count: int,
    status: str,
    priority_mode: str,
    exporter: LazyBirdPrometheusExporter = Depends(get_exporter)
):
    """
    Manually record task completion metric.

    This endpoint can be called by the orchestration engine
    when a task completes.
    """
    exporter.record_task_completion(
        project_id=project_id,
        task_id=task_id,
        project_type=project_type,
        quality_score=quality_score,
        duration_seconds=duration_seconds,
        iteration_count=iteration_count,
        status=status,
        priority_mode=priority_mode
    )

    return {"status": "recorded"}


@router.post("/token-usage")
async def record_token_usage_metric(
    agent_type: str,
    prompt_tokens: int,
    completion_tokens: int,
    cost_usd: float,
    project_type: str,
    exporter: LazyBirdPrometheusExporter = Depends(get_exporter)
):
    """Record token usage and cost metrics."""
    exporter.record_token_usage(
        agent_type=agent_type,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cost_usd=cost_usd,
        project_type=project_type
    )

    return {"status": "recorded"}


@router.post("/agent-switch")
async def record_agent_switch_metric(
    from_agent: str,
    to_agent: str,
    reason: str,
    exporter: LazyBirdPrometheusExporter = Depends(get_exporter)
):
    """Record agent switch event."""
    exporter.record_agent_switch(
        from_agent=from_agent,
        to_agent=to_agent,
        reason=reason
    )

    return {"status": "recorded"}


@router.post("/cache-operation")
async def record_cache_operation_metric(
    cache_type: str,
    operation: str,
    size_bytes: int = None,
    exporter: LazyBirdPrometheusExporter = Depends(get_exporter)
):
    """Record cache operation."""
    exporter.record_cache_operation(
        cache_type=cache_type,
        operation=operation,
        size_bytes=size_bytes
    )

    return {"status": "recorded"}
