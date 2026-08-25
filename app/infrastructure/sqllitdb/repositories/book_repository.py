from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from sqlalchemy import select, delete
from app.infrastructure.sqllitdb.models.book_model import BooksOrm
from app.shared.dtos.book_dto import SBooksAdd, SBooksUpdate, SBooks, BooksDto
from app.application.exceptions import NotFoundError
from app.application.repositories.i_book_repository import IBookRepository

class BookRepository(IBookRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_book(self, book: SBooksAdd, author_id: int,) -> BooksDto:
        new_book = BooksOrm(
            title=book.title,
            author_id=author_id,
        )

        self.session.add(new_book)
        await self.session.flush()

        return BooksDto.model_validate(new_book)


    async def get_books(self) -> list[BooksDto]:
        result = await self.session.execute(select(BooksOrm).where(BooksOrm.is_deleted.is_(False)))
        books = result.scalars().all()

        return [BooksDto.model_validate(book) for book in books]


    async def _get_model_by_id(self, book_id: int) -> BooksOrm:
        result = await self.session.execute(
            select(BooksOrm).where(
                BooksOrm.id == book_id,
                BooksOrm.is_deleted.is_(False)
            ))

        book_model = result.scalar_one_or_none()

        if book_model is None:
            raise NotFoundError(id=book_id)

        return book_model



    async def get_book_id(self, book_id: int) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)
        return BooksDto.model_validate(book_model)
       


    async def update_book(self, book_id: int, book: SBooksUpdate) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)

        data = book.model_dump(exclude_unset=True, exclude_none=True)

        for key, value in data.items():
            setattr(book_model, key, value)

        await self.session.flush()

        return BooksDto.model_validate(book_model)

    async def delete_book(self, book_id: int) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)

        book_model.is_deleted = True
        book_model.deleted_at = datetime.now(timezone.utc)

        await self.session.flush()

        return BooksDto.model_validate(book_model)

    async def purge_deleted_before(self, cutoff: datetime) -> int:
        statement = delete(BooksOrm).where(
            BooksOrm.is_deleted.is_(True),
            BooksOrm.deleted_at.is_not(None),
            BooksOrm.deleted_at <= cutoff,
        )


        result = await self.session.execute(statement)
        await self.session.flush()

        return result.rowcount or 0