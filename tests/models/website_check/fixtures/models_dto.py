from typing import Optional

from pydantic import BaseModel

from src.models.website_check.models import ErrorType


class CreateWebsiteChecksFixtureDTO(BaseModel):
    user_id: Optional[int] = None # если не передать website_id, то создастся website привязанный к данному пользователю

    website_id: Optional[int] = None
    http_status_code: Optional[int] = 200
    response_time_ms: Optional[int] = 140
    is_available: Optional[bool] = True

    error_type: Optional[ErrorType] = None
    error_message: Optional[str] = None
