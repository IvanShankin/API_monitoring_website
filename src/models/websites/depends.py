from fastapi import Depends

from src.core.database import get_db
from src.models.websites.repository import WebsiteRepository
from src.models.websites.service import WebsitesService


def get_website_service(
    session = Depends(get_db),
) -> WebsitesService:
    return WebsitesService(
        website_repo=WebsiteRepository(session),
        session_db=session,
    )