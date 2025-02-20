from users.repositories import UserRepository
from base.repository import BaseRepository
from users.models import User


async def test_user_repository(async_session):
    repo = UserRepository(async_session)

    assert await repo.get_by_unique_params() is None


async def test_base_update_repo(async_session, create_user):
    user = await create_user()
    username_before_update = user.username
    email_before_update = user.email
    data = {"username": "qweqwe", "email": "qweqwe.mail.ru"}
    repo = BaseRepository(async_session, User)

    updated_user = await repo.update(user.id, data)

    assert updated_user.username != username_before_update
    assert updated_user.email != email_before_update
