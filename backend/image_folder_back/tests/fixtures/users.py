import pytest_asyncio
from ..utils import generate_random_string
from auth.hasher import Hasher


@pytest_asyncio.fixture()
async def create_user(async_session):
    from users.models import User

    async def _create_user(**castom_data) -> User:
        data = {
            "username": generate_random_string(5),
            "firstname": generate_random_string(5),
            "lastname": generate_random_string(5),
            "email": generate_random_string(5) + "@mail.ru",
            "password": Hasher.get_password_hash(generate_random_string(5)),
            "code_phrase": generate_random_string(5),
        }
        data.update(castom_data)
        user = User(**data)
        async_session.add(user)
        await async_session.flush()
        return user

    return _create_user
