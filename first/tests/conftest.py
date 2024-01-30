import pytest

from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session

from config import settings
from database import get_async_session, Base
from main import app
from httpx import AsyncClient

from models import *
from orm import AsyncORM

TEST_DATABASE_URL = settings.TEST_DB_URL

engine_test = create_async_engine(url=TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def create_test_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def example_database():
    async with async_session_maker.begin() as session:
        menu = Menu(
            title='Test Menu 1',
            description='Test Menu Description 1'
        )
        session.add(menu)
        await session.commit()

    async with async_session_maker.begin() as session:
        submenu = Submenu(
            title='Test Submenu 1',
            description='Test Submenu Description 1',
            menu_id=menu.id
        )
        session.add(submenu)
        await session.commit()

    async with async_session_maker.begin() as session:
        dish1 = Dish(
            title='Test dish 1',
            description='Test dish description 1',
            price=14.50,
            submenu_id=submenu.id
        )
        session.add(dish1)
        await session.commit()

    return menu, submenu, dish1


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
