import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["gee_connectivity"] == "connected"

def test_get_analytics():
    response = client.get("/api/analytics/uhi")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "lst_mean_celsius" in data[0]
    assert data[0]["city_name"] in ["Wroclaw", "Bengaluru"]

def test_trigger_pipeline_valid():
    payload = {"city": "Wroclaw"}
    response = client.post("/api/pipeline/execute?city=Wroclaw")
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_trigger_pipeline_invalid():
    response = client.post("/api/pipeline/execute?city=Paris")
    assert response.status_code == 400
    assert response.json()["detail"] == "City not supported"