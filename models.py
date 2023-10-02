from datetime import datetime

from sqlalchemy import Integer, String, Float, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    category = Column(String, ForeignKey("categories.name"))
    count = Column(Integer, default=0)
    cost_price = Column(Float)
    retail_price = Column(Float)
    product_category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    name = Column(String, primary_key=True, index=True)
    products = relationship("Product", back_populates="product_category")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="sales")
    sale_price = Column(Float)
    profit = Column(Float)
    created_at = Column(DateTime, default=datetime.now)



