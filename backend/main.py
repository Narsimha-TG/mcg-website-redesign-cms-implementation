from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Automated Technological Resource Discovery System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Resource(BaseModel):
    id: str
    source_url: str
    resource_title: str
    category: str
    tech_stack_tags: List[str]
    confidence_score: float
    embedding_vector: List[float]
    created_at: datetime
    last_updated: datetime

# In-memory seed data
resources_db = [
    Resource(
        id="1",
        source_url="https://github.com/example/repo",
        resource_title="Distributed Scraper",
        category="Infrastructure",
        tech_stack_tags=["Python", "FastAPI", "Redis"],
        confidence_score=0.98,
        embedding_vector=[0.1, 0.2, 0.3],
        created_at=datetime.now(),
        last_updated=datetime.now()
    )
]

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "worker_status": "active", "db_connectivity": "connected"}

@app.get("/api/v1/resources", response_model=List[Resource])
def get_resources(page: int = 1, limit: int = 10):
    return resources_db

@app.post("/api/v1/tasks/trigger")
def trigger_task(workflow_type: str):
    return {"message": f"Workflow {workflow_type} triggered successfully", "task_id": "task-uuid-123"}

@app.get("/api/v1/analytics/summary")
def get_analytics():
    return {"discovery_rate": 150, "avg_quality_score": 0.92, "total_resources": len(resources_db)}