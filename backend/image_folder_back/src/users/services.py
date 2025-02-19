from fastapi import HTTPException, status
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

    async def get_user_by_params(
        self, username: str | None = None, email: str | None = None
    ) -> User | None:
        return await self.repository.get_by_unique_params(username, email)

    async def create(self, data: CreateUserBaseModel) -> User:
        existing_user = await self.repository.get_by_unique_params(
            data.username,
            str(data.email),
        )
        if existing_user:
            if existing_user.email == data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Пользователь с email {data.email} уже существует!",
                )
            elif existing_user.username != data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Пользователь с именем {data.username} уже существует!",
                )
        data_dict = data.model_dump()
        hashed_pass_data = hash_user_data(data.password, str(data.code_phrase))
        data_dict.update(hashed_pass_data)
        return await self.repository.create(data_dict)

    async def update(self, user: User, data: UpdateUserBaseModel) -> User:
        return await self.repository.update(user, data.model_dump())
