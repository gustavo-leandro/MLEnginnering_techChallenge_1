
"""
Categories router: Endpoint for listing book categories.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud
from typing import List

categories_router = APIRouter(prefix="/api/v1", tags=["categories"])

def get_db():
    """
    Dependency to get a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@categories_router.get("/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    """
    List all book categories.
    """
    return crud.get_categories(db)
