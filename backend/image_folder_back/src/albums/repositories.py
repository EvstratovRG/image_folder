from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from albums.models import AlbumCategory
from application.types import UUID_TYPE
from base.repository import BaseRepository


class CategoryRepository(BaseRepository[AlbumCategory]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, AlbumCategory)

    async def get_users_album_category_by_title(
        self, author_id: UUID_TYPE, title: str
    ) -> AlbumCategory | None:
        stmt = select(AlbumCategory).where(
            AlbumCategory.title == title, AlbumCategory.author_id == author_id
        )
        cursor = await self.session.execute(stmt)
        return cursor.scalars().one_or_none()
