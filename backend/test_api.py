import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "avg_score" in data

def test_submit_review():
    payload = {
        "title": "Test Task",
        "status": "pending",
        "score": 0.95,
        "confidence_level": 0.92,
        "action_taken": "test_action"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data
    assert "timestamp" in data

def test_execute_command():
    payload = {"action": "move_arm"}
    response = client.post("/api/robot/command", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["executed"] == "move_arm"