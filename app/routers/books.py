from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import crud, schemas, scraping
from app.routers.auth import get_current_user

api_router = APIRouter(prefix="/api/v1", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# /api/v1/books/ (listagem paginada)
@api_router.get("/books/", response_model=List[schemas.BookBase])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)

# /api/v1/books/scraping/trigger
@api_router.post("/books/scraping/trigger", response_model=schemas.ScrapeResponse, status_code=status.HTTP_201_CREATED)
def scrape_and_save_books(pages: int = 2, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    books = scraping.scrape_books(pages=pages)
    inserted_count = crud.create_books(db, books)
    return schemas.ScrapeResponse(inserted=inserted_count)

# /api/v1/books/search
@api_router.get("/books/search", response_model=List[schemas.BookBase])
def search_books(title: str = None, category: str = None, db: Session = Depends(get_db)):
    return crud.search_books(db, title=title, category=category)

# /api/v1/books/top-rated
@api_router.get("/books/top-rated", response_model=List[schemas.BookBase])
def list_top_rated(db: Session = Depends(get_db)):
    return crud.get_top_rated(db)

# /api/v1/books/price-range
@api_router.get("/books/price-range", response_model=List[schemas.BookBase])
def search_books_by_price(min: float = None, max: float = None, db: Session = Depends(get_db)):
    return crud.search_books_by_price(db, min=min, max=max)

# /api/v1/books/{id}
@api_router.get("/books/{id}", response_model=schemas.BookBase)
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
