import pytest
from app.workers.tasks.analytics import aggregate_metrics_task

def test_aggregate_metrics_task():
    # Calling the function directly (not as a celery task)
    result = aggregate_metrics_task("req-123")
    assert result["status"] == "success"
    assert result["request_id"] == "req-123"
