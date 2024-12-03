import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from app.utils.slug_generate import slugify
from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime

if TYPE_CHECKING:
    from app.core.models.product_model import Product
    from app.core.models.user_model import User


class Restaurant(BaseModel, IdIntPrimaryKeyMixin):
    """Модель ресторана"""

    # Основные поля
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default=uuid_pkg.uuid4, primary_key=True, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(150), index=True
    )  # Название ресторана (с индексом для быстрого поиска)
    slug: Mapped[str] = mapped_column(
        String(150), index=True, unique=True
    )  # Slug для ресторана (с индексом для быстрого поиска)

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Описание ресторана
    address: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )  # Адрес ресторана
    is_active: Mapped[bool] = mapped_column(
        default=True, index=True
    )  # Статус активности ресторана
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)  # Изображение
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )  # Дата создания
    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        default=None,
    )  # Связь с владельцем

    # Отношения
    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="restaurant"
    )  # Связь с продуктами
    owner: Mapped["User"] = relationship("User", back_populates="restaurants")

    def __init__(self, **data):
        super().__init__(**data)
        self.slug = self.generate_slug()

    def __str__(self):
        return f'ID: "{self.id}" | Название: "{self.name}" | Адрес: "{self.address}"'

    def generate_slug(self):
        """Генерирует slug на основе названия ресторана"""
        return slugify(self.name)
