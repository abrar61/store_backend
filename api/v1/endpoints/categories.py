from fastapi import APIRouter, HTTPException, Depends, status
from models.category import CategoryModel, Category
from api.v1.dependencies import get_db
from api.v1.functions import get_category_by_name, handle_exception_and_log

from sqlalchemy.orm import Session

router = APIRouter()


# Endpoint to create a new category
@router.post("/", response_model=CategoryModel)
@handle_exception_and_log
def create_category(category: CategoryModel, db: Session = Depends(get_db)):
    # Check if the category already exists in the database
    db_category = get_category_by_name(name=category.name, db=db)
    if db_category:
        # Raise an HTTPException if the category already exists
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    # Create a new Category instance using the data from the request
    db_category = Category(**category.model_dump())

    # Add the new category to the database
    db.add(db_category)

    # Commit the transaction to persist the changes
    db.commit()

    # Refresh the category object to get the updated database state
    db.refresh(db_category)

    # Return the created category
    return db_category


# Endpoint to search for a category by name
@router.get("/search-by-name/", response_model=CategoryModel)
@handle_exception_and_log
def search_category_by_name(name: str, db: Session = Depends(get_db)):
    # Retrieve the category from the database by name
    db_category = get_category_by_name(name, db)

    # If the category does not exist, raise an HTTPException
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {name} does not exist")

    # Return the retrieved category
    return db_category
