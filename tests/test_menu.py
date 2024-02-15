from http import HTTPStatus
from typing import Any

from api.v1.menu.views import (
    create_menu,
    delete_menu,
    get_menu,
    show_menus,
    update_menu,
)
from httpx import AsyncClient
from tests.utils import reverse


async def test_all_menu_empty(client: AsyncClient) -> None:
    response = await client.get(
        reverse(show_menus),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


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
    assert response.json()['title'] == menu_post['title']
    assert response.json()['description'] == menu_post['description']

    saved_data['menu'] = response.json()


async def test_post_menu_double(
    menu_post: dict[str, str],
    client: AsyncClient,
) -> None:
    response = await client.post(
        reverse(create_menu),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_all_menu_not_empty(client: AsyncClient) -> None:
    response = await client.get(
        reverse(show_menus),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() != []


async def test_get_posted_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.get(
        reverse(get_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == menu['id']
    assert response.json()['title'] == menu['title']
    assert response.json()['description'] == menu['description']
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


async def test_patch_menu(
    menu_patch: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.patch(
        reverse(update_menu, menu_id=menu['id']),
        json=menu_patch,
    )
    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'submenus_count' in response.json()
    assert 'dishes_count' in response.json()
    assert response.json()['title'] == menu_patch['title']
    assert response.json()['description'] == menu_patch['description']

    saved_data['menu'] = response.json()


async def test_get_patched_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.get(
        reverse(get_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == menu['id']
    assert response.json()['title'] == menu['title']
    assert response.json()['description'] == menu['description']
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


async def test_delete_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.delete(
        reverse(delete_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK


async def test_get_deleted_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.get(
        reverse(get_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'menu not found'
