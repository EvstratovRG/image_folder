from fastapi import Path, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.db.dependency_providers import get_session
from application.types import UUID_TYPE
from users.models import User


async def get_user(
    user_id: UUID_TYPE = Path(), db_session: AsyncSession = Depends(get_session)
) -> User:
    stmt = select(User).where(User.id == user_id)
    cursor = await db_session.execute(stmt)
    user = cursor.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    return user
