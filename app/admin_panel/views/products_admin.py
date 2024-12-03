from fastapi import UploadFile
from sqladmin import ModelView
from sqlalchemy.ext.asyncio import AsyncSession
from wtforms import FileField
from wtforms.validators import Optional
from app.api.category_v1.category_crud import CategoryCRUD
from app.core.models import db_helper
from app.core.models.product_model import Product
from app.utils.upload_image import save_image, delete_image


class ProductAdmin(ModelView, model=Product):
    """Админка для продуктов"""

    # Название моделей в админке
    column_labels = {
        "id": "Идентификатор",
        "uuid": "Уникальный идентификатор",
        "name": "Название продукта",
        "description": "Описание продукта",
        "image_url": "URL изображения",
        "product_id": "Идентификатор ресторана",
        "category_id": "Идентификатор категории",
        "created_at": "Дата создания",
        "restaurant": "Ресторан",
    }

    # Список полей которые будут отображаться в админке
    column_list = (
        Product.uuid,
        Product.name,
        "restaurant",
        Product.description,
        Product.image_url,
        Product.restaurant_id,
        Product.category_id,
        Product.created_at,
    )

    # Список полей которые не будут отображаться в админке
    column_details_exclude_list = [Product.id]
    # Нельзя удалять продукты
    can_delete = True
    # Можно редактировать
    can_edit = True

    # Список столбцов которые можно сортировать
    column_sortable_list = (
        Product.created_at,
        Product.name,
        Product.restaurant_id,
        Product.category_id,
        "restaurant",
    )

    # Список столбцов которые можно поискать
    column_searchable_list = (
        Product.uuid,
        Product.name,
        Product.category_id,
        Product.restaurant_id,
    )

    # Список столбцов которые можно редактировать
    # Поля формы
    form_columns = ["name", "description", "restaurant_id", "category_id", "image_url"]
    # Добавляем поле для загрузки изображения
    form_extra_fields = {"image": FileField("Изображение", validators=[Optional()])}

    name = "Продукт"
    name_plural = "Продукты"
    icon = "fa fa-coffee"

    async def on_model_change(
        self, data: dict, model: Product, is_created: bool
    ) -> None:
        """
        Вызывается при сохранении объекта через админку.
        """
        new_image = data.pop("image", None)  # Извлекаем изображение из данных формы

        if new_image:
            # Сохраняем новое изображение
            upload_file = UploadFile(
                new_image.filename, new_image.stream, new_image.content_type
            )
            model.image_url = await save_image(upload_file, model.name)
        elif not is_created:
            # Если изображение не загружается, оставляем текущее
            model.image_url = model.image_url

    async def on_model_delete(self, model: Product) -> None:
        """
        Вызывается при удалении объекта через админку.
        """
        # Удаляем изображение, если объект удаляется
        await delete_image(model.image_url)

        # Настройка ForeignKey-полей

    form_args = {
        # "restaurant_id": {
        #     "query_factory": lambda: get_all_categories,
        #     "label": "Ресторан",
        # },
        "category_id": {
            "query_factory": lambda: CategoryCRUD.get_all_categories(
                db=db_helper.session_getter()
            ),
            "label": "Категория",
        },
    }
