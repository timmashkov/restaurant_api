from typing import Any
from uuid import UUID

from api.v1.submenu.schemas import SubMenuIn, SubMenuOut
from api.v1.submenu.service import SubMenuService
from fastapi import APIRouter, BackgroundTasks, Depends, status
from settings.config import SUBMENU_LINK, SUBMENUS_LINK
from settings.database import vortex
from settings.models import SubMenu
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    SUBMENUS_LINK,
    status_code=status.HTTP_201_CREATED,
    response_model=SubMenuOut,
    description='Создать подменю',
    summary='Создать подменю',
    responses={400: {'description': 'Такое подменю уже есть'}},
)
async def create_submenu(
    menu_id: UUID,
    menu_in: SubMenuIn,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    submenu_repo: SubMenuService = Depends(),
) -> SubMenuOut | dict[str, Any]:
    """
    Эндпоинт создания записи в таблице SubMenu
    :param background_task:
    :param submenu_repo:
    :param menu_id:
    :param menu_in:
    :param session:
    """
    return await submenu_repo.add_submenu_service(
        data=menu_in, session=session, menu_id=menu_id, background_task=background_task
    )


@router.get(
    SUBMENU_LINK,
    description='Показать подменю',
    response_model=SubMenuOut,
    summary='Показать подменю',
    responses={404: {'description': 'submenu not found'}},
)
async def get_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    submenu_repo: SubMenuService = Depends(),
) -> dict | None:
    """
    Эндпоинт получения записи из таблицы SubMenu
    :param background_task:
    :param menu_id:
    :param submenu_id:
    :param session:
    :param submenu_repo:
    """
    return await submenu_repo.get_submenu_service(
        title=submenu_id,
        session=session,
        menu_id=menu_id,
        background_task=background_task,
    )


@router.get(
    SUBMENUS_LINK,
    response_model=list[SubMenuOut],
    description='Список всех подменю',
    summary='Показать подменю',
    responses={404: {'description': 'submenu not found'}},
)
async def show_submenus(
    menu_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    submenu_repo: SubMenuService = Depends(),
) -> list[SubMenu]:
    """
    Эндпоинт получения списка записей в таблице SubMenu
    :param background_task:
    :param menu_id:
    :param session:
    :param submenu_repo:
    """
    return await submenu_repo.get_all_submenus_service(
        session=session, menu_id=menu_id, background_task=background_task
    )


@router.patch(
    SUBMENU_LINK,
    response_model=SubMenuOut,
    description='Обновить подменю',
    summary='Обновить подменю',
    responses={404: {'description': 'submenu not found'}},
)
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    menu_in: SubMenuIn,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    submenu_repo: SubMenuService = Depends(),
) -> dict[str, Any]:
    """
    Эндпоинт изменения записи в таблице SubMenu
    :param background_task:
    :param menu_id:
    :param submenu_id:
    :param menu_in:
    :param session:
    :param submenu_repo:
    """
    return await submenu_repo.change_submenu_service(
        menu_id=menu_id,
        data=menu_in,
        session=session,
        submenu_id=submenu_id,
        background_task=background_task,
    )


@router.delete(
    SUBMENU_LINK,
    description='Удалить подменю',
    summary='Удалить подменю',
    responses={404: {'description': 'submenu not found'}},
)
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(vortex.scoped_session),
    submenu_repo: SubMenuService = Depends(),
) -> dict[str, str | bool]:
    """
    Эндпоинт удаления записи из таблицы SubMenu
    :param background_task:
    :param menu_id:
    :param submenu_id:
    :param session:
    :param submenu_repo:
    """
    return await submenu_repo.drop_submenu_service(
        submenu_id=submenu_id,
        session=session,
        menu_id=menu_id,
        background_task=background_task,
    )
