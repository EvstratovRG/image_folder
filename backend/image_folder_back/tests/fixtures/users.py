import pytest_asyncio

from auth.utils import hash_user_data
from ..utils import generate_random_string, generate_random_valid_password


@pytest_asyncio.fixture()
async def create_user(async_session):
    from users.models import User

    async def _create_user(**custom_data) -> User:
        custom_password = custom_data.pop("password", None)
        custom_code_phrase = custom_data.pop("code_phrase", None)

        password_to_hash = custom_password or generate_random_valid_password(5)
        code_phrase_to_hash = custom_code_phrase or generate_random_string(5)

        hashed_data = hash_user_data(
            password_to_hash,
            code_phrase_to_hash,
        )
        hashed_password, hashed_code_phrase = (
            hashed_data.get("password"),
            hashed_data.get("code_phrase"),
        )

        data = {
            "username": generate_random_string(5),
            "firstname": generate_random_string(5),
            "lastname": generate_random_string(5),
            "email": generate_random_string(5) + "@mail.ru",
            "password": hashed_password,
            "code_phrase": hashed_code_phrase,
        }

        data.update(custom_data)
        user = User(**data)
        async_session.add(user)
        await async_session.flush()
        return user

    return _create_user
