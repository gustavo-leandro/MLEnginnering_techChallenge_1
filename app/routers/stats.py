"""
Stats router: Endpoints for book statistics and analytics.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from typing import List

stats_router = APIRouter(prefix="/api/v1/stats", tags=["stats"])


def get_db():
    """
    Dependency to get a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@stats_router.get("/overview")
def stats_overview(db: Session = Depends(get_db)):
    """
    Get overview statistics for books.
    """
    return crud.get_stats_overview(db)


@stats_router.get("/categories")
def stats_categories(db: Session = Depends(get_db)):
    """
    Get statistics by book category.
    """
    return crud.get_category_overview(db)


@stats_router.get("/top-rated", response_model=List[schemas.BookBase])
def list_top_rated(db: Session = Depends(get_db)):
    """
    List books with top rating.
    """
    return crud.get_top_rated(db)

