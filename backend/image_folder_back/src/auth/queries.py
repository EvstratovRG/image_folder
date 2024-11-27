from sqlalchemy import select, Select
from users.models import User


def get_user_by_username_query(username: str) -> Select:
    return select(User).where(User.username == username)
