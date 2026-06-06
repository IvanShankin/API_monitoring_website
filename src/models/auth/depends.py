from fastapi import Depends
from sqlalchemy.testing.pickleable import User

from src.config import Config
from src.models.auth.auth_service import AuthService
from src.models.auth.token_service import TokenService
from src.models.depends import get_config
from src.models.refresh_tokens.depends import get_refresh_tokens_service
from src.models.users.depends import get_user_service
from src.models.users.dto_models import UsersDTO


async def get_token_service(
    config: Config = Depends(get_config),
    user_service=Depends(get_user_service),
    refresh_token_service=Depends(get_refresh_tokens_service),
) -> TokenService:
    return TokenService(
        config=config,
        users_service=user_service,
        refresh_token_service=refresh_token_service,
    )


async def get_auth_service(
    user_service = Depends(get_user_service),
    token_service = Depends(get_token_service),
) -> AuthService:
    return AuthService(
        users_service=user_service,
        token_service=token_service
    )


async def get_current_user(
    user_service=Depends(get_user_service),
) -> UsersDTO:
    return user_service.get_current_user()