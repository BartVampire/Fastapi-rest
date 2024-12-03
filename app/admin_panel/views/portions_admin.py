import asyncio

from sqladmin import ModelView
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.core.models.db_helper import db_helper
from app.core.models.product_model import Product
from app.core.models.product_size_model import Portion


class PortionAdmin(ModelView, model=Portion):
    """Админка для порций продукта"""

    # Поле для выбора продуктов
    form_args = {
        "product_id": {
            "query_factory": lambda: PortionAdmin._get_products(),  # Асинхронный вызов
            "label": "Продукт",
        }
    }

    # Название моделей в админке
    column_labels = {
        "id": "Идентификатор",
        "name": "Название порции",
        "product_id": "Идентификатор продукта",
        "unit_type": "Тип измерения",
        "size": "Значение размера",
        "price": "Цена",
        "is_available": "Доступность",
        "product": "Продукт",
        "restaurant": "Ресторан",  # Добавлено поле для ресторана
        "product.name": "Название продукта",
        "product.restaurant.name": "Название ресторана",
    }

    # Список полей которые будут отображаться в админке
    column_list = (
        Portion.name,
        Portion.product_id,
        "product.name",  # Имя продукта
        "product.restaurant.name",  # Имя ресторана
        Portion.unit_type,
        Portion.size,
        Portion.price,
        Portion.is_available,
    )

    # Нельзя удалять порции
    can_delete = False
    # Список столбцов которые можно сортировать
    column_sortable_list = (
        Portion.product_id,
        "product.name",
        "product.restaurant.name",
    )

    # Поиск по полям
    column_searchable_list = (Portion.name, "product.name")
    # Фильтры
    column_filters = (Portion.is_available, Portion.product_id)

    # Колонки для редактирования
    form_columns = (
        Portion.name,
        Portion.product_id,  # Поле для выбора продукта
        Portion.unit_type,
        Portion.size,
        Portion.price,
        Portion.is_available,
    )

    name = "Порция продукта"
    name_plural = "Порции продукта"
    icon = "fa fa-cutlery"

    @staticmethod
    async def _fetch_products():
        """Асинхронный метод для получения продуктов с ресторанами"""
        async with db_helper.session_getter() as session:
            result = await session.execute(
                select(Product).options(joinedload(Product.restaurant))
            )
            query = result.scalars().all()
            return query

    @staticmethod
    def _get_products():
        """Обертка для вызова асинхронного метода в синхронной среде"""
        return asyncio.run(PortionAdmin._fetch_products())
