from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine

from application import settings

from .consts import TEST_DATABASE

sqlalchemy_database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    username=settings.PG_USER,
    password=settings.PG_PASSWORD,
    port=int(settings.PG_PORT),
    host=settings.PG_HOST,
    path=TEST_DATABASE,
)

engine = create_async_engine(
    str(sqlalchemy_database_uri),
    echo=True,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=settings.POOL_RECYCLE,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_pre_ping=True,
)
