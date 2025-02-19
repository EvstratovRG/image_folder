from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from base.repository import BaseRepository
from users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, User)

    async def get_by_unique_params(
        self, username: str | None = None, email: str | None = None
    ) -> User | None:
        if not username and email:
            return None
        stmt = select(User).where(or_(User.username == username, User.email == email))
        cursor = await self.session.execute(stmt)
        return cursor.scalar_one_or_none()

    async def update(self, user: User, data: dict[str, Any]) -> User:
        filtered_data = {key: value for key, value in data.items() if value is not None}
        for key, value in filtered_data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
