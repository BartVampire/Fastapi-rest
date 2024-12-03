import math
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy import select, inspect, func
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from sqlalchemy.orm import selectinload, joinedload

from app.api.auth_v1.validation_auth_helper import get_superuser_auth
from app.api.restaurant_v1.restaurant_crud import RestaurantCRUD
from app.core.models.product_size_model import Portion
from app.core.models.category_model import Category
from app.core.models.product_model import Product
from app.core.models.db_helper import db_helper
from app.core.redis import get_redis
from app.core.redis_utils import cache_get, cache_set, to_dict
from app.core.schemas import restaurant_schemas

router = APIRouter(
    tags=["Restaurants"],
)


# ========================
# Роутеры для Restaurant
# ========================


@router.get("/restaurant/{restaurant_uuid}/")
async def get_restaurant_by_uuid_with_products(
    restaurant_uuid: UUID,
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(1, ge=1, le=25, description="Размер страницы"),
    category_filter: Optional[str] = Query(None, description="Фильтр по категории"),
    db: AsyncSession = Depends(db_helper.session_getter),
    redis: Redis = Depends(get_redis),
):
    # Определяем ключ для кэша
    cache_key = f"restaurant:{restaurant_uuid}:with_products:{page}:{page_size}:{category_filter}"

    # Проверяем кэш
    cached_data = await cache_get(redis, cache_key)
    if cached_data:
        return cached_data

    # Получаем ресторан
    db_restaurant = await RestaurantCRUD.get_restaurant_by_uuid(db, restaurant_uuid)
    if not db_restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ресторан не найден.",
        )

    # Получаем все категории ресторана
    categories_query = (
        select(Category)
        .join(Product)
        .where(Product.restaurant_id == db_restaurant.id)
        .distinct()
    )
    categories = await db.execute(categories_query)
    categories = categories.scalars().all()

    # Базовый запрос продуктов
    products_query = (
        select(Product)
        .options(joinedload(Product.portions))
        .where(Product.restaurant_id == db_restaurant.id)
    )

    # Применяем фильтр по категории, если указан
    if category_filter:
        products_query = products_query.join(Category).where(
            Category.slug == category_filter
        )

    # Подсчет общего количества продуктов
    products_query_2 = products_query.subquery()
    # Создаем запрос для подсчета
    total_products_query = select(func.count()).select_from(products_query_2)
    total_products = await db.execute(total_products_query)
    total_products_count = total_products.scalar_one()

    # Добавляем пагинацию
    offset = (page - 1) * page_size
    products_query = products_query.order_by(Product.id).offset(offset).limit(page_size)

    # Получаем продукты
    products = await db.execute(products_query)
    products = products.scalars().unique().all()

    # Подготавливаем данные для ответа
    products_data = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "image_url": product.image_url,
            "category": {
                "id": product.category_id,
            },
            "portions": [
                {
                    "id": portion.id,
                    "name": portion.name,
                    "unit_type": portion.unit_type.value,
                    "size": portion.size,
                    "price": portion.price,
                    "is_available": portion.is_available,
                }
                for portion in product.portions
            ],
        }
        products_data.append(product_data)
    # Проверка, является ли запрос AJAX

    response_data = {
        "restaurant": to_dict(db_restaurant),
        "categories": [
            {"id": cat.id, "name": cat.name, "slug": cat.slug} for cat in categories
        ],
        "products": products_data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_products": total_products_count,
            "total_pages": math.ceil(total_products_count / page_size),
            "current_category": category_filter,
        },
    }

    # Кэшируем результат
    await cache_set(redis=redis, key=cache_key, value=response_data)
    return response_data


@router.get(
    "/restaurants/",
)
async def get_all_restaurants(
    db: AsyncSession = Depends(db_helper.session_getter),
    redis: Redis = Depends(get_redis),
):
    # # Определяем ключ для кэша
    # cache_key = "all_restaurants_routes"
    # # Проверяем кэш
    # cached_data = await cache_get(redis, cache_key)
    # if cached_data:
    #     return cached_data
    # Если кэш пустой, запрашиваем данные из базы данных
    restaurants = await RestaurantCRUD.get_all_restaurants(db=db)
    # # Добавляем данные в кэш
    # await cache_set(redis, cache_key, restaurants)
    return restaurants


@router.post("/", dependencies=[Depends(get_superuser_auth)])
async def create_new_restaurant(
    restaurant: restaurant_schemas.RestaurantCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await RestaurantCRUD.create_restaurant(db=db, restaurant=restaurant)


@router.delete("/", dependencies=[Depends(get_superuser_auth)])
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    await RestaurantCRUD.delete_restaurant(db=db, restaurant_id=restaurant_id)
    return {"message": "Ресторан успешно удален :D"}


@router.put("/", dependencies=[Depends(get_superuser_auth)])
async def update_restaurant(
    restaurant_id: int,
    updated_restaurant: restaurant_schemas.RestaurantUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await RestaurantCRUD.update_restaurant(
        db=db, restaurant_id=restaurant_id, updated_restaurant=updated_restaurant
    )
