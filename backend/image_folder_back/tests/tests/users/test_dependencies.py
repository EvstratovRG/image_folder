import uuid

import pytest
from fastapi.exceptions import HTTPException

from users.dependencies import get_user


async def test_get_user(async_session):
    random_user_id = uuid.uuid4()
    with pytest.raises(HTTPException):
        await get_user(random_user_id, async_session)
