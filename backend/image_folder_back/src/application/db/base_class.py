from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm import declared_attr


class Base(DeclarativeBase):
    __name__: str  # type: ignore

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
