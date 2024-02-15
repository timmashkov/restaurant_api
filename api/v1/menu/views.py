from typing import Any
from uuid import UUID

from api.v1.menu.schemas import MenuIn, MenuOut
from api.v1.menu.service import MenuService
from fastapi import APIRouter, BackgroundTasks, Depends, status
from settings.config import MENU_LINK, MENUS_LINK
from settings.database import vortex
from settings.models import Menu
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    MENUS_LINK,
    status_code=status.HTTP_201_CREATED,
    name='create_menu',
    response_model=MenuOut,
    description='Создать меню',
    summary='Создать меню',
    responses={400: {'description': 'Такое меню уже есть'}},
)
async def create_menu(
    menu_in: MenuIn,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    menu_repo: MenuService = Depends(),
) -> MenuOut | dict[str, Any]:
    """
    Эндпоинт создания записи в таблице Menu
    :param background_task:
    :param menu_in:
    :param session:
    :param menu_repo:
    """
    return await menu_repo.create_menu_service(
        data=menu_in, session=session, background_task=background_task
    )


@router.get(
    MENU_LINK,
    response_model=MenuOut,
    description='Показать меню',
    summary='Показать меню',
    responses={404: {'description': 'menu not found'}},
)
async def get_menu(
    menu_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    menu_repo: MenuService = Depends(),
) -> Menu | None:
    """
    Эндпоинт получения записи из таблицы Menu
    :param background_task:
    :param menu_id:
    :param session:
    :param menu_repo:
    """
    return await menu_repo.get_menu_service(
        title=menu_id, session=session, background_task=background_task
    )


@router.get(
    MENUS_LINK,
    name='show_menus',
    response_model=list[MenuOut],
    description='Список всех меню',
    summary='Список всех меню',
    responses={404: {'description': 'menu not found'}},
)
async def show_menus(
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    menu_repo: MenuService = Depends(),
) -> list[Menu]:
    """
    Эндпоинт получения списка записей в таблице Menu
    :param background_task:
    :param session:
    :param menu_repo:
    """
    return await menu_repo.get_all_menu_service(
        session=session, background_task=background_task
    )


@router.patch(
    MENU_LINK,
    response_model=MenuOut,
    description='Обновить меню',
    summary='Обновить меню',
    responses={404: {'description': 'menu not found'}},
)
async def update_menu(
    menu_id: UUID,
    menu_in: MenuIn,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    menu_repo: MenuService = Depends(),
) -> MenuOut | dict[str, Any]:
    """
    Эндпоинт изменения записи в таблице Menu
    :param background_task:
    :param menu_id:
    :param menu_in:
    :param session:
    :param menu_repo
    """
    return await menu_repo.change_menu_service(
        menu_id=menu_id, data=menu_in, session=session, background_task=background_task
    )


@router.delete(
    MENU_LINK,
    description='Удалить меню',
    summary='Удалить меню',
    responses={404: {'description': 'menu not found'}},
)
async def delete_menu(
    menu_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    menu_repo: MenuService = Depends(),
) -> dict[str, str | bool]:
    """
    Эндпоинт удаления записи из таблицы Menu
    :param background_task:
    :param menu_id:
    :param session:
    :param menu_repo:
    """
    return await menu_repo.drop_menu_service(
        menu_id=menu_id, session=session, background_task=background_task
    )


@router.get(
    '/all_base',
    status_code=200,
    response_model=None,
    summary='Получить все данные',
    responses={404: {'description': 'menu not found'}},
)
async def get_full_menu(
    background_task: BackgroundTasks,
    menu_repo: MenuService = Depends(),
    session: AsyncSession = Depends(vortex.scoped_session),
) -> list[Menu]:
    """
    Эндпоинт получения всех данных
    :param background_task:
    :param menu_repo:
    :param session:
    :return:
    """
    return await menu_repo.get_full_service(
        session=session, background_task=background_task
    )
