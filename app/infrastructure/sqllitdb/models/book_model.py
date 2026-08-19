from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.sqllitdb.base import Model

class BooksOrm(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    