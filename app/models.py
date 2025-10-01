from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Book(Base):
    """
    SQLAlchemy model for the books table.
    """
    __tablename__ = "tb_books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    upc = Column(String, nullable=False, unique=True)
    product_type = Column(String, nullable=False)
    price_excl_tax = Column(Float, nullable=False)
    price_incl_tax = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    num_available = Column(Integer, nullable=False)
    num_reviews = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)


from sqlalchemy import DateTime
from datetime import datetime

class RequestLog(Base):
    """
    SQLAlchemy model for logging HTTP requests.
    """
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    http_method = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    duration_ms = Column(Float, nullable=False)
    created_ts = Column(DateTime, default=datetime.utcnow, nullable=False)
