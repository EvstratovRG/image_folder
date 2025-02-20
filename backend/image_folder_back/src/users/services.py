from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_user_data, verify_hash, decode_data_from_token
from base.service import BaseService
from users.models import User
from users.repositories import UserRepository
from users.schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    RestorePasswordSchema,
)


class UserService(BaseService[User]):
    repository: UserRepository

    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(UserRepository(db_session))

    async def get_user_by_params(
        self, username: str | None = None, email: str | None = None
    ) -> User | None:
        return await self.repository.get_by_unique_params(username, email)

    async def create(self, data: CreateUserSchema) -> User:
        existing_user = await self.repository.get_by_unique_params(
            data.username,
            str(data.email),
        )
        if existing_user and existing_user.email == data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с email {data.email} уже существует!",
            )
        elif existing_user and existing_user.username == data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с именем {data.username} уже существует!",
            )
        data_dict = data.model_dump()
        data_dict.pop("confirm_password")
        hashed_pass_data = hash_user_data(data.password, data.code_phrase)
        data_dict.update(hashed_pass_data)
        return await self.repository.create(data_dict)

    async def update(self, user: User, data: UpdateUserSchema) -> User:
        return await self.repository.update(user, data.model_dump())

    async def get_user_by_token(self, token: str) -> User | None:
        token = token.replace("Bearer ", "")
        username = decode_data_from_token(token=token)
        return await self.repository.get_by_unique_params(username=username)

    @staticmethod
    async def set_password(user: User, password: str) -> bool:
        user.password = hash_user_data(password)["password"]
        return True

    async def reset_password(self, user: User, data: RestorePasswordSchema) -> bool:
        is_match_code_phrase = verify_hash(data.code_phrase, user.code_phrase)
        if not is_match_code_phrase:
            return False
        return await self.set_password(user, data.password)
