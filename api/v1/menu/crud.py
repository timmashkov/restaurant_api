from typing import Any
from uuid import UUID

from api.v1.menu.schemas import MenuIn
from settings.models import Dish, Menu, SubMenu
from sqlalchemy import Result, delete, distinct, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from utils.utils import dishes_count, submenu_count


async def add_menu(session: AsyncSession, data: MenuIn) -> dict[str, Any]:
    """
    Функция добавления записи в таблицу Menu
    :param session:
    :param data:
    :return: answer
    """
    stmt = (
        insert(Menu)
        .values(title=data.title, description=data.description)
        .returning(Menu.id, Menu.title, Menu.description)
    )
    result = await session.execute(stmt)
    answer = result.first()._asdict()
    await session.commit()
    submenus = {
        'submenus_count': await submenu_count(menu_id=answer['id'], session=session)
    }
    dishes = {
        'dishes_count': await dishes_count(submenu_id=answer['id'], session=session)
    }
    answer.update(submenus)
    answer.update(dishes)
    return answer


async def show_menu(title: UUID, session: AsyncSession) -> Menu | None:
    """
    Функция возвращает конкретное меню
    :param title:
    :param session:
    :return: data
    """
    stmt = (
        select(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(distinct(SubMenu.id)).label('submenus_count'),
            func.count(distinct(Dish.id)).label('dishes_count'),
        )
        .select_from(Menu)
        .outerjoin(SubMenu, Menu.id == SubMenu.menu_id)
        .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
        .where(Menu.id == title)
        .group_by(Menu.id)
    )
    result: Result = await session.execute(stmt)
    answer: Menu | None = result.one_or_none()
    return answer


async def get_all_menus(session: AsyncSession) -> list[Menu]:
    """
    Функция возвращает список подменю
    :param session:
    :return: list(answer)
    """
    stmt = select(Menu).order_by(Menu.id)
    result = await session.execute(stmt)
    answer = result.scalars().all()
    return list(answer)


async def change_menu(
    menu_id: UUID, data: MenuIn, session: AsyncSession
) -> dict[str, Any]:
    """
    Функция внесения изменения в запись таблицы Menu
    :param menu_id:
    :param data:
    :param session:
    :return: answer
    """
    stmt = (
        update(Menu)
        .where(Menu.id == menu_id)
        .values(title=data.title, description=data.description)
        .returning(Menu.id, Menu.title, Menu.description)
    )
    result = await session.execute(stmt)
    answer = result.first()._asdict()
    await session.commit()
    submenus = {
        'submenus_count': await submenu_count(menu_id=answer['id'], session=session)
    }
    dishes = {
        'dishes_count': await dishes_count(submenu_id=answer['id'], session=session)
    }
    answer.update(submenus)
    answer.update(dishes)
    return answer


async def drop_menu(menu_id: UUID, session: AsyncSession) -> dict[str, str | bool]:
    """
    Функция удаления записи из таблицы Menu
    :param menu_id:
    :param session:
    :return: dict
    """
    stmt = (
        delete(Menu)
        .where(Menu.id == menu_id)
        .returning(Menu.id, Menu.title, Menu.description)
    )
    await session.execute(stmt)
    await session.commit()
    return {'status': True, 'message': 'The menu has been deleted'}


async def all_menu_data(session: AsyncSession) -> list[Menu]:
    stmt = select(Menu).options(
        selectinload(Menu.submenu_link).selectinload(SubMenu.dishes)
    )
    result = await session.execute(stmt)
    answer = result.scalars().all()
    return list(answer)
