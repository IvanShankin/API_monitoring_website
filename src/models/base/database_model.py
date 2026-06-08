from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import Base

# Объявляем generic тип, ограниченный классом Base
ModelType = TypeVar("ModelType", bound="Base")


class BaseRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, instance: ModelType):
        self.session.add(instance)
        return instance

    async def get_by_id(self, model: ModelType, obj_id: int) -> ModelType | None:
        stmt = select(model).where(model.id == obj_id)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
