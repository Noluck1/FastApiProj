from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.sqllitdb.base import Model
from sqlalchemy import ForeignKey, String

class BooksOrm(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    author: Mapped["UserOrm"] = relationship(
        back_populates="books",
        lazy="selectin"
    )
    