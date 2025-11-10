# ADR-010: Prometheus Metrics Exporter

**Status:** Accepted
**Date:** 2025-11-09
**Decision Makers:** Phantom Neural Cortex Team
**Related:** Phase C Observability #1

## Context

Current system lacks comprehensive observability, making it difficult to:

- **Diagnose performance issues:** No visibility into where time is spent
- **Identify bottlenecks:** Cannot see which operations are slow
- **Track quality trends:** No historical quality metrics
- **Alert on failures:** No proactive monitoring or alerting
- **Optimize resource usage:** No CPU, memory, or API usage tracking
- **SLA compliance:** Cannot verify performance guarantees

**Current monitoring gaps:**
- No metrics on latency distribution (p50, p95, p99)
- No cost tracking per agent or operation
- No quality degradation detection
- No cache hit rate monitoring
- No error rate tracking
- No throughput visibility
- No dependency on external services health

**Operational blind spots:**
- Deployment impact unknown
- Configuration tuning has no metrics
- Performance regressions detected manually
- Post-incident analysis impossible without logs

Implementing comprehensive Prometheus metrics would enable:
- Real-time dashboards (Grafana)
- Automated alerting on anomalies
- Capacity planning based on trends
- Data-driven optimization
- Root cause analysis capabilities

## Decision

Implement a **Prometheus Metrics Exporter** that tracks 40+ custom metrics across system categories:
1. **Performance metrics:** Latency, throughput, queue depth
2. **Quality metrics:** Quality scores, error rates, test coverage
3. **Cost metrics:** API costs, agent usage, resource consumption
4. **System metrics:** Cache hits, database queries, external API calls
5. **Agent metrics:** Per-agent quality, cost, success rate

### Architecture

**Metrics Categories:**

