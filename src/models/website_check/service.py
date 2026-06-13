from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.website_check.exceptions import WebsiteCheckNotFound
from src.models.website_check.models_dto import WebsiteChecksDTO, CreateWebsiteChecksDTO
from src.models.website_check.repository import WebsiteCheckRepository


class WebsiteCheckService:

    def __init__(
        self,
        website_check_repo: WebsiteCheckRepository,
        session_db: AsyncSession,
    ):
        self.website_check_repo = website_check_repo
        self.session_db = session_db

    async def create_website_checks(self, data: CreateWebsiteChecksDTO) -> WebsiteChecksDTO:
        result = await self.website_check_repo.added_website_checks(
            data=data
        )
        await self.session_db.refresh(result)
        await self.session_db.commit()
        return WebsiteChecksDTO.model_validate(result)

    async def get_check_by_id(self, check_id: int, user_id: int) -> WebsiteChecksDTO:
        """
        :exception WebsiteCheckNotFound:
        """
        check = await self.website_check_repo.get_website_checks_by_check_id(website_check_id=check_id, user_id=user_id)
        if not check:
            raise WebsiteCheckNotFound()

        return WebsiteChecksDTO.model_validate(check)

    async def get_checks_by_website_id(self, website_id: int, user_id: int) -> List[WebsiteChecksDTO]:
        checks = await self.website_check_repo.get_website_checks_by_website_id(website_id=website_id, user_id=user_id)
        return [WebsiteChecksDTO.model_validate(check) for check in checks]

    async def delete_by_ids(self, check_ids: List[int], user_id: int) -> WebsiteChecksDTO:
        result = await self.website_check_repo.delete_by_ids(check_ids=check_ids, user_id=user_id)
        await self.session_db.commit()
        return WebsiteChecksDTO.model_validate(result)

    async def delete_by_website_id(self, website_id: int, user_id: int) -> List[WebsiteChecksDTO]:
        result = await self.website_check_repo.delete_by_website_id(website_id=website_id, user_id=user_id)
        await self.session_db.commit()
        return [WebsiteChecksDTO.model_validate(check) for check in result]


