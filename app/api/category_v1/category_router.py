from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth_v1.validation_auth_helper import get_superuser_auth
from app.api.category_v1.category_crud import CategoryCRUD
from app.core.schemas import category_schemas
from app.core.models.db_helper import db_helper

router = APIRouter(
    tags=["Categories"],
)


@router.post(
    "/",
    dependencies=[Depends(get_superuser_auth)],
    response_model=category_schemas.CategoryCreate,
)
async def create_new_category_router(
    category: category_schemas.CategoryCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await CategoryCRUD.create_new_category(db=db, category=category)


@router.put(
    "/{category_id}",
    dependencies=[Depends(get_superuser_auth)],
    response_model=category_schemas.CategoryUpdate,
)
async def update_category_router(
    category_id: int,
    category: category_schemas.CategoryUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await CategoryCRUD.update_category(
        db=db, category_id=category_id, category=category
    )


@router.delete("/{category_id}", dependencies=[Depends(get_superuser_auth)])
async def delete_category_router(
    category_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    await CategoryCRUD.delete_category(db=db, category_id=category_id)
    return {"message": "Категория успешно удалена :D"}