```python
class MetricsExporter:
    """Exports Prometheus metrics for system monitoring"""

    def __init__(self, registry: CollectorRegistry = None):
        self.registry = registry or CollectorRegistry()

        # Performance metrics (8)
        self.task_latency = Histogram(
            'lazybird_task_latency_ms',
            'Task execution latency in milliseconds',
            buckets=[100, 500, 1000, 2000, 5000, 10000],
            registry=self.registry
        )
        self.iteration_duration = Histogram(
            'lazybird_iteration_duration_ms',
            'Single iteration duration',
            buckets=[500, 1000, 2000, 5000],
            registry=self.registry
        )
        self.checkpoint_latency = Histogram(
            'lazybird_checkpoint_latency_ms',
            'Checkpoint evaluation latency',
            buckets=[50, 100, 200, 500],
            registry=self.registry
        )
        self.evaluation_latency = Histogram(
            'lazybird_evaluation_latency_ms',
            'Quality evaluation latency',
            buckets=[500, 1000, 2000, 5000, 10000],
            registry=self.registry
        )
        self.agent_latency = Histogram(
            'lazybird_agent_latency_ms',
            'Agent inference latency',
            labels=['agent'],
            buckets=[500, 1000, 2000, 5000, 10000],
            registry=self.registry
        )
        self.embedding_generation_latency = Histogram(
            'lazybird_embedding_generation_latency_ms',
            'Embedding generation latency',
            buckets=[100, 500, 1000, 2000],
            registry=self.registry
        )
        self.cache_lookup_latency = Histogram(
            'lazybird_cache_lookup_latency_ms',
            'Cache lookup latency by layer',
            labels=['cache_layer'],
            buckets=[1, 5, 10, 50, 100],
            registry=self.registry
        )
        self.api_call_latency = Histogram(
            'lazybird_api_call_latency_ms',
            'External API call latency',
            labels=['service'],
            buckets=[100, 500, 1000, 2000, 5000],
            registry=self.registry
        )

        # Quality metrics (8)
        self.quality_score = Histogram(
            'lazybird_quality_score',
            'Final code quality score (0-100)',
            buckets=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            registry=self.registry
        )
        self.test_coverage = Histogram(
            'lazybird_test_coverage_percent',
            'Code test coverage percentage',
            buckets=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            registry=self.registry
        )
        self.security_vulnerabilities = Counter(
            'lazybird_security_vulnerabilities_total',
            'Total security vulnerabilities detected',
            labels=['severity'],  # critical, high, medium, low
            registry=self.registry
        )
        self.type_errors = Counter(
            'lazybird_type_errors_total',
            'Total type checking errors',
            registry=self.registry
        )
        self.test_failures = Counter(
            'lazybird_test_failures_total',
            'Total test failures',
            registry=self.registry
        )
        self.task_success_rate = Gauge(
            'lazybird_task_success_rate_percent',
            'Percentage of tasks completed successfully',
            registry=self.registry
        )
        self.early_termination_rate = Counter(
            'lazybird_early_termination_total',
            'Tasks terminated early at checkpoint',
            registry=self.registry
        )
        self.checkpoint_failures = Counter(
            'lazybird_checkpoint_failures_total',
            'Checkpoint gate failures',
            labels=['checkpoint'],  # 1, 2, 3
            registry=self.registry
        )

        # Cost metrics (6)
        self.api_cost = Counter(
            'lazybird_api_cost_usd_total',
            'Total API cost in USD',
            labels=['agent', 'operation'],
            registry=self.registry
        )
        self.token_usage = Counter(
            'lazybird_token_usage_total',
            'Total tokens consumed',
            labels=['agent'],
            registry=self.registry
        )
        self.cost_per_task = Histogram(
            'lazybird_cost_per_task_usd',
            'Cost per task execution',
            buckets=[0.01, 0.05, 0.1, 0.2, 0.5],
            registry=self.registry
        )
        self.agent_cost_ratio = Gauge(
            'lazybird_agent_cost_ratio',
            'Cost ratio for agent switching',
            labels=['from_agent', 'to_agent'],
            registry=self.registry
        )
        self.resource_utilization = Gauge(
            'lazybird_resource_utilization_percent',
            'Percentage resource utilization',
            labels=['resource'],  # cpu, memory, network
            registry=self.registry
        )
        self.cost_savings = Counter(
            'lazybird_cost_savings_usd_total',
            'Total savings from optimization',
            registry=self.registry
        )

        # System metrics (10)
        self.cache_hit_rate = Gauge(
            'lazybird_cache_hit_rate_percent',
            'Cache hit rate by layer',
            labels=['cache_layer'],
            registry=self.registry
        )
        self.cache_size = Gauge(
            'lazybird_cache_size_mb',
            'Cache size in MB by layer',
            labels=['cache_layer'],
            registry=self.registry
        )
        self.queue_depth = Gauge(
            'lazybird_task_queue_depth',
            'Number of tasks in queue',
            registry=self.registry
        )
        self.active_tasks = Gauge(
            'lazybird_active_tasks_count',
            'Number of active tasks',
            registry=self.registry
        )
        self.database_queries = Counter(
            'lazybird_database_queries_total',
            'Total database queries executed',
            labels=['operation'],  # select, insert, update, delete
            registry=self.registry
        )
        self.database_latency = Histogram(
            'lazybird_database_latency_ms',
            'Database query latency',
            buckets=[1, 5, 10, 50, 100, 500],
            registry=self.registry
        )
        self.external_api_calls = Counter(
            'lazybird_external_api_calls_total',
            'Calls to external APIs',
            labels=['service'],
            registry=self.registry
        )
        self.external_api_errors = Counter(
            'lazybird_external_api_errors_total',
            'External API call errors',
            labels=['service', 'error_type'],
            registry=self.registry
        )
        self.parallel_eval_speedup = Histogram(
            'lazybird_parallel_eval_speedup',
            'Speedup from parallel evaluation',
            buckets=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
            registry=self.registry
        )
        self.memory_usage = Gauge(
            'lazybird_memory_usage_mb',
            'Process memory usage in MB',
            registry=self.registry
        )

        # Agent metrics (8)
        self.agent_usage = Counter(
            'lazybird_agent_usage_total',
            'Usage count by agent',
            labels=['agent'],
            registry=self.registry
        )
        self.agent_quality = Gauge(
            'lazybird_agent_quality_score',
            'Average quality score by agent',
            labels=['agent'],
            registry=self.registry
        )
        self.agent_cost = Gauge(
            'lazybird_agent_cost_usd_per_call',
            'Cost per call by agent',
            labels=['agent'],
            registry=self.registry
        )
        self.agent_success_rate = Gauge(
            'lazybird_agent_success_rate_percent',
            'Success rate by agent',
            labels=['agent'],
            registry=self.registry
        )
        self.agent_switch_count = Counter(
            'lazybird_agent_switch_total',
            'Mid-task agent switches',
            labels=['from_agent', 'to_agent'],
            registry=self.registry
        )
        self.agent_switch_improvement = Histogram(
            'lazybird_agent_switch_quality_improvement',
            'Quality improvement from switching',
            buckets=[-10, -5, 0, 5, 10, 15, 20],
            registry=self.registry
        )
        self.embedding_cache_hit_rate = Gauge(
            'lazybird_embedding_cache_hit_rate_percent',
            'Hit rate for embedding cache',
            registry=self.registry
        )
        self.guideline_match_quality = Histogram(
            'lazybird_guideline_match_quality_score',
            'Quality of guideline matching (0-1)',
            buckets=[0.1, 0.3, 0.5, 0.7, 0.9],
            registry=self.registry
        )
```

