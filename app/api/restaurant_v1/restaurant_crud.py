import logging
from uuid import UUID
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.models.restaurant_model import Restaurant
from fastapi import HTTPException, status

from app.core.schemas import restaurant_schemas, product_schemas

logger = logging.getLogger(__name__)

# ========================
# CRUD для Restaurant
# ========================


class RestaurantCRUD:
    # ====================================
    # Функция получения ресторана по UUID
    # ====================================
    @staticmethod
    async def get_restaurant_by_uuid(
        db: AsyncSession,
        restaurant_uuid: Optional[UUID] = None,
    ) -> Optional[Restaurant]:
        try:
            query_restaurant = await db.execute(
                select(Restaurant).where(Restaurant.uuid == restaurant_uuid)
            )
            return query_restaurant.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Ошибка при получении ресторана по UUID: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ресторан не найден.",
            )

    # ====================================
    # Функция получения всех ресторанов
    # ====================================
    @staticmethod
    async def get_all_restaurants(
        db: AsyncSession,
    ) -> List[Restaurant]:
        try:
            query_restaurants = await db.execute(select(Restaurant))
            result = query_restaurants.scalars().all()
            return list(result)
        except Exception as e:
            logger.error(f"Ошибка при получении всех ресторанов: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рестораны не найдены.",
            )

    # ====================================
    # Функция создания ресторана
    # ====================================
    @staticmethod
    async def create_restaurant(
        db: AsyncSession, restaurant: restaurant_schemas.RestaurantCreate
    ) -> Restaurant:
        try:
            restaurant = Restaurant(**restaurant.model_dump())
            db.add(restaurant)
            await db.commit()
            await db.refresh(restaurant)
            return restaurant
        except Exception as e:
            logger.error(f"Ошибка при создании ресторана: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Невозможно создать ресторан.",
            )

    # ====================================
    # Функция удаления ресторана
    # ====================================
    @staticmethod
    async def delete_restaurant(db: AsyncSession, restaurant_id: int) -> bool:
        try:
            result = await db.execute(
                select(Restaurant).where(Restaurant.id == restaurant_id)
            )
            db_restaurant = result.scalar_one_or_none()
            if db_restaurant:
                await db.delete(db_restaurant)
                await db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка при удалении ресторана: {str(e)}")
            return False

    # ====================================
    # Функция обновления ресторана
    # ====================================
    @staticmethod
    async def update_restaurant(
        db: AsyncSession,
        restaurant_id: int,
        updated_restaurant: restaurant_schemas.RestaurantUpdate,
    ) -> Restaurant:
        try:
            db_restaurant = await db.execute(
                select(Restaurant).where(Restaurant.id == restaurant_id)
            )
            db_restaurant = db_restaurant.scalar_one_or_none()
            if not db_restaurant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ресторан не найден.",
                )
            for key, value in updated_restaurant.model_dump().items():
                setattr(db_restaurant, key, value)
            await db.commit()
            await db.refresh(db_restaurant)
            return db_restaurant
        except Exception as e:
            logger.error(f"Ошибка при обновлении ресторана: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Невозможно обновить ресторан.",
            )
