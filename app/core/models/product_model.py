from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey, Float, Enum as SQLAEnum, DateTime
from enum import Enum as PyEnum
from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.core.models.category_model import Category
    from app.core.models.restaurant_model import Restaurant
    from app.core.models.product_size_model import ProductSize
    from app.core.models.product_variation_model import ProductVariation


# Перечисление для типов измерения продукта
class MeasurementType(PyEnum):
    WEIGHT = "weight"  # Для продуктов, измеряемых в граммах
    VOLUME = "volume"  # Для продуктов, измеряемых в миллилитрах
    PIECE = "piece"  # Для продуктов, измеряемых в штуках


class Product(BaseModel, IdIntPrimaryKeyMixin):
    """Модель продукта"""

    # Основные поля
    name: Mapped[str] = mapped_column(
        String(150), index=True, nullable=False
    )  # Название продукта
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Описание продукта
    base_price: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # Базовая цена продукта
    measurement_type: Mapped[MeasurementType] = mapped_column(
        SQLAEnum(MeasurementType)
    )  # Тип измерения
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"), index=True
    )  # ID ресторана
    is_available: Mapped[bool] = mapped_column(default=True)  # Доступность продукта
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )  # Дата создания

    # Отношения
    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="products"
    )  # Связь с рестораном
    categories: Mapped[List["Category"]] = relationship(
        secondary="product_categories", back_populates="products"
    )  # Связь с категориями
    variations: Mapped[List["ProductVariation"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )  # Связь с вариациями
    sizes: Mapped[List["ProductSize"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )  # Связь с размерами
