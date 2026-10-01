from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Urban Heat GIS Analysis Automation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyticsData(BaseModel):
    id: str
    city_name: str
    mean_surface_temp: float
    ndvi_correlation: float
    urban_heat_island_intensity: float
    processing_status: str
    timestamp: str

# In-memory seed data
DB = [
    {"id": "1", "city_name": "Wroclaw", "mean_surface_temp": 28.5, "ndvi_correlation": -0.65, "urban_heat_island_intensity": 3.2, "processing_status": "completed", "timestamp": "2023-10-27T10:00:00Z"},
    {"id": "2", "city_name": "Bengaluru", "mean_surface_temp": 31.2, "ndvi_correlation": -0.72, "urban_heat_island_intensity": 4.5, "processing_status": "completed", "timestamp": "2023-10-27T10:05:00Z"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "gee_auth": "active", "worker_status": "idle"}

@app.get("/api/analytics", response_model=List[AnalyticsData])
def get_analytics():
    return DB

@app.post("/api/pipeline/trigger")
def trigger_pipeline(city: str):
    return {"message": f"Pipeline triggered for {city}", "task_id": "task_uuid_123"}

@app.get("/api/spatial/layers")
def get_layers():
    return {"layers": [{"name": "LST_Raster", "url": "http://tiles.example.com/lst/{z}/{x}/{y}.png"}, {"name": "City_Boundary", "type": "GeoJSON"}]}
