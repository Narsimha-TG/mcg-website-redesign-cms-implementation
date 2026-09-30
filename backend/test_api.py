import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_analytics_endpoint():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_reviews_endpoint():
    payload = {
        "id": "task-123",
        "title": "Quality Check",
        "status": "completed",
        "score": 0.95,
        "timestamp": "2023-10-27T10:00:00Z",
        "robot_unit_id": "bot-001",
        "task_type": "inspection",
        "decision_confidence": 0.98,
        "execution_time_ms": 150
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code in [200, 201]
    assert response.json()["status"] == "success"