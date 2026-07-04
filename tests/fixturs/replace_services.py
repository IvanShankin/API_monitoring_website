import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from helpers import test_crypto_context
from src.models.users.repository import UsersRepository
from src.models.users.service import UsersService
from src.models.websites.repository import WebsiteRepository
from src.models.websites.service import WebsitesService


@pytest_asyncio.fixture(scope="function")
async def user_service_fixture(session_db: AsyncSession) -> UsersService:
    return UsersService(
        users_repo=UsersRepository(session=session_db),
        cr_context=test_crypto_context,
        session_db=session_db,
    )


@pytest_asyncio.fixture(scope="function")
async def website_service_fixture(session_db: AsyncSession) -> WebsitesService:
    return WebsitesService(
        website_repo=WebsiteRepository(
            session=session_db,
        ),
        session_db=session_db,
    )

