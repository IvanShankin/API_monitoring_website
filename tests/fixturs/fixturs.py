from typing import AsyncGenerator, Callable

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import create_config, Config
from src.core.database.database import get_db
from src.models.api.app import init_fastapi_app
from src.models.depends import get_config


@pytest_asyncio.fixture(scope="session", autouse=True)
async def lifespan_for_tests(app_fastapi: FastAPI, config_fix: Config, crypto_context_fix: CryptContext ) -> AsyncGenerator[FastAPI, None]:
    app_fastapi.state.config = config_fix
    app_fastapi.state.cr_context = crypto_context_fix


@pytest_asyncio.fixture(scope="session")
async def app_fastapi() -> AsyncGenerator[FastAPI, None]:
    yield init_fastapi_app()


@pytest_asyncio.fixture(scope="session")
async def config_fix() -> AsyncGenerator[Config, None]:
    yield create_config()


@pytest_asyncio.fixture(scope="session")
async def crypto_context_fix() -> AsyncGenerator[CryptContext, None]:
    yield CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )


@pytest_asyncio.fixture(scope="function")
async def session_db(config_fix: Config):
    engine = create_async_engine(config_fix.db_connection.sql_db_url)

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def not_open_session_db(config_fix: Config) -> sessionmaker:
    engine = create_async_engine(config_fix.db_connection.sql_db_url)

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

    return async_session


@pytest_asyncio.fixture
async def client_with_db(session_db, app_fastapi: FastAPI, config_fix: Config):  # session_db открываем заранее
    # переопределяем Depends(get_db) на уже открытую сессию
    app_fastapi.dependency_overrides[get_db] = lambda: session_db
    app_fastapi.dependency_overrides[get_config] = lambda: config_fix

    async with AsyncClient(transport=ASGITransport(app_fastapi), base_url="http://test") as ac:
        yield ac
