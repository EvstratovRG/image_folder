import os
from pathlib import Path

from dotenv import load_dotenv
from logging import getLogger

logger = getLogger()


def get_bool_env(env_name: str, default: bool) -> bool:
    return os.getenv(env_name, str(default)) in [1, "1", "True", "true"]


BASE_DIR = Path(__file__).parent.parent
env_file_path = BASE_DIR.parent / ".env"
load_dotenv(env_file_path)

SERVICE_NAME = os.getenv("SERVICE_NAME", "image_folder")
API_BASE_URL = os.getenv("API_BASE_URL", "/api/image_folder")

PG_DB = os.getenv("PG_DB", "image_folder")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5433")

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
DEBUG = get_bool_env("DEBUG", True)

MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", 100))
PAGE_SIZE = int(os.getenv("PAGE_SIZE", 10))

POOL_SIZE = int(os.getenv("POOL_SIZE", 600))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", 3600))
POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT", 100))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 100))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", ["*"])


ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "120")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "secret")
