# Lazy Bird Monitoring Stack

Complete Prometheus + Grafana monitoring setup for AI orchestration metrics.

## Components

### 1. **Prometheus** (Port 9090)
- Metrics collection and storage
- 15s scrape interval
- Alert rule evaluation
- Time-series database

### 2. **Grafana** (Port 3001)
- Dashboard visualization
- Real-time monitoring
- Alert management
- Default credentials: admin/admin

### 3. **Exporters**
- **PostgreSQL Exporter** (9187): Database metrics
- **Redis Exporter** (9121): Cache metrics
- **Node Exporter** (9100): System metrics

## Quick Start

```bash
# Start entire monitoring stack
cd dashboard
docker-compose up -d prometheus grafana postgres-exporter redis-exporter node-exporter

# View Prometheus UI
open http://localhost:9090

# View Grafana Dashboard
open http://localhost:3001
# Login: admin / admin
```

## Custom Metrics Exposed

### Quality Metrics
- `lazybird_quality_score` - Current quality score (0-100)
- `lazybird_quality_dimensions` - Individual dimensions (coverage, security, etc.)
- `lazybird_quality_trend` - 7-day rolling average
- `lazybird_tasks_completed_total` - Task completion counter by status

### Performance Metrics
- `lazybird_task_duration_seconds` - Task processing time histogram
- `lazybird_iteration_count` - Refinement iterations histogram
- `lazybird_feedback_loop_latency_seconds` - Feedback loop timing
- `lazybird_parallel_speedup_factor` - Parallel evaluation speedup

### Cost Metrics
- `lazybird_tokens_used_total` - Token consumption by agent
- `lazybird_cost_usd_total` - Cost in USD by agent/project
- `lazybird_cost_savings_usd` - Savings from optimizations
- `lazybird_budget_utilization_percent` - Budget usage percentage

### Agent Metrics
- `lazybird_agent_switches_total` - Mid-task agent switches
- `lazybird_agent_performance_score` - Performance by agent
- `lazybird_active_agents` - Currently active agent count

### Cache Metrics
- `lazybird_cache_hit_rate_percent` - Cache hit rate by type
- `lazybird_cache_operations_total` - Operations (hit/miss/eviction)
- `lazybird_cache_size_bytes` - Cache size

### ML Metrics
- `lazybird_iteration_predictor_accuracy_percent` - ML predictor accuracy
- `lazybird_latent_compression_ratio` - Token compression ratio
- `lazybird_weight_optimizer_trials_total` - Bayesian optimization trials
- `lazybird_deep_supervision_checkpoint_quality` - Checkpoint quality

## Prometheus Queries

### Average Quality Score
```promql
avg(lazybird_quality_score)
```

### Task Success Rate (5m)
```promql
sum(rate(lazybird_tasks_completed_total{status="success"}[5m]))
/ sum(rate(lazybird_tasks_completed_total[5m])) * 100
```

### Daily Cost
```promql
sum(increase(lazybird_cost_usd_total[1d]))
```

### P95 Task Duration
```promql
histogram_quantile(0.95,
  sum(rate(lazybird_task_duration_seconds_bucket[5m])) by (le)
)
```

### Cache Hit Rate
```promql
avg(lazybird_cache_hit_rate_percent) by (cache_type)
```

## Alert Rules

### Quality Alerts
- **LowQualityScore**: Avg quality < 60% for 5min → Warning
- **CriticalQualityScore**: Avg quality < 40% for 2min → Critical

### Task Failure Alerts
- **HighTaskFailureRate**: >20% failure rate for 5min → Warning
- **CriticalTaskFailureRate**: >50% failure rate for 2min → Critical

### Cost Alerts
- **HighDailyCost**: >$50/day → Warning
- **BudgetExceeded**: >90% budget utilization → Critical

### Performance Alerts
- **SlowTaskProcessing**: P95 duration >300s for 10min → Warning
- **TooManyIterations**: P95 iterations >10 for 10min → Warning

### Cache Alerts
- **LowCacheHitRate**: Hit rate <50% for 10min → Warning

### System Health Alerts
- **BackendDown**: Backend unreachable for 1min → Critical
- **DatabaseDown**: Database unreachable for 1min → Critical

## Grafana Dashboard

15 panels covering:

1. **Quality Score Overview** - Gauge (0-100%)
2. **Task Completion Rate** - Success percentage
3. **Cost Today** - USD spent today
4. **Active Tasks** - Current task count
5. **Quality Trend (7d)** - Time series by project type
6. **Task Duration Distribution** - P50/P95 histogram
7. **Cost Breakdown by Agent** - Pie chart
8. **Token Usage by Agent** - Stacked area chart
9. **Cache Hit Rate** - Multi-gauge by cache type
10. **Iteration Count Distribution** - Heatmap
11. **Agent Switches** - Bar chart over time
12. **ML Optimization Impact** - Stat panel
13. **Cost Savings** - Bar gauge by optimization
14. **Quality Dimensions** - Radar chart
15. **Agent Performance Comparison** - Bar gauge

## Integration with Backend

The FastAPI backend exposes metrics at:

```
GET /api/metrics
```

Manual metric recording endpoints:

```
POST /api/metrics/task-completion
POST /api/metrics/token-usage
POST /api/metrics/agent-switch
POST /api/metrics/cache-operation
```

## Configuration Files

- `prometheus.yml` - Prometheus scrape configuration
- `alerts.yml` - Alert rule definitions
- `grafana-dashboard.json` - Pre-built Grafana dashboard

## Development

### Test Prometheus Metrics Locally

```bash
# Start backend
cd dashboard/backend
uvicorn main:socket_app --reload

# Fetch metrics
curl http://localhost:8000/api/metrics
```

### Add New Metric

1. Add metric to `prometheus_exporter.py`:
```python
self.my_metric = Counter(
    'lazybird_my_metric_total',
    'Description',
    ['label1', 'label2'],
    registry=self.registry
)
```

2. Record metric:
```python
exporter.my_metric.labels(label1='value1', label2='value2').inc()
```

3. Query in Prometheus:
```promql
lazybird_my_metric_total{label1="value1"}
```

## Production Deployment

### Enable Alertmanager

```yaml
# Add to docker-compose.yml
alertmanager:
  image: prom/alertmanager:v0.26.0
  ports:
    - "9093:9093"
  volumes:
    - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
```

### Configure Email Alerts

```yaml
# alertmanager.yml
route:
  receiver: 'email'
receivers:
  - name: 'email'
    email_configs:
      - to: 'alerts@example.com'
        from: 'prometheus@example.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'your-email@gmail.com'
        auth_password: 'your-app-password'
```

### Configure Slack Alerts

```yaml
receivers:
  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
        channel: '#alerts'
        title: 'Lazy Bird Alert'
```

## Troubleshooting

### Metrics not appearing?
- Check backend is running: `docker-compose ps backend`
- Verify metrics endpoint: `curl http://localhost:8000/api/metrics`
- Check Prometheus targets: http://localhost:9090/targets

### Grafana dashboard empty?
- Add Prometheus data source in Grafana
- Import dashboard from `grafana-dashboard.json`
- Check time range (default: Last 24h)

### Alerts not firing?
- Check alert rules in Prometheus: http://localhost:9090/alerts
- Verify Alertmanager is running
- Check alert configuration in `alerts.yml`

## License

MIT - Part of Lazy Bird AI Orchestration System
