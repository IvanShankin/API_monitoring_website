from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.depends import get_config
from src.config import Config


async def get_db(
    config: Config = Depends(get_config),
) -> AsyncIterator[AsyncSession] :
    async_session_factory = config.db_connection.session_local
    async with async_session_factory() as session:
        yield session