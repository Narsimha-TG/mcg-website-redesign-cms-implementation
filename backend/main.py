from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Review(BaseModel):
    id: Optional[int] = None
    text: str
    rating: int

reviews_db: List[Review] = []

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[Review])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED, response_model=Review)
def create_review(review: Review):
    if review.id is None:
        review.id = len(reviews_db) + 1
    reviews_db.append(review)
    return review

@app.get("/api/analytics")
def get_analytics():
    return {"total_reviews": len(reviews_db)}
