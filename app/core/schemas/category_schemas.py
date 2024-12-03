from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    """Базовая схема для категории"""

    name: str = Field(
        ..., min_length=2, max_length=100, description="Название категории"
    )
    description: Optional[str] = Field(None, description="Описание категории")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInit(CategoryBase):
    id: int = Field(..., description="ID категории")
    slug: str = Field(..., description="Слаг категории")

    class Config:
        """Класс конфигурации"""

        # Позволяет использовать поля модели
        from_attributes = True
