from typing import Any, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from application.types import UUID_TYPE, Model
from utils.pagination import Pagination, paginate_query, MetaPagination


class BaseRepository:
    def __init__(self, db_session: AsyncSession, model: type[Model]) -> None:
        self.session = db_session
        self.model = model

    async def is_object_author(self, obj_id: int, author_id: UUID_TYPE) -> bool:
        stmt = select(self.model).where(
            self.model.id == obj_id, self.model.author_id == author_id
        )
        cursor = await self.session.execute(stmt)
        return cursor.scalar_one_or_none() is not None

    async def get_by_id(self, obj_id: UUID_TYPE | int) -> Model | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        cursor = await self.session.execute(stmt)
        return cursor.scalars().one_or_none()

    async def get_list(
        self,
        pagination: Pagination | None = None,
    ) -> tuple[MetaPagination, list[Model]] | list[Model]:
        stmt = select(self.model).order_by(self.model.id)
        if pagination:
            return await paginate_query(self.session, stmt, pagination)
        cursor = await self.session.execute(stmt)
        return list(cursor.scalars().all())

    async def create(self, obj_data: dict[str, Any]) -> Model:
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: UUID_TYPE | int, data: dict[str, Any]) -> Model:
        stmt = update(self.model).where(self.model.id == obj_id).values(**data)
        await self.session.execute(stmt)
        await self.session.commit()
        return await cast(Model, self.get_by_id(obj_id))

    async def delete(self, obj: Model) -> None:
        await self.session.delete(obj)
        await self.session.commit()
