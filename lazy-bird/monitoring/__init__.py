"""
Prometheus Metrics Monitoring System (ADR-010)

This package implements comprehensive metrics collection and export:
- 40+ custom Prometheus metrics
- Integration with Lazy Bird automation
- Grafana dashboard support
- Real-time monitoring

Components:
- prometheus_exporter.py: Main metrics exporter

Usage:
    from lazy_bird.monitoring import PrometheusExporter

    exporter = PrometheusExporter(port=9090)
    exporter.start()

    # Record metrics
    exporter.record_task_completion(
        project_id='my-project',
        agent='claude',
        duration=45.2,
        quality_score=0.87
    )
"""

__version__ = "1.0.0"
__author__ = "Phantom Neural Cortex Team"

from .prometheus_exporter import LazyBirdPrometheusExporter as PrometheusExporter

__all__ = ['PrometheusExporter']
