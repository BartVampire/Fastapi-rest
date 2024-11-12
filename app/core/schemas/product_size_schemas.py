from pydantic import BaseModel, Field


class ProductSizeBase(BaseModel):
    size: float = Field(
        ..., gt=0, description="Значение размера (в граммах, мл. или шт.)"
    )
    price_modifier: float = Field(default=0.0, description="Модификатор цены")
    is_available: bool = Field(default=True, description="Доступность размера")


class ProductSizeCreate(ProductSizeBase):
    product_id: int = Field(..., description="ID продукта")


class ProductSizeUpdate(ProductSizeBase):
    pass


class ProductSize(ProductSizeBase):
    id: int = Field(..., description="ID размера")
    product_id: int = Field(..., description="ID продукта")

    class Config:
        from_attributes = True
