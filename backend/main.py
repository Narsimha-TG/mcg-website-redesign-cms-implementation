from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Review(BaseModel):
    id: int
    text: str
    rating: int

reviews_db = [
    {"id": 1, "text": "Great bot!", "rating": 5},
    {"id": 2, "text": "Very fast execution.", "rating": 4}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[Review])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED, response_model=Review)
def create_review(review: Review):
    for r in reviews_db:
        if r["id"] == review.id:
            raise HTTPException(status_code=400, detail="Review with this ID already exists")
    reviews_db.append(review.dict())
    return review

@app.get("/api/analytics")
def get_analytics():
    total = len(reviews_db)
    avg_rating = sum(r["rating"] for r in reviews_db) / total if total > 0 else 0
    return {
        "total_reviews": total,
        "average_rating": avg_rating
}
