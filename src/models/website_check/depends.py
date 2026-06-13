from fastapi import Depends

from src.core.database import get_db
from src.models.website_check.repository import WebsiteCheckRepository
from src.models.website_check.service import WebsiteCheckService


def get_website_check_service(
    session = Depends(get_db),
) -> WebsiteCheckService:
    return WebsiteCheckService(
        website_check_repo=WebsiteCheckRepository(session),
        session_db=session,
    )