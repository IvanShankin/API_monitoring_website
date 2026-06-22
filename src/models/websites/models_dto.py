from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.models.base.orm_dto import ORMDTO


class WebsitesDTO(ORMDTO):
    id: int
    user_id: int
    url: str
    name: str | None
    description: str | None
    check_interval_seconds: int
    timeout_in_seconds: int
    is_active: bool
    created_at: datetime


class WebsiteResponse(WebsitesDTO):
    pass


class CreateWebsiteRequestDTO(BaseModel):
    url: str
    name: Optional[str] = None
    description: Optional[str] = None
    check_interval_seconds: int = 60
    timeout_in_seconds: int = 15
    is_active: bool = True


class CreateWebsiteDTO(CreateWebsiteRequestDTO):
    user_id: int


class UpdateWebsiteDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    check_interval_seconds: Optional[int] = None
    timeout_in_seconds: Optional[int] = None
    is_active: Optional[bool] = None


class UpdateWebsiteRequestDTO(UpdateWebsiteDTO):
    pass
