from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import create_config
from src.models.website_check.repository import WebsiteCheckRepository
from src.models.website_check.service import WebsiteCheckService
from src.models.websites.repository import WebsiteRepository
from src.models.websites.service import WebsitesService


class Container:

    def __init__(self) -> None:
        self.config = create_config()
        self.async_session_factory = self.config.db_connection.session_local

    async def get_db(
        self,
    ) -> AsyncIterator[AsyncSession]:
        async with self.async_session_factory() as session:
            yield session

    def get_website_repository(self, session: AsyncSession) -> WebsiteRepository:
        return WebsiteRepository(session=session)

    def get_website_service(self, session: AsyncSession) -> WebsitesService:
        return WebsitesService(
            website_repo=self.get_website_repository(session),
            session_db=session
        )

    def get_website_check_repository(self, session: AsyncSession) -> WebsiteCheckRepository:
        return WebsiteCheckRepository(session=session)

    def get_website_check_service(self, session: AsyncSession) -> WebsiteCheckService:
        return WebsiteCheckService(
            website_check_repo=self.get_website_check_repository(session),
            session_db=session
        )


container = Container()