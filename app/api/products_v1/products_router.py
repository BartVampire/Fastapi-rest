from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.products_v1.products_crud import ProductsCRUD
from app.core.models.db_helper import db_helper
from app.core.schemas.product_schemas import Product

router = APIRouter(
    tags=["Products"],
)


@router.get("/products", response_model=List[Product])
async def get_list_products(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    skip: int = 0,
    limit: int = 100,
    restaurant_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_available: Optional[bool] = None,
):
    """Получение списка продуктов"""
    products = await ProductsCRUD.get_all_products(
        db=db,
        skip=skip,
        limit=limit,
        restaurant_id=restaurant_id,
        category_id=category_id,
        is_available=is_available,
    )
    return products
