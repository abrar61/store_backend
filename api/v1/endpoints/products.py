from fastapi import APIRouter, HTTPException, Depends, status
from models.product import ProductModel, ProductCreate, ProductUpdateCount, InventoryProduct, Product
from .categories import get_category_by_name
from api.v1.dependencies import get_db
from api.v1.functions import get_product_by_id, handle_exception_and_log

from sqlalchemy.orm import Session
from sqlalchemy import case

from typing import List
from api.v1.functions import filter_results_by_created_date

router = APIRouter()


@router.post("/", response_model=ProductCreate)
@handle_exception_and_log
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_category = get_category_by_name(name=product.category, db=db)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category {product.category} does not exists")
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/id/{product_id}/", response_model=ProductModel)
@handle_exception_and_log
def search_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product_by_id(product_id, db)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with {product_id} already exists")
    return db_product


@router.get("/name/{name}/", response_model=List[ProductModel])
@handle_exception_and_log
def get_products_by_name(name: str, created_date: str = "", db: Session = Depends(get_db)):
    results = db.query(Product)
    if created_date:
        results = filter_results_by_created_date(created_date, results, Product)
    results = results.filter(Product.name == name)
    return results.all()


@router.get("/category/{category}/", response_model=List[ProductModel])
@handle_exception_and_log
def search_products_by_category(category: str, created_date: str = "", db: Session = Depends(get_db)):
    results = db.query(Product)
    if created_date:
        results = filter_results_by_created_date(created_date, results, Product)
    results = results.join(Product).filter(Product.category == category)
    return results.all()


@router.get("/inventory/", response_model=List[InventoryProduct])
@handle_exception_and_log
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Product.id, Product.name, Product.count,
                    case(
                       (Product.count < 10, True),
                       else_=False
                    ).label("criticalLy_low")).all()


@router.patch("/update-inventory/", response_model=List[InventoryProduct])
@handle_exception_and_log
def update_inventory(products: List[ProductUpdateCount], db: Session = Depends(get_db)):
    product_list = []
    for product in products:
        db_product = get_product_by_id(product_id=product.id, db=db)
        if db_product:
            setattr(db_product, "count", product.count)
            db.commit()
            db.refresh(db_product)
            product_list.append(db_product)
    return product_list




