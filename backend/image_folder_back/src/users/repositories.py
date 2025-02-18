from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from base.repository import BaseRepository
from users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, User)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        cursor = await self.session.execute(stmt)
        return cursor.scalars().one_or_none()

    async def get_by_unique_params(self, username: str, email: str) -> bool:
        stmt = select(User).where(User.username == username, User.email == email)
        cursor = await self.session.execute(stmt)
        return cursor.scalar() is not None

    async def update(self, user: User, data: dict[str, Any]) -> User:
        filtered_data = {key: value for key, value in data.items() if value is not None}
        for key, value in filtered_data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
