from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100, description="Название категории")
    description: Optional[str] = Field(None, description="Описание категории")
    parent_id: Optional[int] = Field(None, description="ID родительской категории")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass
