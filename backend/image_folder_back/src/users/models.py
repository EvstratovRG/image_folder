import uuid

from application.db.base_class import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Boolean, UniqueConstraint


class User(Base):
    __tablename__ = "users_user"  # type: ignore

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    code_phrase: Mapped[str] = mapped_column(String(100), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (UniqueConstraint("username", "email"),)
