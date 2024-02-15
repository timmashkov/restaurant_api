from typing import Any
from uuid import UUID

from api.v1.dishes.crud import add_dish, change_dish, drop_dish, get_all_dish, show_dish
from api.v1.dishes.schemas import DishIn, DishOut
from asyncpg import UniqueViolationError
from fastapi import BackgroundTasks
from settings.cache import redis_cache
from settings.models import Dish, Menu, SubMenu
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from utils.exceptions import (
    DishAlreadyExists,
    DishNotFound,
    MenuNotFound,
    SubMenuNotFound,
)
from utils.utils import data_finder


class DishService:
    def __init__(self) -> None:
        self.cacher = redis_cache

    async def create_dish_service(
        self,
        menu_id: UUID,
        data: DishIn,
        session: AsyncSession,
        submenu_id: UUID,
        background_task: BackgroundTasks,
    ) -> dict[str, Any]:
        if await data_finder(table=Menu, table_id=menu_id, session=session):
            if await data_finder(table=SubMenu, table_id=submenu_id, session=session):
                try:
                    answer = await add_dish(
                        data=data, submenu_id=submenu_id, session=session
                    )
                    await self.cacher.create_dish_cache(
                        menu_id=menu_id, submenu_id=submenu_id, item=answer
                    )
                    background_task.add_task(
                        self.cacher.create_dish_cache, answer, menu_id, submenu_id
                    )
                    return answer
                except (UniqueViolationError, IntegrityError):
                    raise DishAlreadyExists
            raise SubMenuNotFound
        raise MenuNotFound

    async def get_dish_service(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        title: UUID,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> DishOut | None:
        answer = await show_dish(title=title, session=session)
        if not answer:
            raise DishNotFound
        await self.cacher.get_dish_cache(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=title
        )
        background_task.add_task(
            self.cacher.get_dish_cache, answer, submenu_id, menu_id
        )
        return answer

    async def get_all_dish_service(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> list[Dish]:
        answer = await get_all_dish(session=session)
        await self.cacher.get_all_dishes_cache(menu_id=menu_id, submenu_id=submenu_id)
        background_task.add_task(self.cacher.get_all_dishes_cache, answer, submenu_id)
        return answer

    async def change_dish_service(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        data: DishIn,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> dict[str, Any]:
        if await data_finder(table=Dish, table_id=dish_id, session=session):
            answer = await change_dish(dish_id=dish_id, data=data, session=session)
            await self.cacher.update_dish_cache(
                menu_id=menu_id, submenu_id=submenu_id, item=answer
            )
            background_task.add_task(
                self.cacher.update_dish_cache, answer, submenu_id, menu_id
            )
            return answer
        raise DishNotFound

    async def drop_dish_service(
        self,
        menu_id: UUID,
        dish_id: UUID,
        session: AsyncSession,
        background_task: BackgroundTasks,
    ) -> dict[str, str | bool]:
        if await data_finder(table=Dish, table_id=dish_id, session=session):
            answer = await drop_dish(dish_id=dish_id, session=session)
            await self.cacher.delete_dish_cache(menu_id=menu_id)
            background_task.add_task(self.cacher.delete_dish_cache, answer)
            return answer
        raise DishNotFound
