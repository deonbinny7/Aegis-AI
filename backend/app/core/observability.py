"""
Observability extension points for Prometheus, OpenTelemetry, and structured logging.
"""

from typing import Any

def setup_prometheus_metrics(app: Any) -> None:
    """
    Hook to initialize Prometheus /metrics endpoint.
    Implementation reserved for future prompts.
    """
    pass

def setup_opentelemetry(app: Any) -> None:
    """
    Hook to initialize OpenTelemetry tracing.
    Implementation reserved for future prompts.
    """
    pass
