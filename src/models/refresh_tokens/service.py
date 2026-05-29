import secrets
from datetime import datetime, timedelta, UTC

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import Config
from src.models.base.exception import ServiceException
from src.models.refresh_tokens.dto_models import RefreshTokenDTO
from src.models.refresh_tokens.repository import RefreshTokenRepository


class RefreshTokensService:

    def __init__(
        self,
        token_repo: RefreshTokenRepository,
        session_db: AsyncSession,
        config: Config,
    ):
        self.token_repo = token_repo
        self.session_db = session_db
        self.config = config

    def _generate_unique_token(self) -> str:
        return secrets.token_urlsafe(64)

    async def create_token(self, user_id: int):
        expires_at = datetime.now(UTC) + timedelta(
            days=self.config.tokens.refresh_token_expire_days
        )
        
        for i in range(5):
            try:
                token = self._generate_unique_token()
                token_orm = await self.token_repo.add_token(
                    user_id=user_id,
                    token=token,
                    expires_at=expires_at,
                )
                await self.session_db.commit()

                break
            except IntegrityError:
                await self.session_db.rollback()
        else:
            raise ServiceException("Failed to generate token")

        await self.session_db.refresh(token_orm)
        return RefreshTokenDTO.model_validate(token_orm) if token_orm else None

    async def get_token(self, refresh_token: str) -> RefreshTokenDTO | None:
        token = await self.token_repo.get_token(refresh_token)
        return RefreshTokenDTO.model_validate(token) if token else None
