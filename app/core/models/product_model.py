import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING, Optional

from fastapi import UploadFile
from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime,
    Table,
    Column,
    Integer,
)
from enum import Enum as PyEnum
from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.upload_image import MEDIA_DIR, save_image, delete_image

if TYPE_CHECKING:
    from app.core.models.category_model import Category
    from app.core.models.restaurant_model import Restaurant
    from app.core.models.product_size_model import Portion

# Связующая таблица для продуктов и категорий
dish_category = Table(
    "dish_category",
    BaseModel.metadata,
    Column(
        "product_id", Integer, ForeignKey("products.id"), primary_key=True
    ),  # Внешний ключ на products.id
    Column(
        "category_id", Integer, ForeignKey("categories.id"), primary_key=True
    ),  # Внешний ключ на categories.id
)


# Перечисление для типов измерения продукта
class MeasurementType(PyEnum):
    GRAMS = "grams"  # Для продуктов, измеряемых в граммах
    MILLILITERS = "milliliters"  # Для продуктов, измеряемых в миллилитрах
    PIECE = "piece"  # Для продуктов, измеряемых в штуках


class Product(BaseModel, IdIntPrimaryKeyMixin):
    """Модель продукта"""

    __tablename__ = "products"
    # Основные поля
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default=uuid_pkg.uuid4, primary_key=True, unique=True
    )
    name: Mapped[str] = mapped_column(
        String(150), index=True, nullable=False
    )  # Название продукта
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Описание продукта
    image_url: Mapped[str | None] = mapped_column(
        String, nullable=True
    )  # Изображение продукта

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"), index=True
    )  # ID ресторана
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )  # Дата создания

    restaurant: Mapped["Restaurant"] = relationship(
        "Restaurant", back_populates="products"
    )
    categories: Mapped[List["Category"]] = relationship(
        "Category",
        secondary=dish_category,  # Указываем имя промежуточной таблицы
        back_populates="products",
    )
    portions: Mapped[List["Portion"]] = relationship(
        "Portion", back_populates="product", cascade="all, delete-orphan"
    )

    class Config:
        orm_mode = True

    def __str__(self):
        return f'ID: "{self.id}" | Название: "{self.name}" | Ресторан: "{self.restaurant_id}", Категория: "{self.category_id}"'

    @property
    def image_url_path(self) -> Optional[str]:
        """Возвращает URL изображения если оно существует"""
        if self.image_url:
            return f"/{MEDIA_DIR}/{self.image_url}"
        return None

    async def update_image(self, new_image: Optional[UploadFile] = None) -> None:
        """Обновляет изображение услуги"""
        # Удаляем старое изображение если оно есть
        await delete_image(self.image_url)

        # Сохраняем новое изображение если оно предоставлено
        if new_image:
            self.image_url = await save_image(new_image, self.name)
        else:
            self.image_url = None
