from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Real Estate Data Migration API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MigrationJob(BaseModel):
    row_id: str
    search_criteria: str
    target_url: str
    status: str = "pending"
    error_message: Optional[str] = None
    execution_timestamp: Optional[str] = None

# In-memory storage
jobs_db = [
    MigrationJob(row_id="1", search_criteria="Downtown Apartments", target_url="https://example.com/1"),
    MigrationJob(row_id="2", search_criteria="Suburban Homes", target_url="https://example.com/2")
]

@app.get("/api/v1/status")
async def get_status():
    total = len(jobs_db)
    success = len([j for j in jobs_db if j.status == "success"])
    return {
        "progress": f"{(success/total)*100}%" if total > 0 else "0%",
        "active_worker_count": 1,
        "success_rate": f"{success}/{total}"
    }

@app.post("/api/v1/jobs/start")
async def start_jobs():
    return {"message": "Migration sequence triggered", "status": "running"}

@app.post("/api/v1/jobs/pause")
async def pause_jobs():
    return {"message": "Automation process halted gracefully"}

@app.get("/api/v1/logs")
async def get_logs():
    return {"logs": jobs_db}
