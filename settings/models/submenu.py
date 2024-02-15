from typing import TYPE_CHECKING
from uuid import UUID

from settings.models.base import Base
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, Relationship, mapped_column

if TYPE_CHECKING:
    from .dish import Dish
    from .menu import Menu


class SubMenu(Base):
    __tablename__ = 'submenu'

    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    menu_id: Mapped[UUID] = mapped_column(
        ForeignKey('menu.id', ondelete='CASCADE'), unique=True, nullable=True
    )
    menu_link: Mapped['Menu'] = Relationship(
        'Menu',
        back_populates='submenu_link',
    )

    dishes: Mapped['Dish'] = Relationship(
        'Dish',
        back_populates='position',
        cascade='all, delete-orphan',
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
