import logging
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.models.category_model import Category
from app.core.models.product_model import Product
from app.core.models.product_size_model import Portion
from app.core.models.restaurant_model import Restaurant
from app.core.schemas import product_schemas, product_size_schemas

logger = logging.getLogger(__name__)


class ProductsCRUD:

    @staticmethod
    async def get_all_products(
        db: AsyncSession,
        restaurant_id: Optional[int] = None,
    ) -> List[Product]:
        try:
            query_products = await db.execute(
                select(Product)
                .where(Product.restaurant_id == restaurant_id)
                .options(selectinload(Product.portions))
            )
            products = query_products.scalars().all()
            return list(products)
        except Exception as e:
            logger.error(f"Ошибка при получении списка продуктов: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукты не найдены.",
            )

    @staticmethod
    async def create_only_product(
        db: AsyncSession, product_data: product_schemas.ProductCreate
    ) -> Optional[Product]:
        try:
            db_product = Product(**product_data.model_dump())
            db.add(db_product)
            await db.commit()
            await db.refresh(db_product)
            return db_product
        except Exception as e:
            logger.error(f"Ошибка при создании продукта: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Невозможно создать продукт.",
            )

    @staticmethod
    async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
        try:
            result = await db.execute(
                select(Product)
                .where(Product.id == product_id)
                .options(
                    selectinload(Product.portions),
                )
            )
            product = result.scalar_one_or_none()
            return product
        except Exception as e:
            logger.error(f"Ошибка при получении продукта по ID: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Продукт не найден.",
            )

    @staticmethod
    async def create_product_with_portions(
        db: AsyncSession,
        dish_data: product_schemas.ProductCreate,
        portions_data: List[product_size_schemas.PortionSizeCreate],
    ) -> Optional[Product]:
        try:
            restaurant = await db.execute(
                select(Restaurant).filter(Restaurant.id == dish_data.restaurant_id)
            )
            if not restaurant.scalar_one_or_none():
                logger.error(f"Ресторан с ID {dish_data.restaurant_id} не найден.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Ресторан не найден."
                )

            categories = await db.execute(
                select(Category).filter(Category.id == dish_data.category_id)
            )
            if not categories.scalars().all():
                logger.error(f"Категории с ID {dish_data.category_ids} не найдены.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категории не найдены.",
                )

            db_product = Product(**dish_data.model_dump(exclude={"category_ids"}))
            db_product.categories = categories.scalars().all()
            db.add(db_product)
            await db.commit()
            await db.refresh(db_product)

            for portion_data in portions_data:
                portion_data["dish_id"] = db_product.id
                db_portion = Portion(**portion_data.model_dump())
                db.add(db_portion)
            await db.commit()
            return db_product
        except Exception as e:
            logger.error(f"Ошибка при создании продукта: {str(e)}")
            return None

    @staticmethod
    async def update_product(
        db: AsyncSession,
        product_id: int,
        product: Optional[product_schemas.ProductUpdate],
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
