from http import HTTPStatus
from typing import Any

from api.v1.menu.views import create_menu, delete_menu
from api.v1.submenu.views import (
    create_submenu,
    delete_submenu,
    get_submenu,
    show_submenus,
    update_submenu,
)
from httpx import AsyncClient
from tests.utils import reverse


async def test_post_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    response = await client.post(
        reverse(create_menu),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'submenus_count' in response.json()
    assert 'dishes_count' in response.json()

    saved_data['menu'] = response.json()


async def test_submenu_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.get(
        reverse(show_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


async def test_post_submenu(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.post(
        reverse(create_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED

    saved_data['submenu'] = response.json()


async def test_post_submenu_double(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.post(
        reverse(create_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_all_submenu_not_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.get(
        reverse(show_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() != []


async def test_get_posted_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == submenu['id']
    assert response.json()['title'] == submenu['title']
    assert response.json()['description'] == submenu['description']
    assert response.json()['dishes_count'] == 0


async def test_patch_submenu(
    submenu_patch: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.patch(
        reverse(update_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
        json=submenu_patch,
    )
    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'dishes_count' in response.json()
    assert response.json()['title'] == submenu_patch['title']
    assert response.json()['description'] == submenu_patch['description']

    saved_data['submenu'] = response.json()


async def test_get_patched_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == submenu['id']
    assert response.json()['title'] == submenu['title']
    assert response.json()['description'] == submenu['description']
    assert response.json()['dishes_count'] == 0


async def test_delete_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.delete(
        reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK


async def test_submenu_empty_after_delete(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.get(
        reverse(show_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_get_deleted_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'submenu not found'


async def test_delete_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.delete(
        reverse(delete_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK


async def test_deleted_menu_submenu_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.get(
        reverse(show_submenus, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


async def test_post_objects_for_cascade_check(
    menu_post: dict[str, str],
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    response = await client.post(
        reverse(create_menu),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED

    saved_data['menu'] = response.json()

    menu = saved_data['menu']
    response = await client.post(
        reverse(create_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED

    saved_data['submenu'] = response.json()


async def test_delete_menu_for_cascade_check(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.delete(
        reverse(delete_menu, menu_id=menu['id']),
    )
    assert response.status_code == 200


async def test_get_deleted_submenu_cascade_check(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
