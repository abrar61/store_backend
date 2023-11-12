from fastapi import APIRouter, HTTPException, Depends, status
from models.product import ProductModel, ProductCreate, ProductUpdateCount, InventoryProduct, Product
from .categories import get_category_by_name
from api.v1.dependencies import get_db
from api.v1.functions import get_product_by_id, handle_exception_and_log, filter_results_by_created_date

from sqlalchemy.orm import Session
from sqlalchemy import case

from typing import List

router = APIRouter()


# Endpoint to create a new product
@router.post("/", response_model=ProductCreate)
@handle_exception_and_log
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Check if the specified category exists in the database
    db_category = get_category_by_name(name=product.category, db=db)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Category {product.category} does not exist")

    # Create a new Product instance using the data from the request
    db_product = Product(**product.model_dump())

    # Add the new product to the database
    db.add(db_product)

    # Commit the transaction to persist the changes
    db.commit()

    # Refresh the product object to get the updated database state
    db.refresh(db_product)

    # Return the created product
    return db_product


# Endpoint to search for a product by ID
@router.get("/id/{product_id}/", response_model=ProductModel)
@handle_exception_and_log
def search_product_by_id(product_id: int, db: Session = Depends(get_db)):
    # Retrieve the product from the database by ID
    db_product = get_product_by_id(product_id, db)

    # If the product does not exist, raise an HTTPException
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with ID {product_id} does not exist")

    # Return the retrieved product
    return db_product


# Endpoint to get products by name
@router.get("/name/{name}/", response_model=List[ProductModel])
@handle_exception_and_log
def get_products_by_name(name: str, created_date: str = "", db: Session = Depends(get_db)):
    results = db.query(Product)

    # Filter results by created date if specified
    if created_date:
        results = filter_results_by_created_date(created_date, results, Product)

    # Filter results by product name
    results = results.filter(Product.name == name)

    # Return the list of products
    return results.all()


# Endpoint to search for products by category
@router.get("/category/{category}/", response_model=List[ProductModel])
@handle_exception_and_log
def search_products_by_category(category: str, created_date: str = "", db: Session = Depends(get_db)):
    results = db.query(Product)

    # Filter results by created date if specified
    if created_date:
        results = filter_results_by_created_date(created_date, results, Product)

    # Join tables and filter results by product category
    results = results.join(Product).filter(Product.category == category)

    # Return the list of products
    return results.all()


# Endpoint to get inventory status
@router.get("/inventory/", response_model=List[InventoryProduct])
@handle_exception_and_log
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Product.id, Product.name, Product.count,
                    case(
                        (Product.count < 10, True),
                        else_=False
                    ).label("criticalLy_low")).all()


# Endpoint to update product inventory counts
@router.patch("/update-inventory/", response_model=List[InventoryProduct])
@handle_exception_and_log
def update_inventory(products: List[ProductUpdateCount], db: Session = Depends(get_db)):
    product_list = []
    for product in products:
        # Retrieve the product from the database by ID
        db_product = get_product_by_id(product_id=product.id, db=db)
        if db_product:
            # Update the product count
            setattr(db_product, "count", product.count)
            db.commit()
            db.refresh(db_product)
            product_list.append(db_product)

    # Return the list of updated products
    return product_list
