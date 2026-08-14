import pytest_asyncio

from .factory import create_website_checks
from .models_dto import CreateWebsiteChecksFixtureDTO
from src.models.website_check.models_dto import WebsiteChecksDTO
from tests.helpers import test_crypto_context
from src.core.config import Config


@pytest_asyncio.fixture(scope="function")
async def create_website_check_fixture(
    config_fix: Config,
    not_open_session_db
):

    async def _factory(
        new_websites_checks: CreateWebsiteChecksFixtureDTO = CreateWebsiteChecksFixtureDTO(),
    ) -> WebsiteChecksDTO:
        async with not_open_session_db() as session:
            website_check = await create_website_checks(
                session_db=session,
                crypto_context=test_crypto_context,
                new_websites_checks=new_websites_checks,
            )
            return website_check

    return _factory