from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth_v1.validation_auth_helper import get_superuser_auth
from app.api.products_v1.products_crud import ProductsCRUD
from app.core.models.db_helper import db_helper
from app.core.schemas import product_schemas
from app.core.schemas.product_schemas import Product

router = APIRouter(
    tags=["Products"],
)


@router.get("/products/{restaurant_id}/", response_model=List[Product])
async def get_list_products(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    restaurant_id: Optional[int] = None,
):
    """Получение списка продуктов"""
    products = await ProductsCRUD.get_all_products(
        db=db,
        restaurant_id=restaurant_id,
    )
    return products


@router.get("/products/{product_id}", response_model=product_schemas.Product)
async def get_product(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_id: int,
):
    """Получение продукта"""
    product = await ProductsCRUD.get_product_by_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден.",
        )
    return product


@router.post(
    "/products/",
    response_model=product_schemas.ProductCreate,
    response_model_exclude={"portions"},
)
async def create_product_portion(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_data: product_schemas.ProductCreate,
):
    """Создание только продукта"""
    return await ProductsCRUD.create_only_product(db=db, product_data=product_data)


@router.put("/products/{product_id}", response_model=product_schemas.ProductUpdate)
async def update_product(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_id: int,
):
    """Обновление продукта"""
    product_update = await ProductsCRUD.get_product_by_id(db=db, product_id=product_id)
    if not product_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден.",
        )
    product = await ProductsCRUD.update_product(
        db=db, product_id=product_id, product=product_update
    )

    return product


@router.delete("/products/{product_id}", dependencies=[Depends(get_superuser_auth)])
async def delete_product(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_id: int,
):
    product_delete = await ProductsCRUD.get_product_by_id(db=db, product_id=product_id)
    if not product_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден.",
        )
    if not await ProductsCRUD.delete_product(db=db, product_id=product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не удалось удалить продукт.",
        )
    return {"message": "Продукт успешно удален :D"}
