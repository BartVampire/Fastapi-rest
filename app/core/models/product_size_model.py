from typing import TYPE_CHECKING

from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from app.core.models.product_model import Product


class ProductSize(BaseModel, IdIntPrimaryKeyMixin):
    """Модель размера порции продукта"""

    # Основные поля
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), index=True
    )  # ID продукта
    size: Mapped[float]  # Значение размера (в граммах или мл)
    price_modifier: Mapped[float]  # Модификатор цены
    is_available: Mapped[bool] = mapped_column(default=True)  # Доступность размера

    # Отношения
    product: Mapped["Product"] = relationship(
        back_populates="sizes"
    )  # Связь с продуктом

    @property
    def final_price(self) -> float:
        """Вычисление финальной цены с учетом модификатора"""
        return self.product.base_price + self.price_modifier
