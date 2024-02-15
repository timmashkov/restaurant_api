from uuid import UUID

from pydantic import BaseModel


class DishIn(BaseModel):
    """
    Входные данные блюд
    """

    title: str
    description: str | None = None
    price: str
    discount: int | None = None


class DishOut(DishIn):
    """
    Выходные данные блюд
    """

    id: UUID
