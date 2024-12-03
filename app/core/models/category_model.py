from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text

from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.product_model import dish_category
from app.utils.slug_generate import slugify

if TYPE_CHECKING:
    from app.core.models.product_model import Product


class Category(BaseModel, IdIntPrimaryKeyMixin):
    """Модель категории продуктов"""

    __tablename__ = "categories"

    # Основные поля
    name: Mapped[str] = mapped_column(
        String(100), index=True, nullable=False
    )  # Название категории
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Описание категории
    slug: Mapped[str] = mapped_column(String(150), index=True, unique=True)

    # Отношения
    products: Mapped[List["Product"]] = relationship(
        "Product",
        secondary=dish_category,  # Указываем имя промежуточной таблицы
        back_populates="categories",
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.slug = self.generate_slug()

    def __str__(self):
        return f'ID: "{self.id}" | Название: "{self.name}"'

    def generate_slug(self):
        """Генерирует slug на основе названия ресторана"""
        return slugify(self.name)
