from app.infrastructure.sqllitdb.base import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class FavoriteBookOrm(Model):
    __tablename__ = "favorite_book"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    user: Mapped["UserOrm"] = relationship(
        back_populates="favorite_entries"
    )

    book: Mapped["BooksOrm"] = relationship(
        back_populates="favorite_entries",
        lazy="selectin",
    )
