from fastapi import APIRouter

from api.v1.endpoints import products, sales, categories

router = APIRouter()

router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(sales.router, prefix="/sales", tags=["sales"])
router.include_router(categories.router, prefix="/categories", tags=["categories"])

