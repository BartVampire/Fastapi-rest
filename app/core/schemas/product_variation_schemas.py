from pydantic import BaseModel, Field
from typing import Optional


class ProductVariationBase(BaseModel):
    name: Optional[str] = Field(None, max_length=150, description="Название вариации")
    price_modifier: float = Field(default=0.0, description="Модификатор цены")
    is_available: bool = Field(default=True, description="Доступность вариации")


class ProductVariationCreate(ProductVariationBase):
    product_id: int = Field(..., description="ID продукта")


class ProductVariationUpdate(ProductVariationBase):
    pass


class ProductVariation(ProductVariationBase):
    id: int = Field(..., description="ID вариации")
    product_id: int = Field(..., description="ID продукта")

    class Config:
        from_attributes = True
