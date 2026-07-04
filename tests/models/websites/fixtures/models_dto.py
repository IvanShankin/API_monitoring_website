from typing import Optional

from pydantic import BaseModel


class CreateWebsiteFixtureDTO(BaseModel):
    user_id: Optional[int] = None
    url: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    check_interval_seconds: Optional[int] = None
    timeout_in_seconds: Optional[int] = None
    is_active: Optional[bool] = None