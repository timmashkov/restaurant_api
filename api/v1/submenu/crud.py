from typing import Any
from uuid import UUID

from api.v1.submenu.schemas import SubMenuIn
from settings.models import SubMenu
from sqlalchemy import Result, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from utils.utils import dishes_count


async def add_submenu(
    session: AsyncSession, data: SubMenuIn, menu_id: UUID
) -> dict[str, Any]:
    """
    Функция добавления записи в таблицу SubMenu
    :param session:
    :param data:
    :param menu_id:
    :return: answer
    """
    stmt = (
        insert(SubMenu).values(
            title=data.title, description=data.description, menu_id=menu_id
        )
    ).returning(SubMenu.id, SubMenu.title, SubMenu.description)
    result = await session.execute(stmt)
    answer = result.first()._asdict()
    await session.commit()
    dishes = {
        'dishes_count': await dishes_count(submenu_id=answer['id'], session=session)
    }
    answer.update(dishes)
    return answer


async def show_submenu(title: UUID, session: AsyncSession) -> dict | None:
    """
    Функция возвращает конкретное подменю
    :param title:
    :param session:
    :return: data
    """
    stmt = select(SubMenu).where(SubMenu.id == title)
    result: Result = await session.execute(stmt)
    answer: SubMenu | None = result.scalar_one_or_none()
    if answer:
        data = {
            'id': answer.id,
            'title': answer.title,
            'description': answer.description,
            'menu_id': answer.menu_id,
            'dishes_count': await dishes_count(submenu_id=answer.id, session=session),
        }
        return data
    return None


async def get_all_submenus(session: AsyncSession) -> list[SubMenu]:
    """
    Функция возвращает список подменю
    :param session:
    :return: list(answer)
    """
    stmt = select(SubMenu).order_by(SubMenu.id)
    result = await session.execute(stmt)
    answer = result.scalars().all()
    return list(answer)


async def change_submenu(
    menu_id: UUID, submenu_id: UUID, data: SubMenuIn, session: AsyncSession
) -> dict[str, Any]:
    """
    Функция внесения изменения в запись таблицы SubMenu
    :param menu_id:
    :param submenu_id:
    :param data:
    :param session:
    :return: answer
    """
    stmt = (
        update(SubMenu)
        .where(SubMenu.id == submenu_id)
        .values(title=data.title, description=data.description, menu_id=menu_id)
        .returning(SubMenu.id, SubMenu.title, SubMenu.description, SubMenu.menu_id)
    )
    result = await session.execute(stmt)
    answer = result.first()._asdict()
    await session.commit()
    dishes = {
        'dishes_count': await dishes_count(submenu_id=answer['id'], session=session)
    }
    answer.update(dishes)
    return answer


async def drop_submenu(
    submenu_id: UUID, session: AsyncSession
) -> dict[str, str | bool]:
    """
    Функция удаления записи из таблицы SubMenu
    :param submenu_id:
    :param session:
    :return: dict
    """
    stmt = (
        delete(SubMenu)
        .where(SubMenu.id == submenu_id)
        .returning(SubMenu.id, SubMenu.title, SubMenu.description, SubMenu.menu_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {'status': True, 'message': 'The submenu has been deleted'}
