from fastapi import APIRouter, status, Depends, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence

from application.db.dependency_providers import get_session
from application.types import UUID_TYPE
from auth.dependencies import get_current_user
from users.dependencies import get_user
from users.models import User
from users.services import UserService
from users.schemas import UserBaseModel, CreateUserBaseModel, UpdateUserBaseModel

router = APIRouter(tags=["users"])


@router.get(
    path="/users/me/", status_code=status.HTTP_200_OK, response_model=UserBaseModel
)
async def get_me(
    db_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user


@router.get(
    path="/users/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserBaseModel,
)
async def get_user_detail(
    user_id: UUID_TYPE = Path(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> User:
    return await service.get_by_id(user_id)


@router.patch(
    path="/users/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserBaseModel,
)
async def update_user(
    user: User = Depends(get_user),
    data: UpdateUserBaseModel = Body(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> User:
    return await service.update(user, data)


@router.get(
    path="/users/", status_code=status.HTTP_200_OK, response_model=list[UserBaseModel]
)
async def get_list_users(
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> Sequence:
    return await service.get_list()


@router.post(
    path="/users/", status_code=status.HTTP_201_CREATED, response_model=UserBaseModel
)
async def create_user(
    data: CreateUserBaseModel = Body(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> User:
    return await service.create(data)
