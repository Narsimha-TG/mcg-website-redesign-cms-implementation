import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_get_history():
    response = client.get("/api/v1/trades/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_execute_strategy():
    payload = {"action": "toggle_on"}
    response = client.post("/api/v1/strategy/execute", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_update_config():
    payload = {"risk_limit": 0.05, "strategy_enabled": True}
    response = client.post("/api/v1/config/update", json=payload)
    assert response.status_code == 200
    assert response.json()["new_config"]["risk_limit"] == 0.05
    assert response.json()["new_config"]["strategy_enabled"] is True