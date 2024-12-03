from typing import Optional

from pydantic import BaseModel, Field

from app.core.models.product_model import MeasurementType


class PortionBase(BaseModel):
    unit_type: MeasurementType = Field(
        ..., description="Единица измерения (штуки/граммы/миллилитры)"
    )
    size: float = Field(
        ..., gt=0, description="Значение размера (в граммах, мл. или шт.)"
    )
    price: float = Field(default=0.0, gt=0, description="Цена за порцию")
    is_available: bool = Field(default=True, description="Доступность размера")
    name: Optional[str] = Field(
        ..., min_length=2, max_length=150, description="Название порции"
    )


class PortionSizeCreate(PortionBase):
    pass


class PortionSizeUpdate(PortionBase):
    pass


class PortionSize(PortionBase):
    id: int = Field(..., description="ID размера")
    product_id: int = Field(..., description="ID продукта")

    class Config:
        from_attributes = True
