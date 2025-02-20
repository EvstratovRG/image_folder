from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.db.dependency_providers import get_session
from users.models import User
from users.services import UserService

from .exceptions import TokenDoNotSet, NotValidTokenType


def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db)


async def get_current_user(
    request: Request,
    service: UserService = Depends(get_user_service),
) -> User:
    token = request.headers.get("Authorization")
    if not token:
        raise TokenDoNotSet
    if not token.startswith("Bearer"):
        raise NotValidTokenType
    user = await service.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден."
        )
    return user
