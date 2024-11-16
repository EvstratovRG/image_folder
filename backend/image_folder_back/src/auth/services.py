from .queries import get_user_by_username_query
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from .utils import decode_data_from_token


async def get_user_by_username(db_session: AsyncSession, username: str) -> User | None:
    query = get_user_by_username_query(username=username)
    cursor = await db_session.execute(query)
    return cursor.scalar_one_or_none()


async def get_user_by_token(
    db_session: AsyncSession,
    token: str,
) -> User | None:
    token = token.replace("Bearer ", "")
    username = decode_data_from_token(token=token)
    query = get_user_by_username_query(username=username)
    cursor = await db_session.execute(query)
    return cursor.scalar_one_or_none()
