from datetime import datetime

from src.models.base.orm_dto import ORMDTO


class WebsitesDTO(ORMDTO):
    id: int
    user_id: int
    url: str
    name: str
    description: str
    check_interval_seconds: int
    timeout_in_seconds: int
    is_active: bool
    created_at: datetime


class WebsitesResponse(WebsitesDTO):
    pass