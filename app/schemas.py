"""
Pydantic schemas for data validation and serialization of books and API responses.
"""

from pydantic import BaseModel
from typing import Dict


class ScrapeResponse(BaseModel):
    """
    Schema for scrape response indicating number of inserted records.
    """

    inserted: int


class BookBase(BaseModel):
    """
    Base schema for book data.
    """

    id: int | None = None
    title: str
    category: str
    rating: int
    description: str
    upc: str
    product_type: str
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    num_available: int
    num_reviews: int
    image_url: str

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    """
    Schema for book creation (inherits from BookBase).
    """

    pass


class BookStatsOverview(BaseModel):
    """
    Schema for book statistics overview.
    """

    total_books: int
    average_price: float
    rating_distribution: Dict[int, int] = {"1": 10, "2": 5, "3": 20, "4": 15, "5": 50}


class BookStatsCategory(BaseModel):
    """
    Schema for statistics of a book category.
    """

    category: str
    total_books: int
    average_price: float


class MLBookFeatures(BaseModel):
    """
    Schema for ML features extracted from books.
    """

    category: str
    rating: int
    price_excl_tax: float
    price_incl_tax: float
    num_available: int
    num_reviews: int


class LoginResponse(BaseModel):
    """
    Schema for login response containing JWT token.
    """

    access_token: str
    token_type: str
