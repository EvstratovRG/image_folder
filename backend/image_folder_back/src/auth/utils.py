from datetime import datetime, timedelta
from typing import Any

from application.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY,
)

from passlib.context import CryptContext
from jose import jwt, JWTError

from .enums import TokenTypesEnum
from .exceptions import TokenDecodeError

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_data(data: str) -> str:
    return context.hash(data)


def verify_hash(data: str, hashed_data: str) -> bool:
    return context.verify(data, hashed_data)


def hash_user_data(password: str, code_phrase: str | None = None) -> dict[str, Any]:
    hashed_pass = get_hashed_data(password)
    hashed_data = {"password": hashed_pass}
    if code_phrase:
        hashed_code_phrase = get_hashed_data(code_phrase)
        hashed_data["code_phrase"] = hashed_code_phrase
    return hashed_data


def create_token(
    token_type: TokenTypesEnum,
    subject: str,
) -> str:
    expires_delta = datetime.utcnow() + timedelta(
        minutes=int(
            ACCESS_TOKEN_EXPIRE_MINUTES
            if token_type.name == TokenTypesEnum.access
            else REFRESH_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode = {"exp": expires_delta, "sub": subject}
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
    try:
        decoded_jwt = jwt.decode(
            token,
            JWT_REFRESH_SECRET_KEY if token_type.refresh else JWT_SECRET_KEY,
            ALGORITHM,
        )
    except JWTError as e:
        raise TokenDecodeError(e)
    return decoded_jwt.get("sub")
