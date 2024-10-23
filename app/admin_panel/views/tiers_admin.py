from sqladmin import ModelView

from app.core.models import Tier


class TierAdmin(ModelView, model=Tier):
    """Класс TierAdmin представляет собой админпанель для уровня доступа."""

    column_list = ("id", "name", "created_at", "updated_at")
    column_labels = {
        "id": "ID",
        "name": "Название",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
    }
    column_searchable_list = ("id", "name")
    column_details_list = ("id", "name", "created_at", "updated_at")
    form_columns = (
        "name",
        "created_at",
        "updated_at",
    )

    name = "Уровень доступа"
    name_plural = "Уровни доступа"
    icon = "fa-solid fa-layer-group"
