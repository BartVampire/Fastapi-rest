import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime

if TYPE_CHECKING:
    from app.core.models.product_model import Product
    from app.core.models.category_model import Category


class Restaurant(BaseModel, IdIntPrimaryKeyMixin):
    """Модель ресторана"""

    # Основные поля
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default=uuid_pkg.uuid4, primary_key=True, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(150), index=True
    )  # Название ресторана (с индексом для быстрого поиска)
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Описание ресторана
    address: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )  # Адрес ресторана
    is_active: Mapped[bool] = mapped_column(
        default=True, index=True
    )  # Статус активности ресторана
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )  # Дата создания

    # Отношения
    products: Mapped[List["Product"]] = relationship(
        back_populates="restaurant"
    )  # Связь с продуктами
    categories: Mapped[List["Category"]] = relationship(
        back_populates="restaurant", cascade="all, delete-orphan"
    )
