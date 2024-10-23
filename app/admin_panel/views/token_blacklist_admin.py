from sqladmin import ModelView

from app.core.models import TokenBlackList


class TokenBlacklistAdmin(ModelView, model=TokenBlackList):
    column_list = ("username", "access_token", "refresh_token", "created_at")
    column_searchable_list = ("username", "access_token", "refresh_token")
    column_sortable_list = ("created_at",)

    column_labels = {
        "uuid": "Уникальный идентификатор",
        "username": "Имя пользователя",
        "access_token": "Токен доступа",
        "refresh_token": "Токен обновления",
        "access_expires_at": "Дата и время истечения токена доступа",
        "refresh_expires_at": "Дата и время истечения токена обновления",
        "created_at": "Дата создания",
    }

    name = "Токены в черном списке"
    name_plural = "Токены в черном списке"
    icon = "fa-solid fa-lock"
