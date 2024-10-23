from sqladmin import ModelView
from app.core.models.user_model import User
from datetime import datetime


class UserAdmin(ModelView, model=User):
    """Админка для юзеров"""

    # Название моделей в админке
    column_labels = {
        "username": "Имя пользователя",
        "email": "Электронная почта",
        "phone_number": "Номер телефона",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "is_active": "Подтвержден",
        "created_at": "Дата регистрации",
        "uuid": "Уникальный идентификатор",
        "updated_at": "Дата обновления",
        "deleted_at": "Дата удаления",
        "id": "Идентификатор",
        "is_deleted": "Удаленный пользователь",
        "active_tokens": "Активные токены",
        "tiers": "Уровень доступа",
        "tier_id": "Идентификатор уровня доступа",
    }

    # Список полей которые будут отображаться в админке
    column_list = (
        User.tiers,
        User.id,
        User.first_name,
        User.last_name,
        User.username,
        User.email,
        User.phone_number,
        User.is_active,
        User.created_at,
    )

    # Список полей которые не будут отображаться в админке
    column_details_exclude_list = [User.hashed_password, User.is_superuser]
    # Нельзя удалять пользователя
    can_delete = False
    # Список столбцов которые можно сортировать
    column_sortable_list = (
        User.is_active,
        User.created_at,
    )

    # Список столбцов которые можно поискать
    column_searchable_list = (
        User.tiers,
        User.username,
        User.email,
        User.phone_number,
        User.first_name,
        User.last_name,
        User.id,
        User.uuid,
    )

    # Список столбцов которые можно редактировать
    form_columns = (
        User.first_name,
        User.last_name,
        User.username,
        User.email,
        User.phone_number,
        User.is_active,
        User.tiers,
    )

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa fa-user-ninja"
