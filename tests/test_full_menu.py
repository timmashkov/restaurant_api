from http import HTTPStatus
from typing import Any

from api.v1.dishes.views import create_dish, delete_dish
from api.v1.menu.views import create_menu, delete_menu, get_full_menu
from api.v1.submenu.views import delete_submenu, show_submenus
from httpx import AsyncClient
from tests.utils import reverse


async def test_all_menu_empty(client: AsyncClient) -> None:
    response = await client.get(
        reverse(get_full_menu),
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

    saved_data['menu'] = response.json()


async def test_post_submenu(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.post(
        reverse(
            show_submenus,
            menu_id=menu['id'],
        ),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED

    saved_data['submenu'] = response.json()


async def test_post_dish(
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse(
            create_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
        ),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED
    saved_data['dish'] = response.json()


async def test_full_base(
    menu_post: dict[str, str],
    submenu_post: dict[str, str],
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    response = await client.get(
        reverse(get_full_menu),
    )
    assert response.status_code == HTTPStatus.OK


async def test_delete_dish(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.delete(
        reverse(
            delete_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
    )
    assert response.status_code == HTTPStatus.OK


async def test_full_base_after_dish_delete(
    menu_post: dict[str, str],
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    response = await client.get(
        reverse(get_full_menu),
    )
    assert response.status_code == HTTPStatus.OK


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


async def test_full_base_after_submenu_delete(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    response = await client.get(
        reverse(get_full_menu),
    )
    assert response.status_code == HTTPStatus.OK


async def test_delete_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.delete(
        reverse(delete_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK


async def test_full_base_after_menu_delete(client: AsyncClient) -> None:
    response = await client.get(
        reverse(get_full_menu),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []
