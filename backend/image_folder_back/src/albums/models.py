import uuid
from datetime import datetime

from application.db.base_class import Base

from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import String, DateTime, ForeignKey, Index, UniqueConstraint

from users.models import User
from utils.datetime import get_utc_now


class AlbumCategory(Base):
    __tablename__ = "albums_album_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users_user.id", ondelete="CASCADE"),
    )

    author: Mapped["User"] = relationship("User", backref="album_categories")
    albums: Mapped[list["Album"]] = relationship(
        "Album",
        back_populates="category",
    )

    __table_args__ = (UniqueConstraint("author_id", "title"),)


class Album(Base):
    __tablename__ = "albums_album"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users_user.id", ondelete="CASCADE"),
    )
    cover_id: Mapped[int | None] = mapped_column(
        ForeignKey("albums_image.id", ondelete="SET NULL"),
        nullable=True,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("albums_album_category.id", ondelete="SET NULL"),
        nullable=True,
    )
    content_type: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=get_utc_now,
        nullable=True,
    )

    author: Mapped["User"] = relationship("User", backref="albums")
    category: Mapped["AlbumCategory"] = relationship(
        "AlbumCategory",
    )
    images: Mapped[list["Image"]] = relationship(
        "Image",
        back_populates="album",
        cascade="delete",
        uselist=True,
        foreign_keys="Image.album_id",
    )
    videos: Mapped[list["Video"]] = relationship(
        "Video",
        back_populates="album",
        cascade="delete",
        uselist=True,
        foreign_keys="Video.album_id",
    )
    cover_image: Mapped["Image"] = relationship("Image", foreign_keys=[cover_id])

    __table_args__ = (
        Index("ix_album_category", "category_id"),
        Index("ix_album_author", "author_id"),
    )


class Image(Base):
    __tablename__ = "albums_image"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users_user.id", ondelete="CASCADE"),
    )
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums_album.id", ondelete="CASCADE")
    )

    album: Mapped["Album"] = relationship(
        "Album", back_populates="images", foreign_keys=[album_id]
    )


class Video(Base):
    __tablename__ = "albums_video"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users_user.id", ondelete="CASCADE"),
    )
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums_album.id", ondelete="CASCADE")
    )

    album: Mapped["Album"] = relationship(
        "Album", back_populates="videos", foreign_keys=[album_id]
    )


class AlbumImagePosition(Base):
    __tablename__ = "albums_album_image_position"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums_album.id", ondelete="CASCADE"),
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("albums_image.id", ondelete="CASCADE"),
    )
    video_id: Mapped[int] = mapped_column(
        ForeignKey("albums_video.id", ondelete="CASCADE"),
    )

    position: Mapped[int | None] = mapped_column(nullable=True)

    album: Mapped["Album"] = relationship("Album", backref="image_positions")
    image: Mapped["Image"] = relationship("Image", backref="album_positions")
