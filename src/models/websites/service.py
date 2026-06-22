from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.utils.check_permission import check_permission
from src.models.websites.exception import WebsiteNotFound
from src.models.websites.models_dto import CreateWebsiteDTO, UpdateWebsiteDTO, WebsitesDTO
from src.models.websites.repository import WebsiteRepository


class WebsitesService:

    def __init__(
        self,
        website_repo: WebsiteRepository,
        session_db: AsyncSession,
    ):
        self.website_repo = website_repo
        self.session_db = session_db

    async def create_website(
        self,
        data: CreateWebsiteDTO,
    ) -> WebsitesDTO:
        result = await self.website_repo.add_website(data)

        await self.session_db.refresh(result)
        await self.session_db.commit()

        return WebsitesDTO.model_validate(result)

    async def get_website(
        self,
        website_id: int,
        user_id: int,
    ) -> WebsitesDTO:
        result = await self.website_repo.get_website(website_id)
        if not result:
            raise WebsiteNotFound()

        check_permission(user_id, result.user_id)

        return WebsitesDTO.model_validate(result)

    async def get_all_websites(
        self,
        user_id: int,
    ) -> List[WebsitesDTO]:
        websites = await self.website_repo.get_all_websites(user_id)
        return [WebsitesDTO.model_validate(website) for website in websites]

    async def update_website(
        self,
        website_id: int,
        user_id: int,
        data: UpdateWebsiteDTO,
    ) -> WebsitesDTO:
        """
        :exception WebsiteNotFound:
        :exception NoDataForUpdateWebsite:
        """
        result = await self.website_repo.update_website(website_id=website_id, user_id=user_id, data=data)
        if not result:
            raise WebsiteNotFound()

        await self.session_db.commit()
        return WebsitesDTO.model_validate(result)

    async def delete_website(
        self,
        website_ids: List[int],
        user_id: int,
    ) -> List[WebsitesDTO]:
        websites = await self.website_repo.delete_website(user_id=user_id, website_ids=website_ids)
        await self.session_db.commit()
        return [WebsitesDTO.model_validate(website) for website in websites]
