from fastapi import APIRouter
from .menu.views import router as menu_router
from .submenu.views import router as submenu_router
from .dishes.views import router as dish_router

router = APIRouter(prefix='/v1')

router.include_router(router=menu_router)
router.include_router(router=submenu_router)
router.include_router(router=dish_router)
