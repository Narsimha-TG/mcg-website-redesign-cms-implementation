from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Grow with CallMate AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lead(BaseModel):
    id: str
    title: str
    status: str
    score: float
    timestamp: str
    lead_source: str
    conversion_probability: float

# In-memory seed data
leads_db = [
    {"id": "1", "title": "Tech Corp", "status": "active", "score": 85.5, "timestamp": "2023-10-27T10:00:00Z", "lead_source": "web", "conversion_probability": 0.75}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_leads": len(leads_db), "avg_score": 85.5}

@app.post("/api/reviews")
def submit_review(data: dict):
    return {"status": "success", "received": data}

@app.post("/api/leads/capture")
def capture_lead(lead: Lead):
    leads_db.append(lead.dict())
    return {"status": "created", "id": lead.id}

@app.get("/api/partners/performance")
def get_partner_performance():
    return {"partner_id": "P-001", "metrics": {"conversion_rate": "12%", "active_leads": 1}}