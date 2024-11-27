from fastapi import APIRouter, status, Depends, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence

from application.db.dependency_providers import get_session
from application.types import UUID_TYPE
from auth.dependencies import get_current_user
from users.models import User
from users.schemas import UserBaseModel, CreateUserBaseModel, UpdateUserBaseModel
from users.services import (
    update_user_service,
    create_user_service,
    get_users_service,
    get_detail_user_service,
)

router = APIRouter(tags=['users'])


@router.get(
    path="/users/me/", status_code=status.HTTP_200_OK, response_model=UserBaseModel
)
async def get_me(
    db_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user


@router.patch(
    path="/users/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserBaseModel,
)
async def update_user(
    user_id: UUID_TYPE = Path(),
    data: UpdateUserBaseModel = Body(),
    db_session: AsyncSession = Depends(get_session),
) -> User:
    user = await update_user_service(user_id, data.model_dump(), db_session)
    return user


@router.get(
    path="/users/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserBaseModel,
)
async def get_user_detail(
    user_id: UUID_TYPE = Path(),
    db_session: AsyncSession = Depends(get_session),
) -> User:
    return await get_detail_user_service(user_id, db_session)


@router.get(
    path="/users/", status_code=status.HTTP_200_OK, response_model=list[UserBaseModel]
)
async def get_list_users(
    db_session: AsyncSession = Depends(get_session),
) -> Sequence:
    return await get_users_service(db_session)


@router.post(
    path="/users/", status_code=status.HTTP_201_CREATED, response_model=UserBaseModel
)
async def create_user(
    data: CreateUserBaseModel = Body(),
    db_session: AsyncSession = Depends(get_session),
) -> User:
    return await create_user_service(data.model_dump(), db_session)
