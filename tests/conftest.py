import asyncio
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from runner import app
from settings.database import vortex
from settings.models import Base
from settings.test_database import test_database
from sqlalchemy.ext.asyncio import AsyncSession

Base.metadata.bind = test_database.test_engine


async def override_scoped_session() -> AsyncGenerator[AsyncSession, None]:
    session = test_database.test_session_maker()
    async with session as sess:
        yield sess


app.dependency_overrides[vortex.scoped_session] = override_scoped_session


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_database.test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_database.test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
async def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture
def menu_post() -> dict[str, str]:
    return {'title': 'First menu', 'description': 'Some description'}


@pytest_asyncio.fixture
def menu_patch() -> dict[str, str]:
    return {'title': 'First menu updated', 'description': 'Some description updated'}


@pytest_asyncio.fixture
def submenu_post() -> dict[str, str]:
    return {'title': 'First submenu', 'description': 'Some description'}


@pytest_asyncio.fixture
def submenu_patch() -> dict[str, str]:
    return {'title': 'First submenu updated', 'description': 'Some description updated'}


@pytest_asyncio.fixture
def dish_post() -> dict[str, str]:
    return {
        'title': 'First dish',
        'description': 'Some description',
        'price': '123.456',
    }


@pytest_asyncio.fixture
def dish_2_post() -> dict[str, str]:
    return {
        'title': 'Second dish',
        'description': 'Some another description',
        'price': '654.123',
    }


@pytest_asyncio.fixture
def dish_patch() -> dict[str, str]:
    return {
        'title': 'First dish updated',
        'description': 'Some description updated',
        'price': '654.123',
    }


@pytest_asyncio.fixture(scope='module')
def saved_data() -> dict[str, Any]:
    return {}
