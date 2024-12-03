import logging
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.core.models.product_size_model import Portion
from app.core.schemas import product_size_schemas

logger = logging.getLogger(__name__)


class PortionsCRUD:
    @staticmethod
    async def get_all_portions_by_product_id(
        db: AsyncSession, product_id: int
    ) -> List[Portion]:
        """Получение всех порций продукта"""
        try:
            result = await db.execute(
                select(Portion).where(Portion.product_id == product_id)
            )
            result = result.scalars().all()
            return list(result)
        except Exception as e:
            logger.error(f"Ошибка при получении всех порций продукта: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукт не найден.",
            )

    @staticmethod
    async def get_portion_by_id(db: AsyncSession, portion_id: int) -> Optional[Portion]:
        """Получение порции по ID"""
        try:
            result = await db.execute(select(Portion).where(Portion.id == portion_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Ошибка при получении порции по ID: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Порция не найдена.",
            )

    @staticmethod
    async def create_portion(
        db: AsyncSession,
        portion: product_size_schemas.PortionSizeCreate,
        product_id: int,
    ) -> Portion:
        """Создание порции продукта"""
        try:
            db_portion = Portion(**portion.model_dump(), product_id=product_id)
            db.add(db_portion)
            await db.commit()
            await db.refresh(db_portion)
            return db_portion
        except Exception as e:
            logger.error(f"Ошибка при создании порции продукта: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Невозможно создать порцию продукта.",
            )

    @staticmethod
    async def update_portion(
        db: AsyncSession,
        portion_id: int,
        portion: product_size_schemas.PortionSizeUpdate,
    ) -> Portion:
        """Обновление порции продукта"""
        try:
            db_portion = await PortionsCRUD.get_portion_by_id(
                db=db, portion_id=portion_id
            )
            if not db_portion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Порция не найдена.",
                )
            for key, value in portion.model_dump().items():
                setattr(db_portion, key, value)
            await db.commit()
            await db.refresh(db_portion)
            return db_portion
        except Exception as e:
            logger.error(f"Ошибка при обновлении порции продукта: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    async def delete_portion(db: AsyncSession, portion_id: int) -> bool:
        """Удаление порции продукта"""
        try:
            result = await db.execute(select(Portion).where(Portion.id == portion_id))
            db_portion = result.scalar_one_or_none()
            if db_portion:
                await db.delete(db_portion)
                await db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка при удалении порции продукта: {str(e)}")
            return False