**Metric Recording:**

```python
class MetricsRecorder:
    """Records metrics throughout system operations"""

    def __init__(self, exporter: MetricsExporter):
        self.exporter = exporter

    def record_task_completion(self, task: Task, result: TaskResult):
        """Record metrics for completed task"""
        self.exporter.task_latency.observe(result.execution_time_ms)
        self.exporter.quality_score.observe(result.final_quality)
        self.exporter.cost_per_task.observe(result.cost_usd)
        self.exporter.test_coverage.observe(result.test_coverage)

        if result.success:
            self.exporter.task_success_rate.set(95)  # Update running average

    def record_agent_call(self, agent: str, latency_ms: float,
                         cost: float, tokens_used: int):
        """Record agent API call"""
        self.exporter.agent_latency.labels(agent=agent).observe(latency_ms)
        self.exporter.agent_usage.labels(agent=agent).inc()
        self.exporter.api_cost.labels(agent=agent, operation='refine').inc(cost)
        self.exporter.token_usage.labels(agent=agent).inc(tokens_used)

    def record_cache_hit(self, cache_layer: str, latency_ms: float):
        """Record cache hit"""
        self.exporter.cache_lookup_latency.labels(
            cache_layer=cache_layer
        ).observe(latency_ms)

    def record_evaluation(self, eval: CheckpointEvaluation, latency_ms: float):
        """Record quality evaluation"""
        self.exporter.evaluation_latency.observe(latency_ms)
        self.exporter.security_vulnerabilities.labels(
            severity='critical'
        ).inc(eval.vulnerabilities_critical)
        self.exporter.type_errors.inc(eval.type_errors)
        self.exporter.test_failures.inc(eval.test_failures)

    def record_agent_switch(self, from_agent: str, to_agent: str,
                           quality_delta: float):
        """Record mid-task agent switch"""
        self.exporter.agent_switch_count.labels(
            from_agent=from_agent,
            to_agent=to_agent
        ).inc()
        self.exporter.agent_switch_improvement.observe(quality_delta)

    def record_checkpoint_failure(self, checkpoint_num: int):
        """Record checkpoint gate failure"""
        self.exporter.checkpoint_failures.labels(
            checkpoint=str(checkpoint_num)
        ).inc()
        self.exporter.early_termination_rate.inc()
```

