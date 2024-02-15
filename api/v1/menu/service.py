from typing import Any
from uuid import UUID

from api.v1.menu.crud import (
    add_menu,
    all_menu_data,
    change_menu,
    drop_menu,
    get_all_menus,
    show_menu,
)
from api.v1.menu.schemas import MenuIn
from asyncpg import UniqueViolationError
from fastapi import BackgroundTasks
from settings.cache import redis_cache
from settings.models import Menu
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from utils.exceptions import MenuAlreadyExists, MenuNotFound
from utils.utils import data_finder


class MenuService:
    def __init__(self) -> None:
        self.cacher = redis_cache

    async def create_menu_service(
        self, session: AsyncSession, data: MenuIn, background_task: BackgroundTasks
    ) -> dict[str, Any]:
        try:
            answer = await add_menu(data=data, session=session)
            await self.cacher.create_update_menu_cache(answer)
            background_task.add_task(self.cacher.create_update_menu_cache, answer)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise MenuAlreadyExists

    async def get_menu_service(
        self, title: UUID, session: AsyncSession, background_task: BackgroundTasks
    ) -> Menu | None:
        cache = await self.cacher.get_menu_cache(menu_id=title)
        if cache:
            return cache
        answer = await show_menu(title=title, session=session)
        if not answer:
            raise MenuNotFound
        background_task.add_task(self.cacher.get_menu_cache, title)
        return answer

    async def get_all_menu_service(
        self, session: AsyncSession, background_task: BackgroundTasks
    ) -> list[Menu]:
        cache = await self.cacher.get_all_menus_cache()
        if cache:
            return cache
        answer = await get_all_menus(session=session)
        background_task.add_task(self.cacher.get_all_menus_cache)
        return answer

    async def change_menu_service(
        self,
        menu_id: UUID,
        data: MenuIn,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> dict[str, Any]:
        if await data_finder(table=Menu, table_id=menu_id, session=session):
            answer = await change_menu(menu_id=menu_id, data=data, session=session)
            await self.cacher.create_update_menu_cache(answer)
            background_task.add_task(self.cacher.create_update_menu_cache, answer)
            return answer
        raise MenuNotFound

    async def drop_menu_service(
        self, menu_id: UUID, session: AsyncSession, background_task: BackgroundTasks
    ) -> dict[str, str | bool]:
        if await data_finder(table=Menu, table_id=menu_id, session=session):
            answer = await drop_menu(menu_id=menu_id, session=session)
            await self.cacher.delete_menu_cache(menu_id=menu_id)
            background_task.add_task(self.cacher.delete_menu_cache, menu_id)
            return answer
        raise MenuNotFound

    async def get_full_service(
        self, session: AsyncSession, background_task: BackgroundTasks
    ) -> list[Menu]:
        cache = await self.cacher.get_full_base_menu_cache()
        if cache:
            return cache
        answer = await all_menu_data(session=session)
        background_task.add_task(self.cacher.get_full_base_menu_cache)
        return answer
