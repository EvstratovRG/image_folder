from datetime import datetime, timedelta
from typing import Union, Any
from application.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY,
)

from passlib.context import CryptContext
from jose import jwt

from .enums import TokenTypesEnum

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def hash_user_password(data: dict[str, Any]) -> dict[str, Any]:
    password = data["password"]
    hashed_pass = get_hashed_password(password)
    data["password"] = hashed_pass
    return data


def create_token(
    token_type: TokenTypesEnum,
    subject: Union[str, Any],
) -> str:
    expires_delta = datetime.utcnow() + timedelta(
        minutes=int(
            ACCESS_TOKEN_EXPIRE_MINUTES
            if token_type.name == TokenTypesEnum.access
            else REFRESH_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY
        if token_type.name == TokenTypesEnum.access
        else JWT_REFRESH_SECRET_KEY,
        ALGORITHM,
    )
    return encoded_jwt


def decode_data_from_token(
    token: str,
    token_type: TokenTypesEnum = TokenTypesEnum.access,
) -> str:
    decoded_jwt = jwt.decode(
        token,
        JWT_REFRESH_SECRET_KEY if token_type.refresh else JWT_SECRET_KEY,
        ALGORITHM,
    )
    username = decoded_jwt.get("sub")
    if not username:
        raise Exception("Не валидный токен.")
    return username
