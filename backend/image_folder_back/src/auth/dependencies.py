from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from application.db.dependency_providers import get_session
from users.models import User
from .services import get_user_by_token

from .exceptions import TokenDoNotSet, NotValidTokenType


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_session)
) -> User:
    token = request.headers.get("Authorization")
    if not token:
        raise TokenDoNotSet
    if not token.startswith("Bearer"):
        raise NotValidTokenType
    user = await get_user_by_token(session, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден."
        )
    return user
