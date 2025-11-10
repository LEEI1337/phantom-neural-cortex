"""
Prometheus Exporter - PHASE C Optimierung #10
===============================================

Exportiert Custom Metrics für Prometheus/Grafana Monitoring.
Ermöglicht Echtzeit-Überwachung der Orchestration-Leistung.

Key Features:
- Custom Metrics für Quality, Cost, Performance
- Token Usage Tracking
- Agent Switch Monitoring
- Cache Hit Rate Tracking
- Standardized Prometheus Exposition Format

Use Case: Production Monitoring & Alerting
"""

from prometheus_client import (
    Counter, Gauge, Histogram, Summary,
    CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
)
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json


@dataclass
class MetricConfig:
    """Konfiguration für Metric Collection."""

    enable_histograms: bool = True
    enable_summaries: bool = True
    histogram_buckets: List[float] = None

    def __post_init__(self):
        if self.histogram_buckets is None:
            # Default buckets: 0.5s, 1s, 2.5s, 5s, 10s, 30s, 60s, 120s
            self.histogram_buckets = [0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0]


class LazyBirdPrometheusExporter:
    """
    Prometheus Exporter für Lazy Bird Orchestration Metrics.

    Exposed Metrics:
    - Quality Scores (Gauge)
    - Task Completion Rate (Counter)
    - Iteration Counts (Histogram)
    - Processing Time (Histogram)
    - Token Usage (Counter)
    - Cost Tracking (Counter)
    - Agent Switches (Counter)
    - Cache Hit Rate (Gauge)
    """

    def __init__(self, config: MetricConfig = None, registry: CollectorRegistry = None):
        self.config = config or MetricConfig()
        self.registry = registry or CollectorRegistry()

        # Initialize all metrics
        self._init_quality_metrics()
        self._init_performance_metrics()
        self._init_cost_metrics()
        self._init_agent_metrics()
        self._init_cache_metrics()
        self._init_ml_metrics()

    def _init_quality_metrics(self):
        """Quality-bezogene Metriken."""

        # Current quality score (0-100)
        self.quality_score = Gauge(
            'lazybird_quality_score',
            'Current quality score of tasks',
            ['project_id', 'task_id', 'project_type'],
            registry=self.registry
        )

        # Individual quality dimensions
        self.quality_dimensions = Gauge(
            'lazybird_quality_dimensions',
            'Individual quality dimension scores',
            ['project_id', 'dimension'],  # dimension: test_coverage, security, complexity, etc.
            registry=self.registry
        )

        # Quality trend (rolling average)
        self.quality_trend = Gauge(
            'lazybird_quality_trend',
            'Rolling average quality score (7d)',
            ['project_type'],
            registry=self.registry
        )

        # Task completion status
        self.tasks_completed = Counter(
            'lazybird_tasks_completed_total',
            'Total number of completed tasks',
            ['project_type', 'status'],  # status: success, failed, cancelled
            registry=self.registry
        )

    def _init_performance_metrics(self):
        """Performance-bezogene Metriken."""

        # Task processing time
        if self.config.enable_histograms:
            self.task_duration = Histogram(
                'lazybird_task_duration_seconds',
                'Time taken to complete tasks',
                ['project_type', 'priority_mode'],
                buckets=self.config.histogram_buckets,
                registry=self.registry
            )

        # Iteration count per task
        if self.config.enable_histograms:
            self.iteration_count = Histogram(
                'lazybird_iteration_count',
                'Number of refinement iterations per task',
                ['project_type'],
                buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
                registry=self.registry
            )

        # Feedback loop latency
        if self.config.enable_summaries:
            self.feedback_loop_latency = Summary(
                'lazybird_feedback_loop_latency_seconds',
                'Latency of feedback loop evaluation',
                ['loop_type'],  # loop_type: quality_check, test_run, security_scan
                registry=self.registry
            )

        # Parallel evaluator speedup
        self.parallel_speedup = Gauge(
            'lazybird_parallel_speedup_factor',
            'Speedup factor from parallel evaluation',
            ['project_id'],
            registry=self.registry
        )

    def _init_cost_metrics(self):
        """Cost-bezogene Metriken."""

        # Token usage per agent
        self.tokens_used = Counter(
            'lazybird_tokens_used_total',
            'Total tokens consumed',
            ['agent_type', 'token_type'],  # token_type: prompt, completion
            registry=self.registry
        )

        # Cost in USD
        self.cost_usd = Counter(
            'lazybird_cost_usd_total',
            'Total cost in USD',
            ['agent_type', 'project_type'],
            registry=self.registry
        )

        # Cost savings from optimizations
        self.cost_savings = Gauge(
            'lazybird_cost_savings_usd',
            'Estimated cost savings from optimizations',
            ['optimization'],  # optimization: latent_reasoning, smart_switching, caching
            registry=self.registry
        )

        # Budget utilization
        self.budget_utilization = Gauge(
            'lazybird_budget_utilization_percent',
            'Current budget utilization percentage',
            ['project_id'],
            registry=self.registry
        )

    def _init_agent_metrics(self):
        """Agent-bezogene Metriken."""

        # Agent switches
        self.agent_switches = Counter(
            'lazybird_agent_switches_total',
            'Total number of mid-task agent switches',
            ['from_agent', 'to_agent', 'reason'],
            registry=self.registry
        )

        # Agent performance comparison
        self.agent_performance = Gauge(
            'lazybird_agent_performance_score',
            'Performance score per agent',
            ['agent_type', 'metric'],  # metric: quality, speed, cost_efficiency
            registry=self.registry
        )

        # Active agent distribution
        self.active_agents = Gauge(
            'lazybird_active_agents',
            'Number of currently active agents',
            ['agent_type'],
            registry=self.registry
        )

    def _init_cache_metrics(self):
        """Cache-bezogene Metriken."""

        # Cache hit rate
        self.cache_hit_rate = Gauge(
            'lazybird_cache_hit_rate_percent',
            'Cache hit rate percentage',
            ['cache_type'],  # cache_type: guideline, github_api, quality_pattern
            registry=self.registry
        )

        # Cache operations
        self.cache_operations = Counter(
            'lazybird_cache_operations_total',
            'Total cache operations',
            ['cache_type', 'operation'],  # operation: hit, miss, eviction
            registry=self.registry
        )

        # Cache size
        self.cache_size = Gauge(
            'lazybird_cache_size_bytes',
            'Current cache size in bytes',
            ['cache_type'],
            registry=self.registry
        )

    def _init_ml_metrics(self):
        """ML-Komponenten-bezogene Metriken."""

        # Iteration predictor accuracy
        self.iteration_predictor_accuracy = Gauge(
            'lazybird_iteration_predictor_accuracy_percent',
            'Accuracy of ML iteration predictor',
            registry=self.registry
        )

        # Latent reasoning compression ratio
        self.latent_compression_ratio = Gauge(
            'lazybird_latent_compression_ratio',
            'Token compression ratio from latent reasoning',
            registry=self.registry
        )

        # Weight optimizer convergence
        self.weight_optimizer_trials = Counter(
            'lazybird_weight_optimizer_trials_total',
            'Total Bayesian optimization trials',
            ['project_type', 'outcome'],  # outcome: improvement, no_change, degradation
            registry=self.registry
        )

        # Deep supervision checkpoint quality
        self.deep_supervision_quality = Gauge(
            'lazybird_deep_supervision_checkpoint_quality',
            'Quality at supervision checkpoints',
            ['checkpoint'],  # checkpoint: 33, 66, 100
            registry=self.registry
        )

    # ============================================================
    # Metric Update Methods
    # ============================================================

    def record_task_completion(
        self,
        project_id: str,
        task_id: str,
        project_type: str,
        quality_score: float,
        duration_seconds: float,
        iteration_count: int,
        status: str,
        priority_mode: str
    ):
        """Records task completion with all relevant metrics."""

        # Quality
        self.quality_score.labels(
            project_id=project_id,
            task_id=task_id,
            project_type=project_type
        ).set(quality_score)

        # Completion status
        self.tasks_completed.labels(
            project_type=project_type,
            status=status
        ).inc()

        # Duration
        if self.config.enable_histograms:
            self.task_duration.labels(
                project_type=project_type,
                priority_mode=priority_mode
            ).observe(duration_seconds)

        # Iterations
        if self.config.enable_histograms:
            self.iteration_count.labels(
                project_type=project_type
            ).observe(iteration_count)

    def record_token_usage(
        self,
        agent_type: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost_usd: float,
        project_type: str
    ):
        """Records token usage and associated costs."""

        self.tokens_used.labels(
            agent_type=agent_type,
            token_type='prompt'
        ).inc(prompt_tokens)

        self.tokens_used.labels(
            agent_type=agent_type,
            token_type='completion'
        ).inc(completion_tokens)

        self.cost_usd.labels(
            agent_type=agent_type,
            project_type=project_type
        ).inc(cost_usd)

    def record_agent_switch(
        self,
        from_agent: str,
        to_agent: str,
        reason: str
    ):
        """Records mid-task agent switch."""

        self.agent_switches.labels(
            from_agent=from_agent,
            to_agent=to_agent,
            reason=reason
        ).inc()

    def record_cache_operation(
        self,
        cache_type: str,
        operation: str,  # 'hit', 'miss', 'eviction'
        size_bytes: Optional[int] = None
    ):
        """Records cache operation."""

        self.cache_operations.labels(
            cache_type=cache_type,
            operation=operation
        ).inc()

        if size_bytes is not None:
            self.cache_size.labels(
                cache_type=cache_type
            ).set(size_bytes)

    def update_cache_hit_rate(
        self,
        cache_type: str,
        hit_rate_percent: float
    ):
        """Updates cache hit rate gauge."""

        self.cache_hit_rate.labels(
            cache_type=cache_type
        ).set(hit_rate_percent)

    def update_quality_dimension(
        self,
        project_id: str,
        dimension: str,
        score: float
    ):
        """Updates individual quality dimension score."""

        self.quality_dimensions.labels(
            project_id=project_id,
            dimension=dimension
        ).set(score)

    def update_ml_metric(
        self,
        metric_name: str,
        value: float,
        **labels
    ):
        """Generic ML metric updater."""

        if metric_name == 'iteration_predictor_accuracy':
            self.iteration_predictor_accuracy.set(value)

        elif metric_name == 'latent_compression_ratio':
            self.latent_compression_ratio.set(value)

        elif metric_name == 'deep_supervision_quality':
            checkpoint = labels.get('checkpoint', '100')
            self.deep_supervision_quality.labels(
                checkpoint=checkpoint
            ).set(value)

    def update_cost_savings(
        self,
        optimization: str,
        savings_usd: float
    ):
        """Updates cost savings gauge."""

        self.cost_savings.labels(
            optimization=optimization
        ).set(savings_usd)

    def update_budget_utilization(
        self,
        project_id: str,
        utilization_percent: float
    ):
        """Updates budget utilization."""

        self.budget_utilization.labels(
            project_id=project_id
        ).set(utilization_percent)

    def update_agent_performance(
        self,
        agent_type: str,
        metric: str,
        score: float
    ):
        """Updates agent performance metrics."""

        self.agent_performance.labels(
            agent_type=agent_type,
            metric=metric
        ).set(score)

    def set_active_agents(
        self,
        agent_counts: Dict[str, int]
    ):
        """Sets active agent counts."""

        for agent_type, count in agent_counts.items():
            self.active_agents.labels(
                agent_type=agent_type
            ).set(count)

    # ============================================================
    # Metric Exposition
    # ============================================================

    def generate_metrics(self) -> bytes:
        """
        Generates Prometheus-formatted metrics output.

        Returns:
            Metrics in Prometheus text exposition format
        """
        return generate_latest(self.registry)

    def get_content_type(self) -> str:
        """Returns the content type for HTTP response."""
        return CONTENT_TYPE_LATEST


