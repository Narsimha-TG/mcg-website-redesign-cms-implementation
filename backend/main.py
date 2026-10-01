from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="MCG Website Redesign API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    status: str
    score: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MilestoneApproval(BaseModel):
    id: str
    verification_token: str

# In-memory seed data
db = [
    Review(title="Initial Design Review", status="pending", score=8.5),
    Review(title="CMS Integration", status="approved", score=9.2)
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/analytics", response_model=List[Review])
def get_analytics():
    return db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED)
def create_review(review: Review):
    db.append(review)
    return review

@app.post("/api/milestone/approve")
def approve_milestone(data: MilestoneApproval):
    for item in db:
        if item.id == data.id:
            item.status = "approved"
            return {"message": "Milestone approved successfully", "id": data.id}
    raise HTTPException(status_code=404, detail="Milestone not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)