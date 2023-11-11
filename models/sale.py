from datetime import datetime
from pydantic import BaseModel

from sqlalchemy import Integer, Float, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.database import Base


class SaleBase(BaseModel):
    product_id: int
    sale_price: float

    class Config:
        from_attributes = True


class SaleCreate(SaleBase):
    pass


class SaleModel(SaleBase):
    id: int
    profit: float

    class Config:
        from_attributes = True


class SaleReturn(SaleBase):
    id: int
    profit: float
    created_at: datetime

    class Config:
        from_attributes = True


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="sales")
    sale_price = Column(Float)
    profit = Column(Float)
    created_at = Column(DateTime, default=datetime.now)


