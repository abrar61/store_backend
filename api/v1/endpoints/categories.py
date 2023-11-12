from fastapi import APIRouter, HTTPException, Depends, status
from models.category import CategoryModel, Category
from api.v1.dependencies import get_db
from api.v1.functions import get_category_by_name, handle_exception_and_log

from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=CategoryModel)
@handle_exception_and_log
def create_category(category: CategoryModel, db: Session = Depends(get_db)):
    db_category = get_category_by_name(name=category.name, db=db)
    if db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/search-by-name/", response_model=CategoryModel)
@handle_exception_and_log
def search_category_by_name(name: str, db: Session = Depends(get_db)):
    db_category = get_category_by_name(name, db)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {name} already exists")
    return db_category

