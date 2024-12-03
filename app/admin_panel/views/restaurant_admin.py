from sqladmin import ModelView
from app.core.models.restaurant_model import Restaurant


class RestaurantAdmin(ModelView, model=Restaurant):
    """Админка для ресторанов"""

    # Название моделей в админке
    column_labels = {
        "id": "Идентификатор",
        "uuid": "Уникальный идентификатор",
        "name": "Название ресторана",
        "slug": "Слаг ресторана",
        "description": "Описание ресторана",
        "address": "Адрес ресторана",
        "phone": "Номер телефона",
        "is_active": "Активен",
        "image_url": "URL изображения",
        "created_at": "Дата создания",
        "owner_id": "Идентификатор владельца ресторана",
    }

    # Список полей которые будут отображаться в админке
    column_list = (
        Restaurant.uuid,
        Restaurant.name,
        Restaurant.slug,
        Restaurant.description,
        Restaurant.address,
        Restaurant.is_active,
        Restaurant.image_url,
        Restaurant.phone,
        Restaurant.created_at,
        Restaurant.owner_id,
    )

    # Список полей которые не будут отображаться в админке
    column_details_exclude_list = [Restaurant.id]
    # Нельзя удалять рестораны
    can_delete = False
    # Список столбцов которые можно сортировать
    column_sortable_list = (
        Restaurant.created_at,
        Restaurant.name,
        Restaurant.is_active,
    )

    # Список столбцов которые можно поискать
    column_searchable_list = (
        Restaurant.uuid,
        Restaurant.name,
        Restaurant.phone,
        Restaurant.address,
    )

    # Список столбцов которые можно редактировать
    form_columns = (
        Restaurant.name,
        Restaurant.slug,
        Restaurant.description,
        Restaurant.address,
        Restaurant.is_active,
        Restaurant.image_url,
        Restaurant.phone,
        Restaurant.owner_id,
    )

    name = "Ресторан"
    name_plural = "Рестораны"
    icon = "fa fa-copyright"
