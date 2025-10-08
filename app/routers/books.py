"""
Books router: Endpoints for listing, searching, scraping, and retrieving books.
"""

from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import crud, schemas, scraping
from app.routers.auth import get_current_user

api_router = APIRouter(prefix="/api/v1", tags=["books"])


def get_db():
    """
    Dependency to get a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_router.get("/books/", response_model=List[schemas.BookBase])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    List books with pagination.
    """
    return crud.get_books(db, skip=skip, limit=limit)


@api_router.post(
    "/books/scraping/trigger",
    response_model=schemas.ScrapeResponse,
    status_code=status.HTTP_201_CREATED,
)
def scrape_and_save_books(
    background_tasks: BackgroundTasks,
    pages: int = 2,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    """
    Trigger book scraping from external site and save to database in the background.
    Returns immediately with the status.
    """
    def run_scraping():
        books = scraping.scrape_books(pages=pages)
        crud.create_books(db, books)
    background_tasks.add_task(run_scraping)
    return schemas.ScrapeResponse(message="Scraping started in background")


@api_router.get("/books/search", response_model=List[schemas.BookBase])
def search_books(
    title: str = None, category: str = None, db: Session = Depends(get_db)
):
    """
    Search books by title and/or category.
    """
    return crud.search_books(db, title=title, category=category)


@api_router.get("/books/top-rated", response_model=List[schemas.BookBase])
def list_top_rated(db: Session = Depends(get_db)):
    """
    List books with top rating.
    """
    return crud.get_top_rated(db)


@api_router.get("/books/price-range", response_model=List[schemas.BookBase])
def search_books_by_price(
    min: float = None, max: float = None, db: Session = Depends(get_db)
):
    """
    Search books by price range.
    """
    return crud.search_books_by_price(db, min=min, max=max)


@api_router.get("/books/{id}", response_model=schemas.BookBase)
def get_book(id: int, db: Session = Depends(get_db)):
    """
    Get a book by its ID.
    """
    book = crud.get_book_by_id(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
