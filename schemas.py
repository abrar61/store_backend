from typing import List, Union
from pydantic import BaseModel

from datetime import datetime


class SaleBase(BaseModel):
    product_id: int
    sale_price: float

    class Config:
        from_attributes = True


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: int
    profit: float

    class Config:
        from_attributes = True


class Category(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Union[str, None] = None
    category: str
    cost_price: float
    retail_price: float


class ProductCreate(ProductBase):
    count: int = 0


class Product(ProductBase):
    id: int
    sales: List[Sale] = []

    class Config:
        from_attributes = True


class ProductUpdateCount(BaseModel):
    id: int
    count: int

    class Config:
        from_attributes = True

