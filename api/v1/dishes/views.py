from typing import Any
from uuid import UUID

from api.v1.dishes.schemas import DishIn, DishOut
from api.v1.dishes.service import DishService
from fastapi import APIRouter, BackgroundTasks, Depends, status
from settings.config import DISH_LINK, DISHES_LINK
from settings.database import vortex
from settings.models import Dish
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    DISHES_LINK,
    status_code=status.HTTP_201_CREATED,
    response_model=DishOut,
    description='Создать блюдо',
    summary='Создать блюдо',
    responses={
        404: {'description': 'submenu not found'},
        400: {'description': 'Такое блюдо уже есть'},
    },
)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_in: DishIn,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    dish_repo: DishService = Depends(),
) -> DishOut | dict[str, Any]:
    """
    Эндпоинт создания записи в таблице Dish
    :param background_task:
    :param menu_id:
    :param submenu_id:
    :param dish_in:
    :param session:
    :param dish_repo:
    """
    return await dish_repo.create_dish_service(
        submenu_id=submenu_id,
        data=dish_in,
        session=session,
        menu_id=menu_id,
        background_task=background_task,
    )


@router.get(
    DISH_LINK,
    response_model=DishOut,
    description='Показать блюдо',
    summary='Показать блюдо',
    responses={404: {'description': 'dish not found'}},
)
async def get_dish(
    menu_id: UUID,
    submenu_id,
    dish_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    dish_repo: DishService = Depends(),
) -> DishOut | None:
    """
    Эндпоинт получения записи из таблицы Dish
    :param background_task:
    :param menu_id:
    :param submenu_id:
    :param dish_id:
    :param session:
    :param dish_repo:
    """
    return await dish_repo.get_dish_service(
        title=dish_id,
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_task=background_task,
    )


@router.get(
    DISHES_LINK,
    response_model=list[DishOut],
    description='Список всех блюд',
    summary='Список всех блюд',
    responses={404: {'description': 'dish not found'}},
)
async def show_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    dish_repo: DishService = Depends(),
) -> list[Dish]:
    """
    Эндпоинт получения списка записей в таблице Dish
    :param background_task:
    :param menu_id:
    :param submenu_id:
    :param session:
    :param dish_repo:
    """
    return await dish_repo.get_all_dish_service(
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_task=background_task,
    )


@router.patch(
    DISH_LINK,
    response_model=DishOut,
    description='Обновить блюдо',
    summary='Обновить блюдо',
    responses={404: {'description': 'dish not found'}},
)
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_in: DishIn,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    dish_repo: DishService = Depends(),
) -> DishOut | dict[str, Any]:
    """
    Эндпоинт изменения записи в таблице Dish
    :param background_task:
    :param menu_id:
    :param submenu_id:
    :param dish_id:
    :param dish_in:
    :param session:
    :param dish_repo:
    """
    return await dish_repo.change_dish_service(
        dish_id=dish_id,
        data=dish_in,
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
        background_task=background_task,
    )


@router.delete(
    DISH_LINK,
    description='Удалить блюдо',
    summary='Удалить блюдо',
    responses={404: {'description': 'dish not found'}},
)
async def delete_dish(
    menu_id: UUID,
    dish_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    dish_repo: DishService = Depends(),
) -> dict[str, str | bool]:
    """
    Эндпоинт удаления записи из таблицы Dish
    :param background_task:
    :param menu_id:
    :param dish_id:
    :param session:
    :param dish_repo
    """
    return await dish_repo.drop_dish_service(
        dish_id=dish_id,
        session=session,
        menu_id=menu_id,
        background_task=background_task,
    )
