from typing import TYPE_CHECKING

from settings.models.base import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, Relationship, mapped_column

if TYPE_CHECKING:
    from .submenu import SubMenu


class Menu(Base):
    __tablename__ = 'menu'

    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    submenu_link: Mapped['SubMenu'] = Relationship(
        'SubMenu',
        back_populates='menu_link',
        cascade='all, delete-orphan',
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
