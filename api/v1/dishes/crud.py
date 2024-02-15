from typing import Any
from uuid import UUID

from api.v1.dishes.schemas import DishIn, DishOut
from settings.models import Dish
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def add_dish(
    data: DishIn, session: AsyncSession, submenu_id: UUID
) -> dict[str, Any]:
    """
    Функция добавления записи в таблицу Dish
    :param data:
    :param session:
    :param submenu_id:
    :return: answer
    """
    stmt = (
        insert(Dish)
        .values(
            title=data.title,
            description=data.description,
            price=data.price,
            submenu_id=submenu_id,
            discount=data.discount,
        )
        .returning(
            Dish.id,
            Dish.title,
            Dish.description,
            Dish.price,
            Dish.submenu_id,
            Dish.discount,
        )
    )
    result = await session.execute(stmt)
    answer = result.first()._asdict()
    await session.commit()
    return answer


async def show_dish(title: UUID, session: AsyncSession) -> DishOut | None:
    """
    Функция возвращает конкретное блюдо
    :param title:
    :param session:
    :return: data
    """
    stmt = select(Dish).where(Dish.id == title)
    result = await session.execute(stmt)
    answer: DishOut | None = result.scalar_one_or_none()
    return answer


async def get_all_dish(session: AsyncSession) -> list[Dish]:
    """
    Функция возвращает список блюд
    :param session:
    :return: list(answer)
    """
    stmt = select(Dish).order_by(Dish.id)
    result = await session.execute(stmt)
    answer = result.scalars().all()
    return list(answer)


async def change_dish(
    dish_id: UUID, data: DishIn, session: AsyncSession
) -> dict[str, Any]:
    """
    Функция внесения изменения в запись таблицы Dish
    :param dish_id:
    :param data:
    :param session:
    :return: answer
    """
    stmt = (
        update(Dish)
        .where(Dish.id == dish_id)
        .values(
            title=data.title,
            description=data.description,
            price=data.price,
            discount=data.discount,
        )
        .returning(
            Dish.id,
            Dish.title,
            Dish.description,
            Dish.price,
            Dish.submenu_id,
            Dish.discount,
        )
    )
    result = await session.execute(stmt)
    answer = result.first()._asdict()
    await session.commit()
    return answer


async def drop_dish(dish_id: UUID, session: AsyncSession) -> dict[str, str | bool]:
    """
    Функция удаления записи из таблицы Dish
    :param dish_id:
    :param session:
    :return: dict
    """
    stmt = (
        delete(Dish)
        .where(Dish.id == dish_id)
        .returning(Dish.id, Dish.title, Dish.description, Dish.price, Dish.discount)
    )
    await session.execute(stmt)
    await session.commit()
    return {'status': True, 'message': 'The menu has been deleted'}
