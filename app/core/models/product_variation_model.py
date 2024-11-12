from typing import TYPE_CHECKING

from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

if TYPE_CHECKING:
    from app.core.models.product_model import Product


class ProductVariation(BaseModel, IdIntPrimaryKeyMixin):
    """Модель вариации продукта (например, разные виды мяса)"""

    # Основные поля
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), index=True
    )  # ID продукта
    name: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )  # Название вариации
    price_modifier: Mapped[float] = mapped_column(default=0.0)  # Модификатор цены
    is_available: Mapped[bool] = mapped_column(default=True)  # Доступность вариации

    # Отношения
    product: Mapped["Product"] = relationship(
        back_populates="variations"
    )  # Связь с продуктом
