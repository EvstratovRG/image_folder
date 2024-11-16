from fastapi import APIRouter, Depends, status, HTTPException

from application.db.dependency_providers import get_session
from .hasher import Hasher
from .schemas import AuthTokenResponseSchema, AuthLoginSchema, AuthRefreshSchema
from sqlalchemy.ext.asyncio import AsyncSession
from .services import get_user_by_username
from .utils import create_token, decode_data_from_token
from .enums import TokenTypesEnum
from users.models import User


router = APIRouter()


def _create_tokens(
    user: User,
) -> AuthTokenResponseSchema:
    access = create_token(TokenTypesEnum.access, user.username)
    refresh = create_token(TokenTypesEnum.refresh, user.username)
    return AuthTokenResponseSchema(access_token=access, refresh_token=refresh)


@router.post(
    "/auth/token/",
    status_code=status.HTTP_200_OK,
    response_model=AuthTokenResponseSchema,
)
async def login(
    payload: AuthLoginSchema,
    db_session: AsyncSession = Depends(get_session),
) -> AuthTokenResponseSchema:
    user = await get_user_by_username(db_session, payload.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь {payload.username} не найден.",
        )
    if not Hasher.verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Не верный пароль."
        )
    return _create_tokens(user)


@router.post(
    "/auth/refresh/",
    status_code=status.HTTP_200_OK,
    response_model=AuthTokenResponseSchema,
)
async def refresh_tokens(
    payload: AuthRefreshSchema,
    db_session: AsyncSession = Depends(get_session),
) -> AuthTokenResponseSchema:
    username = decode_data_from_token(payload.refresh_token, TokenTypesEnum.refresh)
    user = await get_user_by_username(db_session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь по токену - не найден.",
        )
    return _create_tokens(user)
