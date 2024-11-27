from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from src.application import settings

from .consts import TEST_DATABASE

main_database_uri = PostgresDsn.build(
    scheme="postgresql",
    username=settings.PG_USER,
    password=settings.PG_PASSWORD,
    port=int(settings.PG_PORT),
    host=settings.PG_HOST,
    path="postgres",
)

test_database_uri = PostgresDsn.build(
    scheme="postgresql",
    username=settings.PG_USER,
    password=settings.PG_PASSWORD,
    port=int(settings.PG_PORT),
    host=settings.PG_HOST,
    path=TEST_DATABASE,
)


main_engine = create_engine(
    str(main_database_uri),
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=settings.POOL_RECYCLE,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_pre_ping=True,
)


test_engine = create_engine(
    str(test_database_uri),
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=settings.POOL_RECYCLE,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_pre_ping=True,
)


def init() -> None:
    with main_engine.connect() as connection:
        cursor = connection.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DATABASE}'")
        )
        if not cursor.scalar():
            connection.commit()
            connection.execution_options(
                isolation_level="AUTOCOMMIT",
            ).execute(
                text(
                    f"CREATE DATABASE {TEST_DATABASE} WITH TEMPLATE {settings.PG_DB} OWNER {settings.PG_USER};"
                ),
            )
            cursor.close()

    with test_engine.connect() as connection:
        connection.execute(
            text("TRUNCATE users_user CASCADE;"),
        )
        connection.commit()


def main() -> None:
    settings.logger.info("Initializing service")
    init()
    settings.logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