class MetricsAggregator:
    """
    Aggregiert Metrics aus verschiedenen Quellen.

    Sammelt Daten aus:
    - Database (PostgreSQL)
    - Cache Manager
    - ML Components
    - Feedback Loops
    """

    def __init__(self, exporter: LazyBirdPrometheusExporter):
        self.exporter = exporter
        self.last_update = datetime.now()

    def aggregate_from_database(self, db_session):
        """
        Liest aktuelle Metrics aus der Datenbank.

        Args:
            db_session: SQLAlchemy Session
        """
        try:
            from models import Project, Task, QualitySnapshot, CostTracking
        except ImportError:
            # If running from different context, try dashboard path
            from dashboard.backend.models import Project, Task, QualitySnapshot, CostTracking

        # Quality trends
        for project in db_session.query(Project).all():
            # Get recent quality snapshots via tasks
            recent_snapshots = db_session.query(QualitySnapshot)\
                .join(Task, Task.id == QualitySnapshot.task_id)\
                .filter(Task.project_id == project.id)\
                .order_by(QualitySnapshot.created_at.desc())\
                .limit(10)\
                .all()

            if recent_snapshots:
                avg_quality = sum(s.overall_quality for s in recent_snapshots) / len(recent_snapshots)
                self.exporter.quality_trend.labels(
                    project_type=project.type.value if hasattr(project.type, 'value') else str(project.type)
                ).set(avg_quality)

                # Update quality dimensions
                latest = recent_snapshots[0]
                quality_dimensions = {
                    'test_coverage': latest.test_coverage,
                    'security_score': latest.security_score,
                    'code_quality': latest.code_quality_score,
                    'type_safety': latest.type_safety,
                    'documentation': latest.documentation
                }
                for dimension, value in quality_dimensions.items():
                    self.exporter.update_quality_dimension(
                        project_id=project.id,
                        dimension=dimension,
                        score=value
                    )

        # Cost tracking
        for cost_entry in db_session.query(CostTracking).all():
            # CostTracking has: agent, tokens_used, cost
            # record_token_usage expects different parameters, so skip for now
            # TODO: Update record_token_usage to match actual CostTracking schema
            pass

    def aggregate_from_cache(self, cache_manager):
        """
        Liest Cache Metrics aus dem CacheManager.

        Args:
            cache_manager: Instance von CacheManager
        """
        # Guideline cache
        guideline_stats = cache_manager.guideline_cache.get_stats()
        self.exporter.update_cache_hit_rate(
            cache_type='guideline',
            hit_rate_percent=guideline_stats['hit_rate']
        )

        # GitHub API cache
        github_stats = cache_manager.github_cache.get_stats()
        self.exporter.update_cache_hit_rate(
            cache_type='github_api',
            hit_rate_percent=github_stats['hit_rate']
        )

        # Quality pattern cache
        quality_stats = cache_manager.quality_pattern_cache.get_stats()
        self.exporter.update_cache_hit_rate(
            cache_type='quality_pattern',
            hit_rate_percent=quality_stats['hit_rate']
        )

    def aggregate_from_ml_components(self, ml_state: Dict):
        """
        Liest ML Component Performance Metrics.

        Args:
            ml_state: Dict mit aktuellen ML States
        """
        # Iteration predictor
        if 'iteration_predictor' in ml_state:
            accuracy = ml_state['iteration_predictor'].get('accuracy', 0.0)
            self.exporter.update_ml_metric(
                'iteration_predictor_accuracy',
                accuracy * 100
            )

        # Latent reasoning
        if 'latent_reasoning' in ml_state:
            compression = ml_state['latent_reasoning'].get('compression_ratio', 1.0)
            self.exporter.update_ml_metric(
                'latent_compression_ratio',
                compression
            )

        # Deep supervision
        if 'deep_supervision' in ml_state:
            for checkpoint, quality in ml_state['deep_supervision'].items():
                self.exporter.update_ml_metric(
                    'deep_supervision_quality',
                    quality,
                    checkpoint=checkpoint
                )

    def should_update(self, interval_seconds: int = 15) -> bool:
        """
        Prüft ob Update nötig ist (rate limiting).

        Args:
            interval_seconds: Minimum interval between updates

        Returns:
            True wenn Update durchgeführt werden soll
        """
        now = datetime.now()
        if (now - self.last_update).total_seconds() >= interval_seconds:
            self.last_update = now
            return True
        return False


# Export
__all__ = [
    'LazyBirdPrometheusExporter',
    'MetricConfig',
    'MetricsAggregator'
]
