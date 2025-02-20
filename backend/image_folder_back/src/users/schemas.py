import re

from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict

from application.types import UUID_TYPE
from utils.consts import (
    UPPERCASE_WITH_DIGIT_AND_SYMBOL_REGEX,
    MAX_FIELD_LENGTH,
    MIN_FIELD_LENGTH,
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
)
from utils.pagination import MetaPagination


class UserBaseSchema(BaseModel):
    id: UUID_TYPE
    username: str
    firstname: str
    lastname: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserListSchema(BaseModel):
    items: list[UserBaseSchema]
    meta: MetaPagination


class BasePasswordSchema(BaseModel):
    password: str = Field(
        min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH
    )
    confirm_password: str = Field(
        min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH
    )

    @model_validator(mode="before")
    def validate_password(cls, data: dict[str, str]) -> dict[str, str]:
        if data["password"] != data["confirm_password"]:
            raise ValueError("Пароли не соответствуют!")
        if not re.match(UPPERCASE_WITH_DIGIT_AND_SYMBOL_REGEX, data["password"]):
            raise ValueError(
                "В пароле должны быть минимум 1 заглавная буква, 1 цифра и 1 символ!",
            )
        return data


class CreateUserSchema(BasePasswordSchema):
    username: str = Field(min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH)
    firstname: str = Field(min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH)
    lastname: str = Field(min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH)
    email: EmailStr = Field(min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH)
    code_phrase: str = Field(min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH)


class UpdateUserSchema(BaseModel):
    username: str | None = Field(
        default=None, min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH
    )
    firstname: str | None = Field(
        default=None, min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH
    )
    lastname: str | None = Field(
        default=None, min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH
    )
    email: EmailStr | None = Field(
        default=None, min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH
    )


class SetNewPasswordSchema(BasePasswordSchema):
    pass


class RestorePasswordSchema(SetNewPasswordSchema):
    code_phrase: str = Field(min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH)
