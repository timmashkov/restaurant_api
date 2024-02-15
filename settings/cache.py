import pickle
from uuid import UUID

from settings.config import (
    DISH_LINK,
    DISHES_LINK,
    EXPIRATION,
    MENU_LINK,
    MENUS_LINK,
    SUBMENU_LINK,
    SUBMENUS_LINK,
)
from settings.models import Dish, Menu, SubMenu
from utils.utils import redis_connector


class RedisCache:
    def __init__(self) -> None:
        self.cache_maker = redis_connector()

    async def delete_cache(
        self,
        pattern: str,
    ) -> None:
        for key in await self.cache_maker.keys(pattern + '*'):
            await self.cache_maker.delete(key)

    async def set_all_dishes_cache(
        self,
        menu_id: str,
        submenu_id: str,
        items: list[Dish],
    ) -> None:
        await self.cache_maker.set(
            DISHES_LINK.format(menu_id=menu_id, submenu_id=submenu_id),
            pickle.dumps(items),
            ex=EXPIRATION,
        )

    async def get_all_dishes_cache(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> list[Dish] | None:
        cache = await self.cache_maker.get(
            DISHES_LINK.format(menu_id=menu_id, submenu_id=submenu_id),
        )
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_dish_cache(
        self,
        item: dict,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        await self.cache_maker.set(
            DISH_LINK.format(
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=item['id'],
            ),
            pickle.dumps(item),
            ex=EXPIRATION,
        )

    async def get_dish_cache(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> Dish | None:
        cache = await self.cache_maker.get(
            DISH_LINK.format(
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id,
            ),
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_dish_cache(
        self,
        item: dict,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        await self.delete_cache(MENU_LINK.format(menu_id=menu_id))
        await self.delete_all_menu_cache()
        await self.set_dish_cache(
            item=item,
            submenu_id=submenu_id,
            menu_id=menu_id,
        )

    async def update_dish_cache(
        self,
        item: dict,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        await self.delete_all_dish_cache(submenu_id, menu_id)
        await self.delete_full_base_cache()
        await self.set_dish_cache(
            item=item,
            submenu_id=submenu_id,
            menu_id=menu_id,
        )

    async def delete_dish_cache(self, menu_id: UUID) -> None:
        await self.delete_cache(MENU_LINK.format(menu_id=menu_id))
        await self.delete_all_menu_cache()

    async def delete_all_dish_cache(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        await self.cache_maker.delete(
            DISHES_LINK.format(menu_id=menu_id, submenu_id=submenu_id)
        )

    async def set_all_submenus_cache(
        self,
        menu_id: UUID,
        items: list[SubMenu],
    ) -> None:
        await self.cache_maker.set(
            SUBMENUS_LINK.format(menu_id=menu_id),
            pickle.dumps(items),
            ex=EXPIRATION,
        )

    async def get_all_submenus_cache(
        self,
        menu_id: UUID,
    ) -> list[SubMenu] | None:
        cache = await self.cache_maker.get(SUBMENUS_LINK.format(menu_id=menu_id))
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_submenu_cache(self, item: dict, menu_id: UUID) -> None:
        await self.cache_maker.set(
            SUBMENU_LINK.format(
                menu_id=menu_id,
                submenu_id=item['id'],
            ),
            pickle.dumps(item),
            ex=EXPIRATION,
        )

    async def get_submenu_cache(
        self, submenu_id: UUID, menu_id: UUID
    ) -> SubMenu | None:
        cache = await self.cache_maker.get(
            SUBMENU_LINK.format(menu_id=menu_id, submenu_id=submenu_id),
        )
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_submenu_cache(self, item: dict, menu_id: UUID) -> None:
        await self.delete_cache(
            MENU_LINK.format(menu_id=menu_id),
        )
        await self.delete_all_menu_cache()
        await self.set_submenu_cache(item, menu_id=menu_id)

    async def update_submenu_cache(self, item: dict, menu_id: UUID) -> None:
        await self.delete_all_submenu_cache(item['id'])
        await self.delete_full_base_cache()
        await self.set_submenu_cache(item, menu_id=menu_id)

    async def delete_submenu_cache(self, menu_id: UUID) -> None:
        await self.delete_cache(MENU_LINK.format(menu_id=menu_id))
        await self.delete_all_menu_cache()

    async def delete_all_submenu_cache(self, menu_id: UUID) -> None:
        await self.cache_maker.delete(SUBMENUS_LINK.format(menu_id=menu_id))

    async def set_all_menus_cache(self, items: list[Menu]) -> None:
        await self.cache_maker.set(
            MENUS_LINK,
            pickle.dumps(items),
            ex=EXPIRATION,
        )

    async def get_all_menus_cache(self) -> list[Menu] | None:
        cache = await self.cache_maker.get(MENUS_LINK)
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_full_base_menu_cache(self, items: list[Menu]) -> None:
        await self.cache_maker.set(
            'full_base_menu',
            pickle.dumps(items),
            ex=EXPIRATION,
        )

    async def get_full_base_menu_cache(self) -> list[Menu] | None:
        cache = await self.cache_maker.get('full_base_menu')
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    async def set_menu_cache(self, item: Menu) -> None:
        await self.cache_maker.set(
            MENU_LINK.format(menu_id=str(item.id)),
            pickle.dumps(item),
            ex=EXPIRATION,
        )

    async def get_menu_cache(self, menu_id: UUID) -> Menu | None:
        cache = await self.cache_maker.get(MENU_LINK.format(menu_id=menu_id))
        if cache:
            item = pickle.loads(cache)
            return item
        return None

    async def create_update_menu_cache(self, item: dict) -> None:
        await self.delete_all_menu_cache()
        await self.cache_maker.set(
            MENU_LINK.format(menu_id=item['id']),
            pickle.dumps(item),
            ex=EXPIRATION,
        )

    async def delete_all_menu_cache(self) -> None:
        await self.cache_maker.delete(MENUS_LINK)
        await self.delete_full_base_cache()

    async def delete_full_base_cache(self) -> None:
        await self.cache_maker.delete('full_base_menu')

    async def delete_menu_cache(self, menu_id: UUID) -> None:
        await self.delete_cache(
            MENU_LINK.format(menu_id=menu_id),
        )
        await self.delete_all_menu_cache()


redis_cache = RedisCache()
