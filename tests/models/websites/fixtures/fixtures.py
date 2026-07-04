from typing import Optional

import pytest_asyncio
from passlib.context import CryptContext

from models.websites.fixtures.factory import create_website_factory
from models.websites.fixtures.models_dto import CreateWebsiteFixtureDTO
from src.core.config import Config
from src.models.websites.models_dto import WebsitesDTO


@pytest_asyncio.fixture(scope="function")
async def create_website_fixture(
    crypto_context_fix: CryptContext,
    config_fix: Config,
    not_open_session_db
):
    async def _factory(
        new_website: Optional[CreateWebsiteFixtureDTO] = None,
    ) -> WebsitesDTO:

        async with not_open_session_db() as session:
            website = await create_website_factory(
                session_db=session,
                crypto_context=crypto_context_fix,
                new_website=new_website,
            )

            return website

    return _factory