import string
import random
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users.models import Users
from src.models.users.models_dto import UsersDTO


def _get_hash_password(crypto_context: CryptContext, password: str) -> str:
    """Преобразует пароль в хеш
    :return: хэш пароля"""
    return crypto_context.hash(password)


def _random_string(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


async def create_user_factory(
    session_db: AsyncSession,
    crypto_context: CryptContext,
    email: Optional[str],
    username: Optional[str],
    hashed_password: Optional[str],
) -> UsersDTO:
    user = Users(
        email=_random_string() + "@mail.com" if email is None else email,
        username=_random_string() if username is None else username,
        hashed_password=_get_hash_password(crypto_context=crypto_context, password=_random_string())
        if hashed_password is None else
        hashed_password,
    )
    session_db.add(user)
    await session_db.commit()

    return UsersDTO.model_validate(user)

