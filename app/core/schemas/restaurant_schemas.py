import uuid as uuid_pkg
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RestaurantBase(BaseModel):
    name: str = Field(..., max_length=150, description="Название ресторана")
    description: Optional[str] = Field(None, description="Описание ресторана")
    address: Optional[str] = Field(None, max_length=200, description="Адрес ресторана")
    is_active: bool = Field(default=True, description="Статус активности ресторана")


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int = Field(..., description="ID ресторана")
    uuid: uuid_pkg = Field(..., description="UUID ресторана")
    created_at: datetime = Field(..., description="Дата создания")

    class Config:
        from_attributes = True
