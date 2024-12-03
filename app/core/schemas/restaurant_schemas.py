from uuid import UUID
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from pydantic import BaseModel, Field, ConfigDict


from app.core.schemas.product_schemas import Product


class RestaurantBase(BaseModel):
    name: str = Field(..., max_length=150, description="Название ресторана")
    description: Optional[str] = Field(None, description="Описание ресторана")
    address: Optional[str] = Field(None, max_length=200, description="Адрес ресторана")
    is_active: bool = Field(default=True, description="Статус активности ресторана")
    phone: Optional[str] = Field(
        max_length=20, min_length=5, description="Номер телефона"
    )
    image_url: Optional[str] = Field(
        description="URL изображения продукта", default=None
    )  # URL изображения
    # products: List["Product"] = Field(..., description="Список продуктов")


class RestaurantCreate(RestaurantBase):
    owner_id: Optional[int] = Field(description="Идентификатор владельца ресторана")


class RestaurantUpdate(RestaurantBase):
    owner_id: Optional[int] = Field(description="Идентификатор владельца ресторана")


class Restaurant(RestaurantBase):
    id: int = Field(..., description="ID ресторана")
    uuid: UUID = Field(..., description="UUID ресторана")
    created_at: datetime = Field(..., description="Дата создания")
    products: List["Product"] = Field(..., description="Список продуктов")
    slug: str = Field(..., description="Слаг ресторана")
    model_config = ConfigDict(arbitrary_types_allowed=True)
