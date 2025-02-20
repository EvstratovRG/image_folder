from fastapi import APIRouter, status, Depends, Body, Path

from application.db.dependency_providers import get_session
from application.types import UUID_TYPE
from auth.dependencies import get_current_user
from users.dependencies import get_user
from users.models import User
from users.services import UserService
from users.schemas import (
    UserBaseSchema,
    CreateUserSchema,
    UpdateUserSchema,
    RestorePasswordSchema,
    SetNewPasswordSchema,
    UserListSchema,
)
from utils.pagination import Pagination, get_pagination

router = APIRouter(tags=["users"], prefix="/users")


@router.get(
    path="/me/",
    status_code=status.HTTP_200_OK,
    response_model=UserBaseSchema,
)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post(
    path="/{user_id}/reset-password/",
    status_code=status.HTTP_200_OK,
)
async def reset_password(
    user: User = Depends(get_user),
    data: RestorePasswordSchema = Body(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> bool:
    return await service.reset_password(user, data)


@router.post(
    path="/set-new-password/",
    status_code=status.HTTP_200_OK,
)
async def set_new_password(
    current_user: User = Depends(get_current_user),
    data: SetNewPasswordSchema = Body(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> bool:
    return await service.set_password(current_user, data.password)


@router.get(
    path="/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserBaseSchema,
)
async def get_user_detail(
    user_id: UUID_TYPE = Path(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> User:
    return await service.get_by_id(user_id)


@router.patch(
    path="/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserBaseSchema,
)
async def update_user(
    user: User = Depends(get_user),
    data: UpdateUserSchema = Body(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> User:
    return await service.update(user, data)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=UserListSchema,
)
async def get_list_users(
    pagination: Pagination = Depends(get_pagination),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> UserListSchema:
    meta, result = await service.get_list(pagination)
    return UserListSchema(
        items=[UserBaseSchema.model_validate(user) for user in result],
        meta=meta,
    )


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserBaseSchema,
)
async def create_user(
    data: CreateUserSchema = Body(),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> User:
    return await service.create(data)


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(lambda db=Depends(get_session): UserService(db)),
) -> None:
    return await service.delete(current_user)
