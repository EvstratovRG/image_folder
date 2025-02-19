from typing import AsyncGenerator

from .db import engine
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

pytest_plugins = ["tests.fixtures.users"]


@pytest.fixture(autouse=True)
def inject_db_session_into_middleware(async_session, mocker):
    mocker.patch("main.SessionLocal", side_effect=lambda: async_session)


@pytest_asyncio.fixture
async def async_client():
    from main import app
    from httpx import __version__

    if __version__ < "0.28.0":
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    else:
        from httpx import ASGITransport

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    connection = await engine.connect()
    await connection.begin()
    await connection.begin_nested()
    db_session = sessionmaker(
        bind=connection, class_=AsyncSession, expire_on_commit=False
    )
    async with db_session() as session:
        yield session
        await session.rollback()
    await connection.close()
    await engine.dispose()
