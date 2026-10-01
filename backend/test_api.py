import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "auth": "connected"}

def test_get_portfolio():
    response = client.get("/api/v1/portfolio")
    assert response.status_code == 200
    data = response.json()
    assert "balance" in data
    assert "positions" in data

def test_create_order_success():
    order_payload = {
        "symbol": "TSLA",
        "side": "buy",
        "quantity": 5,
        "price": 200.50
    }
    response = client.post("/api/v1/orders", json=order_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TSLA"
    assert data["status"] == "pending"
    assert "order_id" in data
    assert "timestamp" in data

def test_toggle_strategy():
    response = client.post("/api/v1/strategy/toggle", json={"enabled": True})
    assert response.status_code == 200
    assert response.json() == {"strategy_enabled": True}