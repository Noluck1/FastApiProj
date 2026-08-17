from app.books.models import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AuthorOrm(Model):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] | None
    last_name: Mapped[str] | None

    books = relationship("book")


