from typing import List

from sqlalchemy import delete, select

from src.models.base.database_model import BaseRepository
from src.models.website_check.models import ErrorType, WebsiteChecks


class WebsiteCheck(BaseRepository):

    async def added_website_checks(
        self,
        website_id: int,
        http_status_code: int,
        response_time_ms: int,
        is_available: bool,
        error_type: ErrorType,
        error_message: str,
    ) -> WebsiteChecks:
        return self.add(
            instance=WebsiteChecks(
                website_id=website_id,
                http_status_code=http_status_code,
                response_time_ms=response_time_ms,
                is_available=is_available,
                error_type=error_type,
                error_message=error_message,
            )
        )

    async def get_website_checks_by_check_id(self, website_check_id: int) -> WebsiteChecks | None:
        result_db = await self.session.execute(
            select(WebsiteChecks)
            .where(WebsiteChecks.id == website_check_id)
        )
        return result_db.scalar_one_or_none()

    async def get_website_checks_by_website_id(self, website_id: int) -> List[WebsiteChecks]:
        result_db = await self.session.execute(
            select(WebsiteChecks)
            .where(WebsiteChecks.website_id == website_id)
        )
        return result_db.scalars().all()

    async def delete_by_id(self, check_id: int) -> WebsiteChecks | None:
        result_db = await self.session.execute(
            delete(WebsiteChecks)
            .where(WebsiteChecks.id == check_id)
            .returning(WebsiteChecks)
        )
        return result_db.scalar_one_or_none()

    async def delete_by_website_id(self, website_id: int) -> List[WebsiteChecks]:
        result_db = await self.session.execute(
            delete(WebsiteChecks)
            .where(WebsiteChecks.website_id == website_id)
            .returning(WebsiteChecks)
        )
        return result_db.scalars().all()