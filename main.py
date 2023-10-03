from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import operations
import models
import schemas
import re
from datetime import date
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.Category, db: Session = Depends(get_db)):
    db_category = operations.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return operations.create_category(db=db, category=category)


@app.post("/products/", response_model=schemas.ProductCreate)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_category = operations.get_category_by_name(db, name=product.category)
    if not db_category:
        raise HTTPException(status_code=400, detail=f"Category {product.category} does not exists")
    return operations.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product])
def get_products(name: str = "", category: str = "", created_date: str = "", db: Session = Depends(get_db)):
    return operations.get_products(db=db, name=name, category=category, created_date=created_date)


@app.post("/sales/", response_model=schemas.Sale)
def sell_product(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_product = operations.get_product_by_id(db, product_id=sale.product_id)
    if not db_product:
        raise HTTPException(status_code=400, detail="Invalid product id")
    elif db_product.count == 0:
        raise HTTPException(status_code=400, detail="Product not available")
    return operations.create_sale(db=db, sale=sale)


@app.get("/sales/", response_model=List[schemas.SaleReturn])
def get_sales(product_name: str = "", category: str = "", sale_date: str = "", db: Session = Depends(get_db)):
    if sale_date:
        if not (re.match("^\d{4}$|^\d{4}-\d{2}$|^\d{4}-\d{2}-\d{2}$", sale_date)):
            raise HTTPException(status_code=400, detail="Invalid date")
    return operations.get_sales(db=db, product_name=product_name, category=category, sale_date=sale_date)


@app.get("/sales-analysis-by-category/")
def get_sales_analysis_by_category(from_date: date = "", to_date: date = "", db: Session = Depends(get_db)):
    if not bool(from_date) == bool(to_date):
        raise HTTPException(status_code=400, detail="Date input is not valid")
    elif not from_date <= to_date:
        raise HTTPException(status_code=400, detail="From date should be less than to date")
    return operations.get_sales_by_category(db=db, from_date=from_date, to_date=to_date)


@app.get("/sales-analysis-by-product/")
def get_sales_analysis_by_product(from_date: date = "", to_date: date = "", db: Session = Depends(get_db)):
    if not bool(from_date) == bool(to_date):
        raise HTTPException(status_code=400, detail="Date input is not valid")
    elif not from_date <= to_date:
        raise HTTPException(status_code=400, detail="From date should be less than to date")
    return operations.get_sales_by_product(db=db, from_date=from_date, to_date=to_date)


@app.get("/inventory/")
def get_inventory(db: Session = Depends(get_db)):
    return operations.get_inventory(db=db)


@app.patch("/update-inventory/")
def update_inventory(products: List[schemas.ProductUpdateCount], db: Session = Depends(get_db)):
    operations.update_inventory(db=db, products=products)
    return {"message": "All records updated"}


@app.get("/product-count-by-category/")
def get_product_count_by_category(db: Session = Depends(get_db)):
    return operations.get_product_count_by_category(db=db)


