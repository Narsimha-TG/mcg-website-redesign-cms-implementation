import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_status():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert "progress" in data
    assert "active_worker_count" in data
    assert "success_rate" in data

def test_start_jobs():
    response = client.post("/api/v1/jobs/start")
    assert response.status_code == 200
    assert response.json() == {"message": "Migration sequence triggered", "status": "running"}

def test_pause_jobs():
    response = client.post("/api/v1/jobs/pause")
    assert response.status_code == 200
    assert response.json() == {"message": "Automation process halted gracefully"}

def test_get_logs():
    response = client.get("/api/v1/logs")
    assert response.status_code == 200
    data = response.json()
    assert "logs" in data
    assert isinstance(data["logs"], list)
    assert len(data["logs"]) > 0
    assert "row_id" in data["logs"][0]