from fastapi import APIRouter, Depends, status, HTTPException

from application.db.dependency_providers import get_session
from users.services import UserService
from .hasher import Hasher
from .schemas import AuthTokenResponseSchema, AuthLoginSchema, AuthRefreshSchema
from .utils import create_token, decode_data_from_token
from .enums import TokenTypesEnum
from users.models import User


router = APIRouter(tags=["auth"])


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
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> AuthTokenResponseSchema:
    user = await service.get_user_by_params(payload.username)
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
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> AuthTokenResponseSchema:
    username = decode_data_from_token(payload.refresh_token, TokenTypesEnum.refresh)
    user = await service.get_user_by_params(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь по токену - не найден.",
        )
    return _create_tokens(user)
