from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
import uuid

app = FastAPI(title="AI Reels Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
jobs: Dict[str, dict] = {}

class ReelRequest(BaseModel):
    prompt: str

class ReelStatus(BaseModel):
    job_id: str
    status: str
    video_url: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime

@app.post("/api/v1/generate-reel", status_code=202)
async def generate_reel(request: ReelRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "job_id": job_id,
        "prompt": request.prompt,
        "status": "processing",
        "video_url": None,
        "metadata": {},
        "created_at": datetime.utcnow()
    }
    return {"job_id": job_id, "status": "processing"}

@app.get("/api/v1/status/{job_id}", response_model=ReelStatus)
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.post("/api/v1/webhook/n8n")
async def n8n_webhook(data: dict):
    job_id = data.get("job_id")
    if job_id in jobs:
        jobs[job_id].update({
            "status": data.get("status", "completed"),
            "video_url": data.get("video_url"),
            "metadata": data.get("metadata", {})
        })
        return {"message": "Webhook processed"}
    raise HTTPException(status_code=404, detail="Job not found")