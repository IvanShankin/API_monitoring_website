from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from tests.models.websites.fixtures.factory import create_website_factory
from tests.models.websites.fixtures.models_dto import CreateWebsiteFixtureDTO
from src.models.website_check.models_dto import WebsiteChecksDTO
from tests.models.website_check.fixtures.models_dto import CreateWebsiteChecksFixtureDTO
from src.models.website_check.models import WebsiteChecks


async def create_website_checks(
    session_db: AsyncSession,
    crypto_context: CryptContext,
    new_websites_checks: CreateWebsiteChecksFixtureDTO = CreateWebsiteChecksFixtureDTO(),
) -> WebsiteChecksDTO:
    """
    :param new_websites_checks: если не передать website_id, то создастся website привязанный к данному пользователю
    """
    if not new_websites_checks.website_id:
        website = await create_website_factory(
            session_db=session_db,
            crypto_context=crypto_context,
            new_website=CreateWebsiteFixtureDTO(
                user_id=new_websites_checks.user_id,
            )
        )
        new_websites_checks.website_id = website.id

    website_check = WebsiteChecks(
        website_id=new_websites_checks.website_id,
        http_status_code=new_websites_checks.http_status_code,
        response_time_ms=new_websites_checks.response_time_ms,
        is_available=new_websites_checks.is_available,
        error_type=new_websites_checks.error_type,
        error_message=new_websites_checks.error_message,
    )
    session_db.add(website_check)
    await session_db.commit()
    await session_db.refresh(website_check)

    return WebsiteChecksDTO.model_validate(website_check)

