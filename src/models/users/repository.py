from sqlalchemy import select

from src.models.base.database_model import BaseRepository
from src.models.users.models import Users


class UsersRepository(BaseRepository):

    async def add_user(
        self,
        email: str,
        username: str,
        hashed_password: str,
    ) -> Users:

        user = Users(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )

        return await self.add(user)

    async def get_user_by_id(self, user_id: int) -> Users:
        return await self.get_by_id(Users, user_id)

    async def get_user_by_email(self, email: str) -> Users | None:
        result_db = await self.session.execute(select(Users).where(Users.email == email))
        return result_db.scalar_one_or_none()



