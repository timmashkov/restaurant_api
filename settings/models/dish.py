from typing import TYPE_CHECKING
from uuid import UUID

from settings.models.base import Base
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, Relationship, mapped_column

if TYPE_CHECKING:
    from .submenu import SubMenu


class Dish(Base):
    __tablename__ = 'dish'

    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[str] = mapped_column(String, nullable=False)
    discount: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    submenu_id: Mapped[UUID] = mapped_column(
        ForeignKey('submenu.id', ondelete='CASCADE'), unique=False, nullable=True
    )
    position: Mapped['SubMenu'] = Relationship(
        'SubMenu',
        back_populates='dishes',
    )
