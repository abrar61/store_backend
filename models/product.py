from datetime import datetime
from typing import List, Union
from pydantic import BaseModel

from sqlalchemy import Integer, String, Float, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.database import Base
from models.sale import SaleModel


class ProductBase(BaseModel):
    name: str
    description: Union[str, None] = None
    category: str
    cost_price: float
    retail_price: float


class ProductCreate(ProductBase):
    count: int = 0


class ProductModel(ProductBase):
    id: int
    created_at: datetime
    sales: List[SaleModel] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ProductUpdateCount(BaseModel):
    id: int
    count: int

    class Config:
        from_attributes = True


class InventoryProduct(BaseModel):
    id: int
    name: str
    count: int
    criticalLy_low: bool

    class Config:
        from_attributes = True


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True)
    description = Column(String(150), nullable=True)
    category = Column(String(150), ForeignKey("categories.name"))
    count = Column(Integer, default=0)
    cost_price = Column(Float)
    retail_price = Column(Float)
    product_category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
