import pytest
from fastapi.testclient import TestClient

try:
    from backend.main import app
except ImportError:
    from main import app

client = TestClient(app)


def test_health_check():
    """Verify system health, GEE authentication, and worker status endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "healthy"
    assert payload.get("gee_auth") == "active"
    assert payload.get("worker_status") == "idle"


def test_get_analytics():
    """Verify aggregated UHI metrics and thermal raster statistics endpoint."""
    response = client.get("/api/analytics")
    assert response.status_code == 200
    records = response.json()
    assert isinstance(records, list)
    assert len(records) >= 2

    expected_fields = {
        "id",
        "city_name",
        "mean_surface_temp",
        "ndvi_correlation",
        "urban_heat_island_intensity",
        "processing_status",
        "timestamp",
    }

    for item in records:
        assert expected_fields.issubset(item.keys())
        assert isinstance(item["id"], str)
        assert isinstance(item["city_name"], str)
        assert isinstance(item["mean_surface_temp"], (int, float))
        assert isinstance(item["ndvi_correlation"], (int, float))
        assert isinstance(item["urban_heat_island_intensity"], (int, float))
        assert item["processing_status"] in ["completed", "pending", "failed"]


def test_trigger_pipeline_success():
    """Verify triggering GEE extraction and raster analysis workflow."""
    target_city = "Wroclaw"
    response = client.post("/api/pipeline/trigger", params={"city": target_city})
    assert response.status_code == 200
    payload = response.json()
    assert f"Pipeline triggered for {target_city}" in payload.get("message", "")
    assert "task_id" in payload


def test_trigger_pipeline_missing_param():
    """Verify validation failure when required city query param is omitted."""
    response = client.post("/api/pipeline/trigger")
    assert response.status_code == 422


def test_get_spatial_layers():
    """Verify geospatial GeoJSON/GeoTIFF metadata and map tile URLs endpoint."""
    response = client.get("/api/spatial/layers")
    assert response.status_code == 200
    payload = response.json()
    assert "layers" in payload
    assert isinstance(payload["layers"], list)
    assert len(payload["layers"]) >= 1
