from typing import Any
from uuid import UUID

from api.v1.submenu.crud import (
    add_submenu,
    change_submenu,
    drop_submenu,
    get_all_submenus,
    show_submenu,
)
from api.v1.submenu.schemas import SubMenuIn
from asyncpg import UniqueViolationError
from fastapi import BackgroundTasks
from settings.cache import redis_cache
from settings.models import Menu, SubMenu
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from utils.exceptions import MenuNotFound, SubMenuAlreadyExists, SubMenuNotFound
from utils.utils import data_finder


class SubMenuService:
    def __init__(self) -> None:
        self.cacher = redis_cache

    async def add_submenu_service(
        self,
        session: AsyncSession,
        data: SubMenuIn,
        menu_id: UUID,
        background_task: BackgroundTasks,
    ) -> dict[str, Any]:
        if await data_finder(table=Menu, table_id=menu_id, session=session):
            try:
                answer = await add_submenu(session=session, data=data, menu_id=menu_id)
                await self.cacher.create_submenu_cache(menu_id=menu_id, item=answer)
                background_task.add_task(
                    self.cacher.create_submenu_cache, answer, menu_id
                )
                return answer
            except (UniqueViolationError, IntegrityError):
                raise SubMenuAlreadyExists
        raise MenuNotFound

    async def get_submenu_service(
        self,
        menu_id: UUID,
        title: UUID,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> dict | None:
        answer = await show_submenu(title=title, session=session)
        if not answer:
            raise SubMenuNotFound
        await self.cacher.get_submenu_cache(menu_id=menu_id, submenu_id=title)
        background_task.add_task(self.cacher.get_submenu_cache, answer, menu_id)
        return answer

    async def get_all_submenus_service(
        self, menu_id: UUID, session: AsyncSession, background_task: BackgroundTasks
    ) -> list[SubMenu]:
        answer = await get_all_submenus(session=session)
        await self.cacher.get_all_submenus_cache(menu_id=menu_id)
        background_task.add_task(self.cacher.get_all_submenus_cache, answer)
        return answer

    async def change_submenu_service(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        data: SubMenuIn,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> dict[str, Any]:
        if await data_finder(table=SubMenu, table_id=submenu_id, session=session):
            answer = await change_submenu(
                menu_id=menu_id, submenu_id=submenu_id, data=data, session=session
            )
            await self.cacher.update_submenu_cache(answer, menu_id=menu_id)
            background_task.add_task(self.cacher.update_submenu_cache, answer, menu_id)
            return answer
        raise SubMenuNotFound

    async def drop_submenu_service(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> dict[str, str | bool]:
        if await data_finder(table=SubMenu, table_id=submenu_id, session=session):
            answer = await drop_submenu(submenu_id=submenu_id, session=session)
            await self.cacher.delete_submenu_cache(menu_id=menu_id)
            background_task.add_task(self.cacher.delete_submenu_cache, menu_id)
            return answer
        raise SubMenuNotFound
