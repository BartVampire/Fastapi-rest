from datetime import datetime
from typing import List, TYPE_CHECKING, Optional

from pydantic import BaseModel, Field, field_validator


from app.core.schemas.category_schemas import CategoryInit
from app.core.schemas.product_size_schemas import PortionSize, PortionSizeCreate


class ProductBase(BaseModel):
    """Базовая схема для продукта"""

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        examples=["Хинкали"],
        description="Название продукта",
    )  # Название продукта
    description: Optional[str] = Field(
        description="Описание продукта", default=None
    )  # Описание
    image_url: Optional[str] = Field(
        description="URL изображения продукта", default=None
    )  # URL изображения

    restaurant_id: int = Field(..., description="ID ресторана")
    category_id: Optional[int] = Field(
        description="ID категории", default=None
    )  # ID категории

    # @field_validator("base_price")
    # def validate_price(self, v):
    #     """Проверка, что цена положительная"""
    #     if v <= 0:
    #         raise ValueError("Цена должна быть положительная")
    #     return v


class ProductCreate(ProductBase):
    """Схема для создания продукта"""

    pass


class ProductCreateWithPortions(ProductBase):
    """Схема для создания продукта с порциями"""

    portions: List["PortionSizeCreate"] = Field(
        ..., description="Варианты порций продукта"
    )


class ProductUpdate(ProductBase):
    """Схема для обновления продукта"""

    pass


class Product(ProductBase):
    """Схема для отображения продукта"""

    id: int = Field(..., description="ID продукта")
    created_at: datetime = Field(..., description="Дата создания")
    restaurant_id: int = Field(..., description="ID ресторана")
    # categories: List["CategoryInit"] = Field(
    #     default=[], description="Категории продукта"
    # )
    category_id: Optional[int] = Field(..., description="ID категории")
    portions: List["PortionSize"] = Field(default=[], description="Порции продукта")

    class Config:
        """Класс конфигурации"""

        # Позволяет использовать поля модели
        from_attributes = True
