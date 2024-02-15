from uuid import UUID

from pydantic import BaseModel


class MenuIn(BaseModel):
    """
    Входные данные меню
    """

    title: str
    description: str | None = None


class MenuOut(MenuIn):
    """
    Выходные данные меню
    """

    id: UUID
    submenus_count: int | None = 0
    dishes_count: int | None = 0
