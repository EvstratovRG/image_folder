from typing import TypeVar, Generic, Sequence, Any, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from application.db.base_class import Base
from application.types import UUID_TYPE

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: type[T]) -> None:
        self.session = db_session
        self.model = model

    async def get_by_id(self, obj_id: UUID_TYPE | int) -> T | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        cursor = await self.session.execute(stmt)
        return cursor.scalars().one_or_none()

    async def get_list(self) -> Sequence[T]:
        stmt = select(self.model).order_by(self.model.id)
        cursor = await self.session.execute(stmt)
        return cursor.scalars().all()

    async def create(self, obj_data: dict[str, Any]) -> T:
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: UUID_TYPE | int, data: dict[str, Any]) -> T:
        stmt = update(self.model).where(self.model.id == obj_id).values(**data)
        await self.session.execute(stmt)
        await self.session.commit()
        return await cast(T, self.get_by_id(obj_id))

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()
