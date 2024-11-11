from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from application import settings

sqlalchemy_database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    username=settings.PG_USER,
    password=settings.PG_PASSWORD,
    port=int(settings.PG_PORT),
    host=settings.PG_HOST,
    path=settings.PG_DB or '',
)

engine = create_async_engine(
    str(sqlalchemy_database_uri),
    echo=True,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=settings.POOL_RECYCLE,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_pre_ping=True,
    connect_args={
        "statement_cache_size": 0,
    },
)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
