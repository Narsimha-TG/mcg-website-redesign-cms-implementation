from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Urban Heat GIS Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UHIAnalysis(BaseModel):
    id: str
    city_name: str
    lst_mean_celsius: float
    uhi_intensity_score: float
    processing_status: str
    satellite_source: str
    timestamp: str

# In-memory seed data
db = [
    {"id": "1", "city_name": "Wroclaw", "lst_mean_celsius": 28.5, "uhi_intensity_score": 4.2, "processing_status": "completed", "satellite_source": "Landsat-8", "timestamp": "2023-10-01T12:00:00Z"},
    {"id": "2", "city_name": "Bengaluru", "lst_mean_celsius": 32.1, "uhi_intensity_score": 6.8, "processing_status": "completed", "satellite_source": "Sentinel-2", "timestamp": "2023-10-01T12:00:00Z"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "worker_heartbeat": "active", "gee_connectivity": "connected"}

@app.post("/api/pipeline/execute")
def trigger_pipeline(city: str):
    if city not in ["Wroclaw", "Bengaluru"]:
        raise HTTPException(status_code=400, detail="City not supported")
    return {"message": f"Pipeline triggered for {city}", "task_id": "task_uuid_123"}

@app.get("/api/analytics/uhi", response_model=List[UHIAnalysis])
def get_analytics():
    return db

@app.get("/api/spatial/layers")
def get_layers():
    return {"layers": [{"name": "uhi_contours", "type": "geojson", "url": "/data/wroclaw_uhi.json"}]}
