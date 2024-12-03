import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from app.api.restaurant_v1.restaurant_router import get_restaurant_by_uuid_with_products
from app.core.models.restaurant_model import Restaurant
from app.jinja2_main.jinja2_templates import templates

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Index"],
)


@router.get("/")
async def index_page(
    request: Request,
    restaurant_uuid: Optional[UUID | str] = Query(None),  # Параметр из строки запроса
    restaurant: dict = Depends(get_restaurant_by_uuid_with_products),
):
    print(f"Request headers: {request.headers}")
    print(f"Is AJAX: {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")
    restaurant_db: dict | Restaurant = restaurant.get("restaurant")
    categories: list = restaurant.get("categories")
    products: list = restaurant.get("products")
    pagination: dict = restaurant.get("pagination")

    if isinstance(restaurant_db, Restaurant):  # Если это модель
        restaurant_uuid = restaurant_db.uuid
    elif isinstance(restaurant_db, dict):  # Если это словарь
        restaurant_uuid = restaurant_db.get("uuid", None)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Возвращаем только HTML для сетки продуктов и пагинации
        return templates.TemplateResponse(
            "includes/menu-section.html",
            {
                "request": request,
                "products": products,
                "pagination": pagination,
                "categories": categories,
                "restaurant_uuid": restaurant_uuid,
            },
        )

    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "restaurant": restaurant_db,
            "categories": categories,
            "products": products,
            "restaurant_uuid": restaurant_uuid,
            "pagination": restaurant.get("pagination"),
        },
    )


@router.get("/menu/")
async def menu_page(
    request: Request,
    restaurant_uuid: Optional[UUID | str] = Query(None),  # Параметр из строки запроса
    restaurant: dict = Depends(get_restaurant_by_uuid_with_products),
):
    restaurant_db: dict | Restaurant = restaurant.get("restaurant")
    categories: list = restaurant.get("categories")
    products: list = restaurant.get("products")
    if isinstance(restaurant_db, Restaurant):  # Если это модель
        restaurant_uuid = restaurant_db.uuid
    elif isinstance(restaurant_db, dict):  # Если это словарь
        restaurant_uuid = restaurant_db.get("uuid", None)

    return templates.TemplateResponse(
        name="menu.html",
        context={
            "request": request,
            "restaurant": restaurant_db,
            "categories": categories,
            "products": products,
            "restaurant_uuid": restaurant_uuid,
            "pagination": restaurant.get("pagination"),
        },
    )


@router.get("/menu/")
async def about_page(
    request: Request,
    restaurant_uuid: Optional[UUID | str] = Query(None),  # Параметр из строки запроса
    restaurant: dict = Depends(get_restaurant_by_uuid_with_products),
):
    restaurant_db: dict | Restaurant = restaurant.get("restaurant")
    categories: list = restaurant.get("categories")
    products: list = restaurant.get("products")
    if isinstance(restaurant_db, Restaurant):  # Если это модель
        restaurant_uuid = restaurant_db.uuid
    elif isinstance(restaurant_db, dict):  # Если это словарь
        restaurant_uuid = restaurant_db.get("uuid", None)

    return templates.TemplateResponse(
        name="menu.html",
        context={
            "request": request,
            "restaurant": restaurant_db,
            "categories": categories,
            "products": products,
            "restaurant_uuid": restaurant_uuid,
            "pagination": restaurant.get("pagination"),
        },
    )


@router.get("/menu/")
async def contact_page(
    request: Request,
    restaurant_uuid: Optional[UUID | str] = Query(None),  # Параметр из строки запроса
    restaurant: dict = Depends(get_restaurant_by_uuid_with_products),
):
    restaurant_db: dict | Restaurant = restaurant.get("restaurant")
    categories: list = restaurant.get("categories")
    products: list = restaurant.get("products")
    if isinstance(restaurant_db, Restaurant):  # Если это модель
        restaurant_uuid = restaurant_db.uuid
    elif isinstance(restaurant_db, dict):  # Если это словарь
        restaurant_uuid = restaurant_db.get("uuid", None)

    return templates.TemplateResponse(
        name="menu.html",
        context={
            "request": request,
            "restaurant": restaurant_db,
            "categories": categories,
            "products": products,
            "restaurant_uuid": restaurant_uuid,
            "pagination": restaurant.get("pagination"),
        },
    )
