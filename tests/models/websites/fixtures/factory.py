from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from tests.models.users.fixtures.factory import create_user_factory
from .models_dto import CreateWebsiteFixtureDTO
from src.models.websites.models import Websites
from src.models.websites.models_dto import WebsitesDTO


async def create_website_factory(
    session_db: AsyncSession,
    crypto_context: CryptContext,
    new_website: Optional[CreateWebsiteFixtureDTO] = None,
) -> WebsitesDTO:
    if new_website is None:
        new_website = CreateWebsiteFixtureDTO()

    if new_website.user_id is None:
        user = await create_user_factory(session_db, crypto_context)
        new_website.user_id = user.id

    website = Websites(
        **new_website.model_dump(),
    )
    session_db.add(website)
    await session_db.commit()
    await session_db.refresh(website)

    return WebsitesDTO.model_validate(website)