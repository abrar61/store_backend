from dateutil.parser import parse
from fastapi import HTTPException, status
from datetime import time, datetime
from functools import wraps
import logging

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from models.product import Product
from models.sale import Sale
from models.category import Category


def parse_date(d):
    try:
        return parse(d)
    except:
        return False


def handle_exception_and_log(fun):
    @wraps(fun)
    def inner(*args, **kwargs):
        try:
            logging.info(f"Function {fun.__name__} is accessed")
            output = fun(*args, **kwargs)
            logging.info(f"Output of function {fun.__name__} is {output}")
            return output
        except HTTPException as e:
            logging.error(f"Exception raised in function {fun.__name__} is {e.detail}")
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            logging.error(f"Error in function {fun.__name__} is {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return inner


def filter_results_by_created_date(created_date, results, model):
    parsed_date = parse_date(created_date)
    if not parsed_date:
        raise HTTPException(status_code=400, detail="Invalid date")
    # Filter by year
    results = results.filter(extract("year", model.created_at) == parsed_date.year)
    if len(created_date) > 4:
        # Filter by month
        results = results.filter(extract("month", model.created_at) == parsed_date.month)
    if len(created_date) > 7:
        # Filter by day
        results = results.filter(extract("day", model.created_at) == parsed_date.day)
    return results


def get_and_filter_results(db: Session, column, group_by_column, from_date, to_date):
    results = db.query(column,
                       func.count(Product.sales).label("total_sales"),
                       func.sum(Sale.sale_price).label("revenue"),
                       func.sum(Sale.profit).label("profit")
                       )
    if to_date and from_date:
        results = (results.filter(Product.created_at >= datetime.combine(from_date, time.min)).
                   filter(Product.created_at <= datetime.combine(to_date, time.max)))
    return results.join(Sale.product).group_by(group_by_column)


def get_category_by_name(name: str, db: Session):
    return db.query(Category).filter(Category.name == name).first()


def get_product_by_id(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()
