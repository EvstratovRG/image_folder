from pydantic import BaseModel, Field, EmailStr

from application.types import UUID_TYPE


class UserBaseModel(BaseModel):
    id: UUID_TYPE
    username: str
    firstname: str
    lastname: str
    email: str


class CreateUserBaseModel(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    firstname: str = Field(min_length=3, max_length=100)
    lastname: str = Field(min_length=3, max_length=100)
    email: EmailStr = Field(min_length=3, max_length=100)
    password: str = Field(min_length=5, max_length=100)  # TODO: хэшировать пароль
    code_phrase: str = Field(
        min_length=5, max_length=100
    )  # TODO: хэшировать кодовую фразу

    # TODO: добавить валидацию пароля, чтобы использовались цифры + символы


class UpdateUserBaseModel(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=100)
    firstname: str | None = Field(default=None, min_length=3, max_length=100)
    lastname: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = Field(default=None, min_length=3, max_length=100)
    password: str | None = Field(
        default=None, min_length=5, max_length=100
    )  # TODO: хэшировать пароль
    code_phrase: str | None = Field(
        default=None, min_length=5, max_length=100
    )  # TODO: хэшировать кодовую фразу
