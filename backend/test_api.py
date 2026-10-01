import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "worker_nodes" in response.json()

def test_get_analytics():
    response = client.get("/api/v1/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_views" in data
    assert data["success_rate"] >= 0

def test_enqueue_task():
    payload = {"video_url": "https://youtube.com/watch?v=test123"}
    response = client.post("/api/v1/tasks/enqueue", params=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["video_url"] == "https://youtube.com/watch?v=test123"
    assert data["status"] == "queued"
    assert "task_id" in data

def test_rotate_proxy():
    response = client.post("/api/v1/proxy/rotate")
    assert response.status_code == 200
    assert response.json()["status"] == "success"