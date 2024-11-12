from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey

from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.core.models.product_model import Product
    from app.core.models.restaurant_model import Restaurant


class Category(BaseModel, IdIntPrimaryKeyMixin):
    """Модель категории продуктов"""

    # Основные поля
    name: Mapped[str] = mapped_column(
        String(100), index=True, nullable=False
    )  # Название категории
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Описание категории
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id")
    )  # ID родительской категории

    # Отношения
    products: Mapped[List["Product"]] = relationship(
        secondary="product_categories", back_populates="categories"
    )  # Связь с продуктами через промежуточную таблицу
    subcategories: Mapped[List["Category"]] = relationship(
        "Category",
        backref="parent",
        remote_side="Category.id",
    )  # Связь для иерархии категорий
    restaurant: Mapped["Restaurant"] = relationship(back_populates="categories")
