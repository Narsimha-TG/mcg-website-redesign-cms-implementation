from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="MCG Website Redesign API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentItem(BaseModel):
    id: str
    title: str
    status: str
    score: float
    timestamp: str
    verification_result: Optional[str] = None
    metadata: dict = {}

# In-memory seed data
db = [
    ContentItem(id="1", title="Homepage Hero", status="published", score=95.5, timestamp=datetime.now().isoformat()),
    ContentItem(id="2", title="About Us", status="draft", score=88.0, timestamp=datetime.now().isoformat())
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_items": len(db), "average_score": sum(i.score for i in db) / len(db) if db else 0}

@app.post("/api/reviews")
def submit_review(item: ContentItem):
    db.append(item)
    return {"message": "Review submitted successfully", "id": item.id}

@app.post("/api/verify")
def trigger_verification(item_id: str):
    for item in db:
        if item.id == item_id:
            item.verification_result = "Verified"
            return {"status": "success", "item_id": item_id}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/api/content", response_model=List[ContentItem])
def get_content():
    return db