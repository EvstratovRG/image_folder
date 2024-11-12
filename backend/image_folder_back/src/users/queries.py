from typing import Any

from application.types import UUID_TYPE
from .models import User
from sqlalchemy import Select, select, insert, Insert


def get_list_users_query() -> Select:
    return select(User)


def get_detail_user_query(user_id: UUID_TYPE) -> Select:
    return select(User).where(User.id == user_id)


def create_user_query(data: dict[str, Any]) -> Insert:
    return insert(User).values(**data).returning(User.id)
