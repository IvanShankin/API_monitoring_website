from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.website_check.models_dto import WebsiteChecksDTO, CreateWebsiteChecksDTO
from src.models.website_check.repository import WebsiteCheckRepository


class WebsiteChecksService:

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
        await self.session_db.commit()
        return WebsiteChecksDTO.model_validate(result)

    async def get_check_by_id(self, check_id: int) -> WebsiteChecksDTO | None:
        check = await self.website_check_repo.get_website_checks_by_check_id(check_id)
        return WebsiteChecksDTO.model_validate(check) if check else None

    async def get_check_by_website_id(self, website_id: int) -> WebsiteChecksDTO | None:
        check = await self.website_check_repo.get_website_checks_by_website_id(website_id)
        return WebsiteChecksDTO.model_validate(check) if check else None

    async def delete_by_id(self, check_id: int) -> WebsiteChecksDTO | None:
        result = await self.website_check_repo.delete_by_id(check_id)
        await self.session_db.commit()
        return WebsiteChecksDTO.model_validate(result) if result else None

    async def delete_by_website_id(self, website_id: int) -> List[WebsiteChecksDTO]:
        result = await self.website_check_repo.delete_by_website_id(website_id)
        await self.session_db.commit()
        return [WebsiteChecksDTO.model_validate(check) for check in result]


