from typing import Optional

from pydantic import BaseModel


class CreateUserFixtureDTO(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None