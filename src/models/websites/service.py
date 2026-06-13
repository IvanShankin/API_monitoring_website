from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.websites.models_dto import CreateWebsitesDTO, UpdateWebsiteDTO, WebsitesDTO
from src.models.websites.repository import WebsiteRepository


class WebsitesService:

    def __init__(
        self,
        website_repo: WebsiteRepository,
        session: AsyncSession,
    ):
        self.website_repo = website_repo
        self.session = session

    async def create_website(
        self,
        data: CreateWebsitesDTO,
    ) -> WebsitesDTO:
        result = await self.website_repo.add_website(data)
        await self.session.commit()
        return WebsitesDTO.model_validate(result)

    async def get_website(
        self,
        website_id: int,
    ) -> WebsitesDTO | None:
        result = await self.website_repo.get_website(website_id)
        return WebsitesDTO.model_validate(result) if result else None

    async def get_all_websites(
        self,
        user_id: int,
    ) -> List[WebsitesDTO]:
        websites = await self.website_repo.get_all_websites(user_id)
        return [WebsitesDTO.model_validate(website) for website in websites]

    async def update_website(
        self,
        website_id: int,
        data: UpdateWebsiteDTO,
    ) -> WebsitesDTO | None:
        result = await self.website_repo.update_website(website_id=website_id, data=data)
        return WebsitesDTO.model_validate(result) if result else None

    async def delete_website(
        self,
        website_ids: List[int],
    ) -> List[WebsitesDTO]:
        websites = await self.website_repo.delete_website(website_ids=website_ids,)
        return [WebsitesDTO.model_validate(website) for website in websites]
