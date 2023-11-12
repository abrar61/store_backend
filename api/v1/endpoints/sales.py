from fastapi import APIRouter, HTTPException, Depends, status
from datetime import date

from models.sale import SaleModel, SaleCreate, SaleReturn, SaleAnalysis, Sale
from models.product import Product
from .products import get_product_by_id
from api.v1.dependencies import get_db

from sqlalchemy.orm import Session

from typing import List
from re import match
from api.v1.functions import filter_results_by_created_date, get_and_filter_results, handle_exception_and_log

router = APIRouter()


# Endpoint to create sale of a product
@router.post("/", response_model=SaleModel)
@handle_exception_and_log
def sell_product(sale: SaleCreate, db: Session = Depends(get_db)):
    # Retrieve the product from the database by ID
    db_product = get_product_by_id(product_id=sale.product_id, db=db)

    # Check if the product with the specified ID exists
    if not db_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product ID")
    # Check if the product is available (count > 0)
    elif db_product.count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not available")

    # Retrieve the product again (for details like retail price)
    product = get_product_by_id(product_id=sale.product_id, db=db)

    # If sale price is not provided, use retail price as sale price
    if not sale.sale_price:
        sale.sale_price = product.retail_price

    # Create a new Sale instance using the data from the request
    db_sale = Sale(**sale.model_dump())

    # Calculate profit for the sale
    db_sale.profit = sale.sale_price - product.cost_price

    # Add the new sale to the database
    db.add(db_sale)

    # Update product count
    setattr(product, "count", product.count - 1)

    # Commit the transaction to persist the changes
    db.commit()

    # Refresh the sale object to get the updated database state
    db.refresh(db_sale)

    # Return the created sale
    return db_sale


# Endpoint to get sales with optional filters
@router.get("/", response_model=List[SaleReturn])
@handle_exception_and_log
def get_sales(product_name: str = "", category: str = "", sale_date: str = "", db: Session = Depends(get_db)):
    # Validate sale_date format
    if sale_date:
        if not (match("^\d{4}$|^\d{4}-\d{2}$|^\d{4}-\d{2}-\d{2}$", sale_date)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")

    # Start with all sales records
    results = db.query(Sale)

    # Filter results by created date if specified
    if sale_date:
        results = filter_results_by_created_date(sale_date, results, Sale)

    # Filter results by product name if specified
    if product_name:
        results = results.filter(Sale.reproduct.name == product_name)

    # Filter results by product category if specified
    if category:
        results = results.join(Product).filter(Product.category == category)

    # Return the list of sales
    return results.all()


# Endpoint to get sales analysis by category
@router.get("/analysis-by-category/", response_model=List[SaleAnalysis])
@handle_exception_and_log
def get_sales_analysis_by_category(from_date: date = "", to_date: date = "", db: Session = Depends(get_db)):
    # Validate date input (either both dates should be in input or neither)
    if not bool(from_date) == bool(to_date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date input")
    elif not from_date <= to_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="From date should be less than or equal to to date")

    # Use a common function to get and filter results based on category
    return get_and_filter_results(db, Product.category, Product.category, from_date, to_date)


# Endpoint to get sales analysis by product
@router.get("/analysis-by-product/", response_model=List[SaleAnalysis])
@handle_exception_and_log
def get_sales_analysis_by_product(from_date: date = "", to_date: date = "", db: Session = Depends(get_db)):
    # Validate date input (either both dates should be in input or neither)
    if not bool(from_date) == bool(to_date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date input")
    elif not from_date <= to_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="From date should be less than or equal to to date")

    return get_and_filter_results(db, Product.name, Product.id, from_date, to_date)
