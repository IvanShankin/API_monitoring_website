from typing import List

from sqlalchemy import delete, select, and_, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base.database_model import BaseRepository
from src.models.website_check.models import WebsiteChecks
from src.models.website_check.models_dto import CreateWebsiteChecksDTO
from src.models.websites.models import Websites


class WebsiteCheckRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=WebsiteChecks)

    async def added_website_checks(
        self,
        data: CreateWebsiteChecksDTO
    ) -> WebsiteChecks:
        return self.add(
            data
        )

    async def get_website_checks_by_check_id(self, website_check_id: int, user_id: int) -> WebsiteChecks | None:
        result_db = await self.session.execute(
            select(WebsiteChecks)
            .join(Websites, WebsiteChecks.website_id == Websites.id)
            .where(
                (WebsiteChecks.id == website_check_id) &
                (Websites.user_id == user_id)
            )
        )
        return result_db.scalar_one_or_none()

    async def get_website_checks_by_website_id(self, website_id: int, user_id: int) -> List[WebsiteChecks]:
        result_db = await self.session.execute(
            select(WebsiteChecks)
            .join(Websites, WebsiteChecks.website_id == Websites.id)
            .where(
                (WebsiteChecks.website_id == website_id) &
                (Websites.user_id == user_id)
            )
        )
        return result_db.scalars().all()

    async def delete_by_ids(self, check_ids: List[int], user_id: int) -> List[WebsiteChecks]:
        result_db = await self.session.execute(
            delete(WebsiteChecks)
            .where(
                and_(
                    WebsiteChecks.id.in_(check_ids),
                    exists().where(
                        and_(
                            WebsiteChecks.website_id == Websites.id,
                            Websites.user_id == user_id
                        )
                    )
                )
            )
            .returning(WebsiteChecks)
        )
        return result_db.scalars().all()

    async def delete_by_website_id(self, website_id: int, user_id: int) -> List[WebsiteChecks]:
        result_db = await self.session.execute(
            delete(WebsiteChecks)
            .where(
                and_(
                    WebsiteChecks.id == website_id,
                    exists().where(
                        and_(
                            WebsiteChecks.website_id == Websites.id,
                            Websites.user_id == user_id
                        )
                    )
                )
            )
            .returning(WebsiteChecks)
        )
        return result_db.scalars().all()