from src.models.base.orm_dto import ORMDTO


class RefreshTokenDTO(ORMDTO):
    refresh_token_id: int
    user_id: int
    token: str
    expires_at: str
    created_at: str