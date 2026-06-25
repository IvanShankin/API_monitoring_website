from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete, func

from src.models.base.database_model import BaseRepository
from src.models.websites.exception import NoDataForUpdateWebsite
from src.models.websites.models import Websites
from src.models.websites.models_dto import CreateWebsiteDTO, UpdateWebsiteDTO, WebsitesDTO


class WebsiteRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Websites)

    async def add_website(
        self,
        data: CreateWebsiteDTO,
    ) -> Websites:
        return self.add(data)

    async def get_website(
        self,
        website_id: int,
    ) -> Websites | None:
        result_db = await self.session.execute(
            select(Websites)
            .where(Websites.id == website_id)
        )
        return result_db.scalar_one_or_none()

    async def get_websites_for_tests(self, date_from: datetime) -> List[WebsitesDTO]:
        result_db = await self.session.execute(
            select(Websites)
            .where(
                Websites.is_active == True,
                date_from > Websites.last_check_at + func.make_interval(secs=Websites.check_interval_seconds)
            )
        )
        return result_db.scalars().all()

    async def get_all_websites_by_users(
        self,
        user_id: int,
    ) -> List[WebsitesDTO]:
        result_db = await self.session.execute(
            select(Websites)
            .where(Websites.user_id == user_id)
        )
        return result_db.scalars().all()

    async def update_website(
        self,
        website_id: int,
        user_id: int,
        data: UpdateWebsiteDTO,
    ) -> Websites | None:
        """
        :exception NoDataForUpdateWebsite:
        """
        values = data.model_dump(exclude_unset=True)
        if not values:
            raise NoDataForUpdateWebsite()

        result_db = await self.session.execute(
            update(Websites)
            .where(
                (Websites.id == website_id) &
                (Websites.user_id == user_id)
            )
            .values(**values)
            .returning(Websites)
        )
        return result_db.scalar_one_or_none()

    async def delete_website(
        self,
        user_id: int,
        website_ids: List[int],
    ) -> List[Websites]:
        result_db = await self.session.execute(
            delete(Websites)
            .where(
                (Websites.id.in_(website_ids)) &
                (Websites.user_id == user_id)
            )
            .returning(Websites)
        )
        return result_db.scalars().all()




