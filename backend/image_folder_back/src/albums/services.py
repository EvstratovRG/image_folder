from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from albums.models import AlbumCategory
from albums.repositories import CategoryRepository
from application.types import UUID_TYPE
from base.service import BaseService


class CategoryService(BaseService[AlbumCategory]):
    repository: CategoryRepository

    def __init__(self, db_session: AsyncSession):
        super().__init__(CategoryRepository(db_session))

    async def create(self, author_id: UUID_TYPE, data: dict[str, Any]) -> AlbumCategory:
        data["author_id"], title = author_id, data["title"]
        is_exists = await self.repository.get_users_album_category_by_title(
            author_id,
            title,
        )
        if is_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категория {title} - уже существует.",
            )
        return await self.repository.create(data)
