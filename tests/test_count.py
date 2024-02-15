from http import HTTPStatus
from typing import Any

from api.v1.dishes.views import create_dish, show_dishes
from api.v1.menu.views import create_menu, delete_menu, get_menu, show_menus
from api.v1.submenu.views import (
    create_submenu,
    delete_submenu,
    get_submenu,
    show_submenus,
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


async def test_post_first_dish(
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse(create_dish, menu_id=menu['id'], submenu_id=submenu['id']),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'price' in response.json()
    assert response.json()['title'] == dish_post['title']
    assert response.json()['description'] == dish_post['description']
    assert response.json()['price'] == dish_post['price']

    saved_data['dish_1'] = response.json()


async def test_post_second_dish(
    dish_2_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse(create_dish, menu_id=menu['id'], submenu_id=submenu['id']),
        json=dish_2_post,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'price' in response.json()
    assert response.json()['title'] == dish_2_post['title']
    assert response.json()['description'] == dish_2_post['description']
    assert response.json()['price'] == dish_2_post['price']

    saved_data['dish_2'] = response.json()


async def test_current_menu(
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
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2


async def test_get_current_submenu(
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
    assert response.json()['dishes_count'] == 2


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


async def test_dish_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(show_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


async def test_current_menu_empty(
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


async def test_all_menu_empty(client: AsyncClient) -> None:
    response = await client.get(
        reverse(show_menus),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []
