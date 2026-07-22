from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.models.base.orm_dto import ORMDTO
from src.models.website_check.models import ErrorType


class WebsiteChecksDTO(ORMDTO):
    id: int
    website_id: int
    http_status_code: Optional[int]
    response_time_ms: Optional[int]
    is_available: bool

    error_type: Optional[ErrorType]
    error_message: Optional[str]

    checked_at: datetime


class WebsiteChecksDTOResponse(WebsiteChecksDTO):
    pass


class CreateWebsiteChecksDTO(BaseModel):
    website_id: int
    http_status_code: int | None
    response_time_ms: int | None
    is_available: bool
    error_type: Optional[ErrorType] = None
    error_message: Optional[str] = None
