from src.models.auth.exception import InvalidCredentials
from src.models.auth.models import TokenResponse
from src.models.auth.token_service import TokenService
from src.models.users.service import UsersService


class AuthService:

    def __init__(
        self,
        users_service: UsersService,
        token_service: TokenService,
    ):
        self.users_service = users_service
        self.token_service = token_service

    async def login(
        self,
        username: str,
        password: str
    ) -> TokenResponse:

        user = await self.users_service.get_user_by_username_or_email(username)

        if not user:
            raise InvalidCredentials()

        if not self.users_service.verify_password(
            password,
            user.hashed_password
        ):
            raise InvalidCredentials()

        return await self.token_service.create_token_response(user_id=user.id)
