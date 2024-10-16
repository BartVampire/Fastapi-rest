import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .mixins.id_int_pk import IdIntPrimaryKeyMixin
from .base_model import BaseModel


class Tier(IdIntPrimaryKeyMixin, BaseModel):
    """
    Класс Tier представляет собой модель уровня доступа в базе данных. Он наследует от IdIntPrimaryKeyMixin и BaseModel
    Поля класса:
    .name: Mapped[str] - Название уровня доступа. Строка длиной до 255 символов. Это поле не может быть NULL и должно быть уникальным.
    .created_at: Mapped[datetime.datetime] - Дата и время создания записи уровня доступа. Устанавливается автоматически на текущее время в формате UTC при создании записи.
    .updated_at: Mapped[datetime.datetime | None]- Дата и время последнего обновления записи уровня доступа. По умолчанию None, что означает, что значение не установлено при создании.
    """

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default_factory=lambda: datetime.UTC
    )
    updated_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, default=None)
