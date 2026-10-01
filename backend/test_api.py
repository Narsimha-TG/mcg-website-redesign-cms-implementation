import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["db_connectivity"] == "connected"

def test_get_analytics():
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "discovery_rate" in data
    assert "avg_quality_score" in data
    assert data["total_resources"] >= 0

def test_trigger_task():
    payload = {"workflow_type": "scraping"}
    response = client.post("/api/v1/tasks/trigger", params=payload)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert "triggered successfully" in data["message"]

def test_get_resources_schema():
    response = client.get("/api/v1/resources")
    assert response.status_code == 200
    resources = response.json()
    assert isinstance(resources, list)
    if len(resources) > 0:
        keys = resources[0].keys()
        expected_fields = ["id", "source_url", "resource_title", "category", "tech_stack_tags", "confidence_score", "embedding_vector", "created_at", "last_updated"]
        for field in expected_fields:
            assert field in keys