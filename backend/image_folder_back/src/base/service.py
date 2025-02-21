from typing import overload, Any

from fastapi import HTTPException, status

from application.types import Model
from base.repository import BaseRepository
from users.models import User
from utils.pagination import Pagination, MetaPagination


class BaseService:
    repository: BaseRepository

    def __init__(self, repository: BaseRepository[Model]) -> None:
        self.repository = repository

    async def get_by_id(self, obj_id: int) -> Model | None:
        return await self.repository.get_by_id(obj_id)

    @overload
    async def get_list(self, pagination: None = None) -> list[Model]: ...

    @overload
    async def get_list(
        self, pagination: Pagination
    ) -> tuple[MetaPagination, list[Model]]: ...

    async def get_list(
        self,
        pagination: Pagination | None = None,
    ) -> tuple[MetaPagination, list[Model]] | list[Model]:
        return await self.repository.get_list(pagination)

    async def update(self, object_id: int, user: User, data: dict[str, Any]) -> Model:
        if not user.is_superuser:
            can_update = await self.repository.is_object_author(object_id, user.id)
            if not can_update:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Вам не доступна эта операция.",
                )
        return await self.repository.update(object_id, data)

    async def delete(self, obj: Model) -> None:
        await self.repository.delete(obj)
