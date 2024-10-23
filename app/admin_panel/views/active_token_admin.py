from sqladmin import ModelView

from app.core.models import ActiveToken


class ActiveTokenAdmin(ModelView, model=ActiveToken):
    column_labels = {
        "uuid": "Уникальный идентификатор",
        "access_token": "Токен доступа",
        "refresh_token": "Токен обновления",
        "access_expires_at": "Дата и время истечения токена доступа",
        "refresh_expires_at": "Дата и время истечения токена обновления",
        "user_agent": "Пользовательский агент",
        "ip_address": "IP адрес пользователя",
        "users": "Пользователь",
        "user_id": "Идентификатор пользователя",
    }
    # Список полей, которые будут сортироваться по умолчанию
    column_sortable_list = ["access_expires_at", "refresh_expires_at", "created_at"]
    # Список полей, которые будут отображаться в админке
    column_list = [ActiveToken.users] + [
        "uuid",
        "access_token",
        "refresh_token",
        "access_expires_at",
        "refresh_expires_at",
        "user_agent",
        "ip_address",
        "created_at",
    ]

    column_searchable_list = [
        "uuid",
        "access_token",
        "user_agent",
        "ip_address",
        "refresh_token",
    ]

    # Список столбцов которые можно редактировать
    form_columns = (
        ActiveToken.users,
        ActiveToken.access_token,
        ActiveToken.refresh_token,
    )
    name = "Активный токены"
    name_plural = "Активные токены"

    icon = "fa-solid fa-key"
