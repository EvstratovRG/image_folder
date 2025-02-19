from typing import TypeVar, Generic

from application.db.base_class import Base
from base.repository import BaseRepository
from utils.pagination import Pagination, MetaPagination

T = TypeVar("T", bound=Base)


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]) -> None:
        self.repository = repository

    async def get_by_id(self, obj_id: int) -> T | None:
        return await self.repository.get_by_id(obj_id)

    async def get_list(self, pagination: Pagination) -> tuple[MetaPagination, list[T]]:
        return await self.repository.get_list(pagination)

    async def delete(self, obj: T) -> None:
        await self.repository.delete(obj)