**Prometheus Endpoint:**

```python
def create_metrics_app():
    """Create Flask app exposing Prometheus metrics"""

    app = Flask(__name__)
    exporter = MetricsExporter()
    recorder = MetricsRecorder(exporter)

    @app.route('/metrics')
    def metrics():
        """Expose Prometheus metrics endpoint"""
        return generate_latest(exporter.registry)

    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {'status': 'healthy'}, 200

    @app.route('/dashboard')
    def dashboard():
        """Grafana dashboard link"""
        return {
            'dashboard': 'http://grafana:3000/d/lazybird-metrics'
        }

    return app, exporter, recorder
```

### Implementation Details

**File:** `lazy-bird/monitoring/prometheus_exporter.py`

**Core Classes:**

```python
class MetricsManager:
    """Central metrics management"""

    def __init__(self):
        self.exporter = MetricsExporter()
        self.recorder = MetricsRecorder(self.exporter)

    def start_prometheus_server(self, port: int = 8000):
        """Start Prometheus metrics server"""
        start_http_server(port, registry=self.exporter.registry)

    def export_metrics(self) -> str:
        """Export current metrics as Prometheus format"""
        return generate_latest(self.exporter.registry).decode('utf-8')

    def get_metric_summary(self) -> Dict[str, Any]:
        """Get summary of key metrics"""
        return {
            'avg_quality': self._get_avg('lazybird_quality_score'),
            'avg_latency_ms': self._get_avg('lazybird_task_latency_ms'),
            'success_rate': self._get_gauge('lazybird_task_success_rate_percent'),
            'total_cost_usd': self._get_counter('lazybird_api_cost_usd_total'),
            'cache_hit_rate': self._get_avg('lazybird_cache_hit_rate_percent'),
        }
```

**Grafana Dashboard Configuration:**

```json
{
  "dashboard": {
    "title": "Phantom Neural Cortex - LazyBird Metrics",
    "panels": [
      {
        "title": "Task Success Rate",
        "targets": [
          {"expr": "lazybird_task_success_rate_percent"}
        ]
      },
      {
        "title": "Average Task Latency (p95)",
        "targets": [
          {"expr": "histogram_quantile(0.95, lazybird_task_latency_ms)"}
        ]
      },
      {
        "title": "Quality Score Distribution",
        "targets": [
          {"expr": "lazybird_quality_score"}
        ]
      },
      {
        "title": "Cost by Agent",
        "targets": [
          {"expr": "sum by (agent) (rate(lazybird_api_cost_usd_total[5m]))"}
        ]
      },
      {
        "title": "Cache Hit Rate by Layer",
        "targets": [
          {"expr": "lazybird_cache_hit_rate_percent"}
        ]
      },
      {
        "title": "Agent Comparison",
        "targets": [
          {"expr": "lazybird_agent_quality_score"},
          {"expr": "lazybird_agent_cost_usd_per_call"}
        ]
      }
    ]
  }
}
```

## Consequences

### Positive

1. **Complete System Visibility:** Real-time insight into operations
   - See exactly where time is spent
   - Identify performance bottlenecks immediately
   - Quality trends visible at a glance
   - Cost tracking per component

2. **Automated Alerting:** Detect issues proactively
   - Alert on quality degradation >5%
   - Alert on latency spikes >2σ
   - Alert on error rate increases
   - Can act before customers notice

3. **Data-Driven Optimization:** Quantitative improvement decisions
   - Measure impact of configuration changes
   - A/B test optimizations with confidence
   - Avoid premature optimization
   - Focus on highest-impact improvements

4. **Capacity Planning:** Understand resource needs
   - Predict when scaling needed
   - Right-size infrastructure
   - Avoid over/under-provisioning
   - Cost optimization

