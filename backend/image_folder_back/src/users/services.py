from typing import AnyStr

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_user_data
from base.service import BaseService
from users.models import User
from users.repositories import UserRepository
from users.schemas import CreateUserBaseModel, UpdateUserBaseModel


class UserService(BaseService[User]):
    repository: UserRepository

    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(UserRepository(db_session))

    async def get_exist_by_params(self, *args: AnyStr) -> bool:
        return await self.repository.get_by_unique_params(*args)

    async def get_by_username(self, username: str) -> User:
        return await self.repository.get_by_username(username)

    async def create(self, data: CreateUserBaseModel) -> User:
        existing_user = await self.repository.get_by_unique_params(
            data.username, str(data.email)
        )
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=f"Пользователь с именем {data.username} и email {data.email} уже существует!",
            )

        data_dict = data.model_dump()
        hashed_pass_data = hash_user_data(data.password, str(data.code_phrase))
        data_dict.update(hashed_pass_data)
        return await self.repository.create(data_dict)

    async def update(self, user: User, data: UpdateUserBaseModel) -> User:
        return await self.repository.update(user, data.model_dump())
