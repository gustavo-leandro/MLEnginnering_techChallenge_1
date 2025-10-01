from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from typing import List

stats_router = APIRouter(prefix="/api/v1/stats", tags=["stats"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@stats_router.get("/overview")
def stats_overview(db: Session = Depends(get_db)):
    total_books = crud.count_books(db)
    avg_price = crud.avg_price(db)
    rating_dist = crud.rating_distribution(db)
    return {
        "total_books": total_books,
        "avg_price": avg_price,
        "rating_distribution": rating_dist
    }

@stats_router.get("/categories")
def stats_categories(db: Session = Depends(get_db)):
    return crud.stats_by_category(db)

@stats_router.get("/top-rated", response_model=List[schemas.BookBase])
def top_rated_books(db: Session = Depends(get_db)):
    return crud.top_rated_books(db)

@stats_router.get("/price-range", response_model=List[schemas.BookBase])
def books_price_range(min: float, max: float, db: Session = Depends(get_db)):
    return crud.books_in_price_range(db, min, max)
