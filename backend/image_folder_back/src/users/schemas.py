import re

from pydantic import BaseModel, Field, EmailStr, model_validator

from application.types import UUID_TYPE
from utils.consts import UPPERCASE_WITH_DIGIT_AND_SYMBOL_REGEX


class UserBaseSchema(BaseModel):
    id: UUID_TYPE
    username: str
    firstname: str
    lastname: str
    email: str


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    firstname: str = Field(min_length=3, max_length=100)
    lastname: str = Field(min_length=3, max_length=100)
    email: EmailStr = Field(min_length=3, max_length=100)
    password: str = Field(min_length=5, max_length=100)
    confirm_password: str = Field(min_length=5, max_length=100)
    code_phrase: str = Field(min_length=5, max_length=100)

    @model_validator(mode="before")
    def validate_password(cls, data: dict[str, str]) -> dict[str, str]:
        if data["password"] != data["confirm_password"]:
            raise ValueError("Пароли не соответствуют!")
        if not re.match(UPPERCASE_WITH_DIGIT_AND_SYMBOL_REGEX, data["password"]):
            raise ValueError(
                "В пароле должны быть минимум 1 заглавная буква, 1 цифра и 1 символ!",
            )
        return data


class UpdateUserSchema(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=100)
    firstname: str | None = Field(default=None, min_length=3, max_length=100)
    lastname: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = Field(default=None, min_length=3, max_length=100)


class RestorePasswordSchema(BaseModel):
    code_phrase: str = Field(min_length=5, max_length=100)


class SetNewPasswordSchema(BaseModel):
    password: str = Field(min_length=5, max_length=100)
    confirm_password: str = Field(min_length=5, max_length=100)

    @model_validator(mode="before")
    def validate_password(cls, data: dict[str, str]) -> dict[str, str]:
        if data["password"] != data["confirm_password"]:
            raise ValueError("Пароли не соответствуют!")
        if not re.match(UPPERCASE_WITH_DIGIT_AND_SYMBOL_REGEX, data["password"]):
            raise ValueError(
                "В пароле должны быть минимум 1 заглавная буква, 1 цифра и 1 символ!",
            )
        return data
