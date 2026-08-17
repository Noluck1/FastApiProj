from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey

class Model(DeclarativeBase):
    pass

class BooksOrm(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: mapped_column(ForeignKey('authors.id'))
    