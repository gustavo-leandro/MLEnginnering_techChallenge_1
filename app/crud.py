from sqlalchemy.orm import Session
from . import models, schemas
from typing import List


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

def get_categories(db: Session):
    return [row[0] for row in db.query(models.Book.category).distinct().all()]