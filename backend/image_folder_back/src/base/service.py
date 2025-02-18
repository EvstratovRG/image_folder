from typing import TypeVar, Generic, Sequence

from application.db.base_class import Base
from base.repository import BaseRepository

T = TypeVar("T", bound=Base)


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]) -> None:
        self.repository = repository

    async def get_by_id(self, obj_id: int) -> T | None:
        return await self.repository.get_by_id(obj_id)

    async def get_list(self) -> Sequence[T]:
        return await self.repository.get_list()

    async def delete(self, obj: T) -> str:
        await self.repository.delete(obj)
        return f"Объект {obj.id} успешно удалён."
