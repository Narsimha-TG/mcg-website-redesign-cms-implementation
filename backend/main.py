from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

reviews_db = []

class Review(BaseModel):
    review: str

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews")
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED)
def create_review(review: Review):
    reviews_db.append(review.dict())
    return review.dict()

@app.get("/api/analytics")
def get_analytics():
    return {"total_reviews": len(reviews_db)}
