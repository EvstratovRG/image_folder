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

SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

PG_DB = os.getenv("PG_DB", "image_folder")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5433")
API_BASE_URL = os.getenv("API_BASE_URL", "/api/image_folder")

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
DEBUG = get_bool_env("DEBUG", True)
MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", 100))

POOL_SIZE = int(os.getenv("POOL_SIZE", 600))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", 3600))
POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT", 100))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 100))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", ["*"])
