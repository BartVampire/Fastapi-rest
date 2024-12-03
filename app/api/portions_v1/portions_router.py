from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth_v1.validation_auth_helper import get_superuser_auth
from app.api.portions_v1.portions_crud import PortionsCRUD
from app.core.schemas import product_size_schemas
from app.core.schemas.product_size_schemas import PortionSize
from app.core.models.db_helper import db_helper

router = APIRouter(
    tags=["Portions"],
)


@router.get("/portions/{product_id}", response_model=list[PortionSize])
async def get_portions_by_product_id(
    product_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Роутер для получения всех порций продукта."""
    portions = await PortionsCRUD.get_all_portions_by_product_id(
        db=db, product_id=product_id
    )
    if not portions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден.",
        )
    return portions


@router.post(
    "/",
    response_model=product_size_schemas.PortionSizeCreate,
    dependencies=[Depends(get_superuser_auth)],
)
async def create_new_portion(
    product_id: int,
    portion: product_size_schemas.PortionSizeCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Роутер для создания новой порции продукта."""
    return await PortionsCRUD.create_portion(
        db=db, portion=portion, product_id=product_id
    )


@router.delete(
    "/{portion_id}",
    dependencies=[Depends(get_superuser_auth)],
)
async def delete_portion_router(
    portion_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Роутер для удаления порции продукта."""
    if await PortionsCRUD.delete_portion(db=db, portion_id=portion_id):
        return {"message": "Порция успешно удалена :D"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Порция не найдена.",
        )


@router.put(
    "/{portion_id}",
    response_model=product_size_schemas.PortionSizeUpdate,
    dependencies=[Depends(get_superuser_auth)],
)
async def update_portion_router(
    portion_id: int,
    portion: product_size_schemas.PortionSizeUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Роутер для обновления порции продукта."""
    return await PortionsCRUD.update_portion(
        db=db, portion_id=portion_id, portion=portion
    )
