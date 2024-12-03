import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.core.models.category_model import Category
from app.core.schemas import category_schemas

logger = logging.getLogger(__name__)


class CategoryCRUD:
    @staticmethod
    async def get_all_categories(db: AsyncSession) -> List[Category]:
        try:
            result = await db.execute(select(Category).order_by(Category.name))
            result = result.scalars().all()
            return list(result)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категории не найдены.",
            )

    @staticmethod
    async def get_category_by_id(
        db: AsyncSession, category_id: int
    ) -> Optional[Category]:
        try:
            result = await db.execute(
                select(Category).where(Category.id == category_id)
            )
            result = result.scalars().first()
            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена.",
            )

    @staticmethod
    async def create_new_category(
        db: AsyncSession, category: category_schemas.CategoryCreate
    ) -> Category:
        try:
            db_category = Category(**category.model_dump())
            db.add(db_category)
            await db.commit()
            await db.refresh(db_category)
            return db_category
        except Exception as e:
            logger.error(f"Ошибка при создании категории: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать категорию.",
            )

    @staticmethod
    async def update_category(
        db: AsyncSession, category_id: int, category: category_schemas.CategoryUpdate
    ) -> Category:
        try:
            db_category = await CategoryCRUD.get_category_by_id(
                db=db, category_id=category_id
            )
            if not db_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категория не найдена.",
                )
            for key, value in category.model_dump().items():
                setattr(db_category, key, value)
            await db.commit()
            await db.refresh(db_category)
            return db_category
        except Exception as e:
            logger.error(f"Ошибка при обновлении категории: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось обновить категорию.",
            )

    @staticmethod
    async def delete_category(db: AsyncSession, category_id: int) -> None:
        try:
            db_category = await CategoryCRUD.get_category_by_id(
                db=db, category_id=category_id
            )
            if not db_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категория не найдена.",
                )
            await db.delete(db_category)
            await db.commit()
        except Exception as e:
            logger.error(f"Ошибка при удалении категории: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось удалить категорию.",
            )
