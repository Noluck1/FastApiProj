from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.infrastructure.persistence.sqlalchemy.base import Model
from sqlalchemy import ForeignKey, DateTime, func, String
from app.books.infrastructure.persistence.mixins.mixin import SoftDeleteMixin


class BooksOrm(Model, SoftDeleteMixin):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100))

    description: Mapped[str | None] = mapped_column(String(255))

    author_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True
    )

    updated_by_id: Mapped[int | None] =  mapped_column(
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    favorite_entries: Mapped[list["FavoriteBookOrm"]] = relationship(
            back_populates="book",
            cascade="all, delete-orphan",
            lazy="selectin",
        )
    