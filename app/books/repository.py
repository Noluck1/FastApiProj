from fastapi import HTTPException
from sqlalchemy import select
from app.books.models import BooksOrm
from app.database import SessionDep
from schemas import SBooksAdd, SBooks, SBooksUpdate


class BookRepository:
    @classmethod
    async def add_book(cls, book: SBooksAdd, session:SessionDep) -> int:
        data = book.model_dump()
        new_book = BooksOrm(**data)
        session.add(new_book)
        await session.flush()
        await session.commit()

        return new_book.id

    @classmethod
    async def get_book(cls, session:SessionDep) -> list[SBooks]:
        result = await session.execute(select(BooksOrm))
        book_models = result.scalars().all()
        books = [SBooks.model_validate(book_model) for book_model in book_models]

        return books

    @classmethod
    async def uppdate_book(cls, book_id: int, session:SessionDep, book: SBooksUpdate ):
        result = await session.execute(select(BooksOrm).where(BooksOrm.id == book_id))
        book_models = result.scalar_one_or_none()

        if book_models is None:
            raise HTTPException(status_code=404, detail="Book not found")

        data = book.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(book_models, key, value)

        await session.flush()
        await session.commit()

        return book_models

    @classmethod
    async def delete_book(cls, session:SessionDep, book_id: int):
        result = await session.execute(select(BooksOrm).where(BooksOrm.id == book_id))
        book_models = result.scalar_one_or_none()
        if book_models is None:
            raise HTTPException(status_code=404, detail="Book not found")

        await session.delete(book_models)
        await session.commit()

        return book_id