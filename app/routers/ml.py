"""
ML router: Endpoints for ML features, training data, and predictions.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from app.routers.auth import get_current_user
from typing import List
import random

ml_router = APIRouter(prefix="/api/v1/ml", tags=["ml"])


def get_db():
    """
    Dependency to get a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@ml_router.get("/features", response_model=List[schemas.MLBookFeatures])
def get_features(db: Session = Depends(get_db)):
    """
    Get ML features for all books.
    """
    books = crud.get_books(db)
    features = [
        schemas.MLBookFeatures(
            category=b.category,
            rating=b.rating,
            price_excl_tax=b.price_excl_tax,
            price_incl_tax=b.price_incl_tax,
            num_available=b.num_available,
            num_reviews=b.num_reviews,
        )
        for b in books
    ]
    return features


@ml_router.get("/training-data", response_model=List[schemas.BookBase])
def get_training_data(db: Session = Depends(get_db)):
    """
    Get a random subset of 100 books for ML training.
    """
    books = crud.get_books(db)
    if len(books) > 100:
        books = random.sample(books, 100)
    return books


@ml_router.post("/predictions")
def post_predictions(data: List[dict], user: str = Depends(get_current_user)):
    """
    Post data for ML predictions (mock implementation).
    """
    predictions = [{"input": d, "prediction": 1} for d in data]
    return {"predictions": predictions}
