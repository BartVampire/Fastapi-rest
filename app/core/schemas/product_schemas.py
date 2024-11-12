from datetime import datetime
from typing import List, TYPE_CHECKING

from pydantic import BaseModel, Field, field_validator
from app.core.models.product_model import MeasurementType

if TYPE_CHECKING:
    from app.core.models.category_model import Category
    from app.core.models.restaurant_model import Restaurant
    from app.core.models.product_size_model import ProductSize
    from app.core.models.product_variation_model import ProductVariation


class ProductBase(BaseModel):
    """Базовая схема для продукта"""

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        examples=["Хинкали"],
        description="Название продукта",
    )  # Название продукта
    description: [str | None] = Field(
        description="Описание продукта", default=None
    )  # Описание
    base_price: float = Field(..., gt=0, description="Базовая цена продукта")
    measurement_type: MeasurementType = Field(
        ...,
        description="Тип измерения продукта",
    )  # Тип измерения
    restaurant_id: int = (Field(..., description="ID ресторана"),)
    is_available: bool = Field(..., description="Доступность продукта")

    @field_validator("base_price")
    def validate_price(self, v):
        """Проверка, что цена положительная"""
        if v <= 0:
            raise ValueError("Цена должна быть положительная")
        return v


class ProductCreate(ProductBase):
    """Схема для создания продукта"""

    category_ids: List[int] = Field(..., description="Список ID категорий")


class ProductUpdate(ProductBase):
    """Схема для обновления продукта"""

    category_ids: List[int] = Field(..., description="Список ID категорий")


class Product(ProductBase):
    """Схема для отображения продукта"""

    id: int = Field(..., description="ID продукта")
    created_at: datetime = Field(..., description="Дата создания")
    restaurant: Restaurant = Field(..., description="Информация о ресторане")
    categories: List[Category] = Field(default=[], description="Категории продукта")
    variations: List[ProductVariation] = Field(
        default=[], description="Вариации продукта"
    )
    sizes: List[ProductSize] = Field(default=[], description="Размеры продукта")

    class Config:
        """Класс конфигурации"""

        # Позволяет использовать поля модели
        from_attributes = True
