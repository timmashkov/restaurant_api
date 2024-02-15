from http import HTTPStatus
from typing import Any

from api.v1.dishes.views import (
    create_dish,
    delete_dish,
    get_dish,
    show_dishes,
    update_dish,
)
from api.v1.menu.views import create_menu, delete_menu
from api.v1.submenu.views import create_submenu, delete_submenu
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


async def test_post_dish(
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

    saved_data['dish'] = response.json()


async def test_post_dish_double(
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
    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_dish_not_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse(show_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() != []


async def test_get_posted_dish(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(
            get_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']
        ),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == dish['id']
    assert response.json()['title'] == dish['title']
    assert response.json()['description'] == dish['description']
    assert response.json()['price'] == dish['price']


async def test_patch_dish(
    dish_patch: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.patch(
        reverse(
            update_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
        json=dish_patch,
    )
    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert 'price' in response.json()
    assert response.json()['title'] == dish_patch['title']
    assert response.json()['description'] == dish_patch['description']
    assert response.json()['price'] == dish_patch['price']

    saved_data['dish'] = response.json()


async def test_get_patched_dish(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(
            get_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']
        ),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == dish['id']
    assert response.json()['title'] == dish['title']
    assert response.json()['description'] == dish['description']
    assert response.json()['price'] == dish['price']


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


async def test_dish_empty_after_delete(
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


async def test_get_deleted_dish(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(
            get_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']
        ),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


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


async def test_deleted_submenu_dish_empty(
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


async def test_post_objects_for_cascade_check(
    submenu_post: dict[str, str],
    dish_post: dict[str, str],
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

    submenu = saved_data['submenu']
    response = await client.post(
        reverse(create_dish, menu_id=menu['id'], submenu_id=submenu['id']),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED

    saved_data['dish'] = response.json()


async def test_delete_submenu_for_cascade_check(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.delete(
        reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK


async def test_get_deleted_dish_cascade_check(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse(
            get_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']
        ),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'dish not found'


async def test_delete_menu_finally(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    menu = saved_data['menu']
    response = await client.delete(
        reverse(delete_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK
