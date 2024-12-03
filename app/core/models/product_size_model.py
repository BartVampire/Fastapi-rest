from sqlalchemy import Enum, Float, String
from typing import TYPE_CHECKING

from app.core.models.base_model import BaseModel
from app.core.mixins.id_int_pk import IdIntPrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.core.models.product_model import MeasurementType

if TYPE_CHECKING:
    from app.core.models.product_model import Product


class Portion(BaseModel, IdIntPrimaryKeyMixin):
    """Модель размера порции продукта"""

    # Основные поля
    name: Mapped[str] = mapped_column(
        String(150), index=True, nullable=False
    )  # Название порции
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), index=True
    )  # ID продукта
    unit_type: Mapped[MeasurementType] = mapped_column(
        Enum(MeasurementType)
    )  # Тип измерения
    size: Mapped[float] = mapped_column(Float)  # Значение размера (в граммах или мл)
    price: Mapped[float] = mapped_column(Float)  # Модификатор цены
    is_available: Mapped[bool] = mapped_column(default=True)  # Доступность размера

    # Отношения
    product: Mapped["Product"] = relationship(
        back_populates="portions"
    )  # Связь с продуктом

    def __str__(self):
        return f'ID: "{self.id}" | Название: "{self.name}" | Тип: "{self.unit_type}" | Размер: "{self.size}" | Цена: "{self.price}"'
