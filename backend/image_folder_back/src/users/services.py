from typing import Any

from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from application.types import UUID_TYPE
from users.models import User
from users.queries import (
    get_detail_user_query,
    get_list_users_query,
    create_user_query,
)


async def get_users_service(db_session: AsyncSession) -> Sequence:
    query = get_list_users_query()
    cursor = await db_session.execute(query)
    return cursor.scalars().all()


async def create_user_service(data: dict[str, Any], db_session: AsyncSession) -> User:
    query = create_user_query(data)
    cursor = await db_session.execute(query)
    await db_session.commit()
    instance_id = cursor.scalars().one_or_none()
    return await get_detail_user_service(user_id=instance_id, db_session=db_session)


async def get_detail_user_service(user_id: UUID_TYPE, db_session: AsyncSession) -> User:
    query = get_detail_user_query(user_id)
    cursor = await db_session.execute(query)
    return cursor.scalars().one_or_none()


async def update_user_service(
    user_id: UUID_TYPE, data: [str, Any], db_session: AsyncSession
) -> User:
    user_to_update = await get_detail_user_service(user_id, db_session)
    filtered_data = {key: value for key, value in data.items() if value is not None}
    for key, value in filtered_data.items():
        setattr(user_to_update, key, value)
    await db_session.commit()
    return await get_detail_user_service(user_id, db_session)


async def get_me_service(
    db_session: AsyncSession,
):  # TODO: будет добавлено после авторизации
    # query = get_detail_user_query()
    # cursor = ...
    return ...
