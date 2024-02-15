import os

from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv('.env')
else:
    load_dotenv('.env_prod')

PREFIX_LINK = 'http://main_app:8000/api/v1'
MENUS_LINK = '/menus'
MENU_LINK = '/menus/{menu_id}'
SUBMENUS_LINK = '/menus/{menu_id}/submenus'
SUBMENU_LINK = '/menus/{menu_id}/submenus/{submenu_id}'
DISHES_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes'
DISH_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
MENU_FILE_LINK = '/food_app/admin/Menu.xlsx'

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
db_url = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')

CELERY_STATUS = os.environ.get('CELERY_STATUS')

EXPIRATION = 3600

DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')
DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
test_db_url = (
    f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:'
    f'{DB_PORT_TEST}/{DB_NAME_TEST}'
)
