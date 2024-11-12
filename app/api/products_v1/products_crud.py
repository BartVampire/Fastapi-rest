import logging
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.category_model import Category
from app.core.models.product_model import Product
from app.core.models.restaurant_model import Restaurant
from app.core.schemas import product_schemas

logger = logging.getLogger(__name__)


class ProductsCRUD:

    @staticmethod
    async def get_all_products(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 150,
        restaurant_id: Optional[int] = None,
        category_id: Optional[int] = None,
        is_available: Optional[bool] = None,
    ) -> List[Product]:
        try:
            query = await db.execute(select(Product))
            if restaurant_id:
                query = query.where(Product.restaurant_id == restaurant_id)
            if category_id:
                query = query.join(Product.categories).filter(
                    Product.categories.id == category_id
                )
            if is_available is not None:
                query = query.where(Product.is_available == is_available)
            result = query.offset(skip).limit(limit)
            products = result.scalars().all()
            return list(products)
        except Exception as e:
            logger.error(f"Ошибка при получении списка продуктов: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукты не найдены.",
            )

    @staticmethod
    async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
        try:
            result = await db.execute(select(Product).where(Product.id == product_id))
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Ошибка при получении продукта по ID: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукт не найден.",
            )

    @staticmethod
    async def create_product(
        db: AsyncSession, product: product_schemas.ProductCreate
    ) -> Optional[Product]:
        try:
            restaurant = await db.execute(
                select(Restaurant).filter(Restaurant.id == product.restaurant_id)
            )
            if not restaurant.scalar_one_or_none():
                logger.error(f"Ресторан с ID {product.restaurant_id} не найден.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Ресторан не найден."
                )

            categories = await db.execute(
                select(Category).filter(Category.id.in_(product.category_ids))
            )
            if len(categories.scalars().all()) != len(product.category_ids):
                logger.error(f"Категории с ID {product.category_ids} не найдены.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категории не найдены.",
                )

            db_product = Product(**product.model_dump(exclude={"category_ids"}))
            db_product.categories = categories.scalars().all()
            db.add(db_product)
            await db.commit()
            await db.refresh(db_product)
            return db_product
        except Exception as e:
            logger.error(f"Ошибка при создании продукта: {str(e)}")
            return None

    @staticmethod
    async def update_product(
        db: AsyncSession, product_id: int, product: product_schemas.ProductUpdate
    ) -> Optional[Product]:
        try:
            result = await db.execute(select(Product).where(Product.id == product_id))
            db_product = result.scalar_one_or_none()
            if db_product:
                for key, value in product.model_dump().items():
                    setattr(db_product, key, value)
                await db.commit()
                await db.refresh(db_product)
                return db_product
            return None
        except Exception as e:
            logger.error(f"Ошибка при обновлении продукта: {str(e)}")
            return None

    @staticmethod
    async def delete_product(db: AsyncSession, product_id: int) -> bool:
        try:
            result = await db.execute(select(Product).where(Product.id == product_id))
            db_product = result.scalar_one_or_none()
            if db_product:
                await db.delete(db_product)
                await db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка при удалении продукта: {str(e)}")
            return False
