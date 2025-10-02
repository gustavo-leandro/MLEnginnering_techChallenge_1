"""
CRUD operations for Book and RequestLog models.
Provides database interaction functions for books and request logging.
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[models.Book]:
    """
    Retrieve a paginated list of books from the database.
    """
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_books(db: Session, books: List[schemas.BookBase]) -> int:
    """
    Delete all existing books and insert new ones.
    """
    db.query(models.Book).delete()
    for book in books:
        db_book = models.Book(**book.dict())
        db.add(db_book)
    db.commit()
    return len(books)


def get_book_by_id(db: Session, book_id: int):
    """
    Retrieve a book by its ID.
    """
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def search_books(db: Session, title: str = None, category: str = None):
    """
    Search books by title and/or category.
    """
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(models.Book.category.ilike(f"%{category}%"))
    return query.all()


def search_books_by_price(db: Session, min: float = None, max: float = None):
    """
    Search books by price range.
    """
    query = db.query(models.Book)
    if min:
        query = query.filter(models.Book.price_incl_tax >= min)
    if max:
        query = query.filter(models.Book.price_incl_tax <= max)
    return query.all()


def get_categories(db: Session):
    """
    Get a list of all distinct book categories.
    """
    return [row[0] for row in db.query(models.Book.category).distinct().all()]


def get_stats_overview(db: Session):
    """
    Get overview statistics for books: total, average price, rating distribution.
    """
    total_books = db.query(models.Book).count()
    average_price = db.query(func.avg(models.Book.price_incl_tax)).scalar() or 0.0

    rating_distribution = dict(
        db.query(models.Book.rating, func.count(models.Book.id))
        .group_by(models.Book.rating)
        .all()
    )

    return schemas.BookStatsOverview(
        total_books=total_books,
        average_price=float(average_price),
        rating_distribution=rating_distribution,
    )


def get_category_overview(db: Session):
    """
    Get statistics for each book category.
    """
    results = (
        db.query(
            models.Book.category,
            func.count(models.Book.id),
            func.avg(models.Book.price_incl_tax),
        )
        .group_by(models.Book.category)
        .all()
    )

    category_stats = [
        {
            "category": category,
            "total_books": total,
            "average_price": float(avg_price) if avg_price else 0.0,
        }
        for category, total, avg_price in results
    ]
    return category_stats


def get_top_rated(db: Session):
    """
    Get all books with the highest rating (5).
    """
    return db.query(models.Book).filter(models.Book.rating == 5).all()


def create_request_log(
    db: Session, http_method: str, endpoint: str, status_code: int, duration_ms: float
):
    """
    Create a log entry for an HTTP request.
    """
    log = models.RequestLog(
        http_method=http_method,
        endpoint=endpoint,
        status_code=status_code,
        duration_ms=duration_ms,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
