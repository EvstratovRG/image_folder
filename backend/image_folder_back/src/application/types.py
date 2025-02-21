from typing import TypeVar
from uuid import UUID

from application.db.base_class import Base

UUID_TYPE = str | UUID

Model = TypeVar("Model", bound=Base)
