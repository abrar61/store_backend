from fastapi import APIRouter, HTTPException, Depends, status
from datetime import date

from models.sale import SaleModel, SaleCreate, SaleReturn, Sale
from models.product import Product
from .products import get_product_by_id
from api.v1.dependencies import get_db

from sqlalchemy.orm import Session

from typing import List
from re import match
from api.v1.functions import filter_results_by_created_date, get_and_filter_results

router = APIRouter()


@router.post("/", response_model=SaleModel)
def sell_product(sale: SaleCreate, db: Session = Depends(get_db)):
    db_product = get_product_by_id(product_id=sale.product_id, db=db)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product id")
    elif db_product.count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not available")
    product = get_product_by_id(product_id=sale.product_id, db=db)
    if not sale.sale_price:
        sale.sale_price = product.retail_price
    db_sale = Sale(**sale.model_dump())
    db_sale.profit = sale.sale_price - product.cost_price
    db.add(db_sale)
    setattr(product, "count", product.count - 1)
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.get("/", response_model=List[SaleReturn])
def get_sales(product_name: str = "", category: str = "", sale_date: str = "", db: Session = Depends(get_db)):
    if sale_date:
        if not (match("^\d{4}$|^\d{4}-\d{2}$|^\d{4}-\d{2}-\d{2}$", sale_date)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date")
    results = db.query(Sale)
    if sale_date:
        results = filter_results_by_created_date(sale_date, results, Sale)
    if product_name:
        results = results.filter(Sale.reproduct.name == product_name)
    if category:
        results = results.join(Product).filter(Product.category == category)
    return results.all()


@router.get("/analysis-by-category/")
def get_sales_analysis_by_category(from_date: date = "", to_date: date = "", db: Session = Depends(get_db)):
    if not bool(from_date) == bool(to_date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date input is not valid")
    elif not from_date <= to_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="From date should be less than to date")
    return get_and_filter_results(db, Product.category, Product.category, from_date, to_date)


@router.get("/analysis-by-product/")
def get_sales_analysis_by_product(from_date: date = "", to_date: date = "", db: Session = Depends(get_db)):
    if not bool(from_date) == bool(to_date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date input is not valid")
    elif not from_date <= to_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="From date should be less than to date")
    return get_and_filter_results(db, Product.name, Product.id, from_date, to_date)

