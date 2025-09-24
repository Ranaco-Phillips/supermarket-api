from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db_setup import Base

class Supermarket(Base):
    __tablename__ = "supermarkets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    website = Column(String, unique=True, nullable=False)

    # relationships
    products = relationship("Product", back_populates="supermarket")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slug = Column(String, unique=True, index=True)  # e.g. "cakes-bread"
    name = Column(String, unique=True, index=True)  # e.g. "Bakery & Bread"
    description = Column(String, nullable=True)     # optional, could hold longer info

    # relationships
    products = relationship("Product", back_populates="category")
    

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # foreign keys
    supermarket_id = Column(Integer, ForeignKey("supermarkets.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    # relationships
    supermarket = relationship("Supermarket", back_populates="products")
    category = relationship("Category", back_populates="products")


# (Optional) price history if you want to track changes
class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
