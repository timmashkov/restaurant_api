from uuid import UUID

import aioredis
from aioredis import Redis
from settings.config import REDIS_HOST, REDIS_PORT
from settings.models import Dish, Menu, SubMenu
from sqlalchemy import Result, func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def submenu_count(menu_id: UUID, session: AsyncSession) -> int | Result:
    result = (
        select(func.count()).select_from(SubMenu).filter(SubMenu.menu_id == menu_id)
    )
    stmt = await session.execute(result)
    answer: Result | None = stmt.scalar_one_or_none()
    if answer:
        return answer
    return 0


async def dishes_count(submenu_id: UUID, session: AsyncSession) -> int:
    dish_id = select(Menu).where(Menu.id == submenu_id)
    total: Result = await session.execute(dish_id)
    final = total.scalar_one_or_none()
    if final:
        menu_id = final.id
        stmt = select(SubMenu.dishes).where(SubMenu.menu_id == menu_id)
        result = await session.execute(stmt)
        answer = result.all()
        return len(answer)
    stmt = select(SubMenu.dishes).where(SubMenu.id == submenu_id)
    result = await session.execute(stmt)
    answer = result.all()
    return len(answer)


async def data_finder(
    table: type[Menu] | type[SubMenu] | type[Dish],
    table_id: UUID,
    session: AsyncSession,
) -> Menu | None:
    stmt = select(table).where(table.id == table_id)
    result = await session.execute(stmt)
    answer = result.scalar_one_or_none()
    return answer


def redis_maker() -> aioredis.ConnectionPool:
    return aioredis.ConnectionPool.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')


redis_pool = redis_maker()


def redis_connector() -> Redis:
    return Redis(connection_pool=redis_pool)
