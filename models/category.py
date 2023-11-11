from pydantic import BaseModel

from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from core.database import Base


class CategoryModel(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Category(Base):
    __tablename__ = "categories"

    name = Column(String, primary_key=True, index=True)
    products = relationship("Product", back_populates="product_category")


