from datetime import datetime

from pydantic import BaseModel

from src.models.base.orm_dto import ORMDTO
from src.models.website_check.models import ErrorType


class WebsiteChecksDTO(ORMDTO):
    id: int
    website_id: int
    http_status_code: int
    response_time_ms: int
    is_available: bool

    error_type: ErrorType
    error_message: str

    checked_at: datetime


class WebsiteChecksDTOResponse(WebsiteChecksDTO):
    pass


class CreateWebsiteChecksDTO(BaseModel):
    website_id: int
    http_status_code: int
    response_time_ms: int
    is_available: bool
    error_type: str
    error_message: str
