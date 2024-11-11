from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncSession:
    return request.state.db
