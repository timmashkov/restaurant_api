from uuid import UUID

from pydantic import BaseModel


class SubMenuIn(BaseModel):
    """
    Входные данные подменю
    """

    title: str
    description: str | None = None


class SubMenuOut(SubMenuIn):
    """
    Выходные данные подменю
    """

    id: UUID
    dishes_count: int | None = 0