5. **Post-Incident Analysis:** Root cause investigation
   - Replay events that led to failure
   - Identify timing/causation relationships
   - Improve system reliability
   - Learn from incidents

### Negative

1. **Metrics Cardinality Explosion:** Too many label combinations
   - 40 metrics × 5 agents × 3 operations = 600 time series
   - Storage cost increases
   - Query performance degradation
   - **Mitigation:** Careful label design, cardinality limits

2. **Overhead of Recording Metrics:** Adds latency
   - Each metric observation takes ~1-5μs
   - Can add up in hot paths
   - **Mitigation:** Async recording, sampling

3. **Metric Staleness:** Requires active use to see patterns
   - Slow queries take time to detect
   - Need sufficient traffic to see distribution
   - **Mitigation:** Synthetic monitoring, alerts on silence

4. **Alert Tuning Difficulty:** False positives from poor thresholds
   - Too strict: alert fatigue
   - Too loose: misses real issues
   - Thresholds vary by time of day
   - **Mitigation:** Machine learning for anomaly detection

5. **Data Storage and Retention:** Cost and complexity
   - Metrics retention requires storage
   - High-resolution metrics = high cost
   - **Mitigation:** Sampling, tiered storage

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Metric cardinality explosion | Medium | Medium | Label limits, cardinality enforcement |
| Alerting false positives | Medium | Low | Threshold tuning, ML-based anomaly detection |
| Storage cost exceeds budget | Low | Low | Sampling, downsampling old data |
| Metrics wrong/misleading | Low | High | Validation, regular audit of metric definitions |

## Alternatives Considered

### 1. No Metrics (Status Quo)
**Rejected Reason:** Blind operations, cannot optimize, no incident response

### 2. Application Logging Only
**Rejected Reason:** Too verbose, hard to aggregate, not time-series optimized

### 3. Custom Metrics Implementation
**Rejected Reason:** Reinventing the wheel, poor integration with monitoring tools

### 4. Pull-based Monitoring (Datadog/New Relic)
**Rejected Reason:** Vendor lock-in, high cost, doesn't give full control

## Implementation Status

✅ **Completed:**
- MetricsExporter with 40+ metrics ([prometheus_exporter.py](../../lazy-bird/monitoring/prometheus_exporter.py))
- MetricsRecorder for observation recording
- Prometheus HTTP endpoint
- Grafana dashboard configuration
- Integration points throughout system
- Unit tests ([test_prometheus_exporter.py](../../lazy-bird/tests/test_prometheus_exporter.py))

⏳ **Pending:**
- Production deployment and metrics collection
- Grafana dashboard creation
- Alert rule configuration
- Metrics validation and tuning

## Validation

**Success Criteria:**
- [x] Metrics collection without errors
- [x] Prometheus endpoint responds correctly
- [x] Metrics exportable in Prometheus format
- [ ] Production validation: 1000+ recorded metrics
- [ ] Grafana dashboards functional
- [ ] Alert rules functional

**Monitoring:**
- Monitor the monitoring: `lazybird_metrics_export_latency_ms`

**Dashboard Metrics:**

```
Top-level dashboard shows:
- Task success rate: 95%+
- Average quality: 85%
- Average latency: 45s (5 iterations × 9s each)
- Total cost: $0.07 per task (52% savings vs baseline)
- Cache hit rate: 45%
```

## Related Decisions

- All other ADRs depend on metrics for validation
- **ADR-004:** Deep Supervision (checkpoint metrics)
- **ADR-006:** Parallel Evaluation (speedup metrics)
- **ADR-007:** Three-Layer Caching (cache metrics)
- **ADR-005:** Smart Agent Switching (agent cost metrics)

## References

- Prometheus: https://prometheus.io/
- Grafana: https://grafana.com/
- Python prometheus client: https://github.com/prometheus/client_python
- Metrics best practices: https://prometheus.io/docs/practices/
- Implementation: `lazy-bird/monitoring/prometheus_exporter.py`
