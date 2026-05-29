from datetime import datetime
from typing import List

from sqlalchemy import delete, select

from src.models.base.database_model import BaseRepository
from src.models.refresh_tokens.models import RefreshToken


class RefreshTokenRepository(BaseRepository):

    async def add_token(
        self,
        user_id: int,
        token: str,
        expires_at: datetime,
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        return await self.add(token)

    async def get_token(self, token: str) -> RefreshToken | None:
        result_db = await self.session.execute(
            select(RefreshToken)
            .where(RefreshToken.token == token)
        )
        return result_db.scalar_one_or_none()

    async def delete_expires_tokens(self) -> List[RefreshToken]:
        result_db = await self.session.execute(
            delete(RefreshToken)
            .where(RefreshToken.expires_at < datetime.now())
            .returning(RefreshToken)
        )
        return result_db.scalars().all()