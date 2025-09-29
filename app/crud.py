from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from sqlalchemy import func


def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_books(db: Session, books: List[schemas.BookBase]) -> int:
    # Apaga todos os livros existentes antes de inserir novos
    db.query(models.Book).delete()
    for book in books:
        db_book = models.Book(**book.dict())
        db.add(db_book)
    db.commit()
    return len(books)

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def search_books(db: Session, title: str = None, category: str = None):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(models.Book.category.ilike(f"%{category}%"))
    return query.all()

def search_books_by_price(db: Session, min: float = None, max: float = None):
    query = db.query(models.Book)
    if min:
        query = query.filter(models.Book.price_incl_tax >= min)
    if max:
        query = query.filter(models.Book.price_incl_tax <= max)
    return query.all()

def get_categories(db: Session):
    return [row[0] for row in db.query(models.Book.category).distinct().all()]

def get_stats_overview(db: Session):
    total_books = db.query(models.Book).count()
    average_price = db.query(func.avg(models.Book.price_incl_tax)).scalar() or 0.0

    rating_distribution = dict(
    db.query(
        models.Book.rating,
        func.count(models.Book.id)
    )
    .group_by(models.Book.rating)
    .all()
    )

    return schemas.BookStatsOverview(
        total_books=total_books,
        average_price=float(average_price),
        rating_distribution=rating_distribution
    )


def get_category_overview(db: Session):

    results = db.query(
        models.Book.category,
        func.count(models.Book.id),
        func.avg(models.Book.price_incl_tax)
    ).group_by(models.Book.category).all()

    category_stats = [
        {
            "category": category,
            "total_books": total,
            "average_price": float(avg_price) if avg_price else 0.0
        }
        for category, total, avg_price in results
    ]
    return category_stats

def get_top_rated(db: Session):

    query = db.query(models.Book).filter(models.Book.rating == 5).all()

    return query