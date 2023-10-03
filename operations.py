from sqlalchemy import func, case, extract
from sqlalchemy.orm import Session
from datetime import time, datetime
from dateutil.parser import parse
from fastapi import HTTPException
from typing import List
import models
import schemas


def create_category(db: Session, category: schemas.Category):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, name=str, category=str, created_date=str):
    results = db.query(models.Product)
    if created_date:
        parsed_date = parse_date(created_date)
        if not parsed_date:
            raise HTTPException(status_code=400, detail="Invalid date")
        # Filter by year
        results = results.filter(extract("year", models.Product.created_at) == parsed_date.year)
        if len(created_date) > 4:
            # Filter by month
            results = results.filter(extract("month", models.Product.created_at) == parsed_date.month)
        if len(created_date) > 7:
            # Filter by day
            results = results.filter(extract("day", models.Product.created_at) == parsed_date.day)
    if name:
        results = results.filter(models.Product.name == name)
    if category:
        results = results.join(models.Product).filter(models.Product.category == category)
    return results.all()


def get_sales(db: Session, product_name=str, category=str, sale_date=str):
    results = db.query(models.Sale)
    if sale_date:
        parsed_date = parse_date(sale_date)
        if not parsed_date:
            raise HTTPException(status_code=400, detail="Invalid date")
        # Filter by year
        results = results.filter(extract("year", models.Sale.created_at) == parsed_date.year)
        if len(sale_date) > 4:
            # Filter by month
            results = results.filter(extract("month", models.Sale.created_at) == parsed_date.month)
        if len(sale_date) > 7:
            # Filter by day
            results = results.filter(extract("day", models.Sale.created_at) == parsed_date.day)
    if product_name:
        results = results.filter(models.Sale.product.name == product_name)
    if category:
        results = results.join(models.Product).filter(models.Product.category == category)
    return results.all()


def get_products_by_category(db: Session, category: str, limit: int = 100):
    return db.query(models.Product).filter(models.Product.category == category).limit(limit).all()


def create_sale(db: Session, sale: schemas.SaleCreate):
    product = get_product_by_id(db, product_id=sale.product_id)
    if not sale.sale_price:
        sale.sale_price = product.retail_price
    db_sale = models.Sale(**sale.model_dump())
    db_sale.profit = sale.sale_price - product.cost_price
    db.add(db_sale)
    setattr(product, "count", product.count - 1)
    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_sales_by_category(db: Session, from_date, to_date):
    return get_and_filter_results(db, models.Product.category, models.Product.category, from_date, to_date)


def get_sales_by_product(db: Session, from_date, to_date):
    return get_and_filter_results(db, models.Product.name, models.Product.id, from_date, to_date)


def get_and_filter_results(db: Session, column, group_by_column, from_date, to_date):
    results = db.query(column,
                       func.count(models.Product.sales).label("total_sales"),
                       func.sum(models.Sale.sale_price).label("revenue"),
                       func.sum(models.Sale.profit).label("profit")
                       )
    if to_date and from_date:
        results = (results.filter(models.Product.created_at >= datetime.combine(from_date, time.min)).
                   filter(models.Product.created_at <= datetime.combine(to_date, time.max)))
    results = results.join(models.Sale.product).group_by(group_by_column)
    return [r._mapping for r in results]


def get_inventory(db: Session):
    results = db.query(models.Product.id, models.Product.name, models.Product.count,
                       case(
                           (models.Product.count < 10, True),
                           else_=False
                       ).label("criticalLy_low"))
    return [r._mapping for r in results]


def update_inventory(db: Session, products: List):
    for product in products:
        db_product = get_product_by_id(db, product.id)
        if db_product:
            setattr(db_product, "count", product.count)
            db.commit()
            db.refresh(db_product)


def get_product_count_by_category(db: Session):
    return db.query(models.Product.category,
                    func.count(models.Product.id).label("product_count")
                    ).group_by(models.Product.category)


def parse_date(d):
    try:
        return parse(d)
    except:
        return False

