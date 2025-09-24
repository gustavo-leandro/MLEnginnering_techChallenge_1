from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"  # nome da tabela no banco

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
