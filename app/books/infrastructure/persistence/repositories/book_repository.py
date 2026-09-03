from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from sqlalchemy import select, delete, func
from app.books.infrastructure.persistence.models.book_model import BooksOrm
from app.books.api.dto.book_dto import SBooksAdd, SBooksUpdate, SPutBookUpdate, BooksDto
from app.books.application.exceptions import NotFoundError
from app.books.application.ports.i_book_repository import IBookRepository
from app.shared.dtos.book_list import BookListFilters, BookListSortBy, SortOrder
from app.books.domain.entities.book import Book
from app.books.infrastructure.persistence.mappers.book_mapper import book_to_domain, book_to_orm, apply_book_to_orm


class BookRepository(IBookRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_book(self, book: Book) -> Book:

        if book.id is not None:
            raise ValueError("New book must not have an id")

        model = book_to_orm(book)
        
        self.session.add(model)

        await self.session.flush()
        await self.session.refresh(model)

        return book_to_domain(model)


    async def get_books(
            self, 
            page: int, 
            page_size: int,
            filters: BookListFilters,
            sort_by: BookListSortBy,
            sort_order: SortOrder,
    ) -> tuple[list[Book], int]:
        where_clauses = []

        if filters.id is not None:
            where_clauses.append(BooksOrm.id == filters.id)

        if filters.title is not None:
            where_clauses.append(BooksOrm.title == filters.title)

        if filters.title_contains is not None:
            where_clauses.append(
                BooksOrm.title.ilike(
                    f"%{filters.title_contains}%"
                )
            )

        if filters.created_from is not None:
            where_clauses.append(BooksOrm.created_at >= filters.created_from)

        if filters.created_to is not None:
            where_clauses.append(BooksOrm.created_at <= filters.created_to)

        if filters.updated_from is not None:
            where_clauses.append(BooksOrm.updated_at >= filters.updated_from)

        if filters.updated_to is not None:
            where_clauses.append(BooksOrm.updated_at <= filters.updated_to)

        if filters.is_deleted is not None:
            where_clauses.append(BooksOrm.is_deleted.is_(filters.is_deleted))

        elif not filters.include_deleted:
            where_clauses.append(BooksOrm.is_deleted.is_(False))

        sort_column = {
            "id": BooksOrm.id,
            "created_at": BooksOrm.created_at,
            "updated_at": BooksOrm.updated_at
        }[sort_by]

        order_by = sort_column.desc() if sort_order == "desc" else sort_column.asc()

        count_stmt = select(func.count(BooksOrm.id)).where(*where_clauses)
        total = await self.session.scalar(count_stmt)       

        book_result = await self.session.execute(
            select(BooksOrm)
            .where(*where_clauses)
            .order_by(order_by)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        books = book_result.scalars().all()

        return ([book_to_domain(book) for book in books], int(total or 0))


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



    async def get_book_id(self, book_id: int) -> Book:
        book_model = await self._get_model_by_id(book_id)
        return book_to_domain(book_model)
       

    async def purge_deleted_before(self, cutoff: datetime) -> int:
        statement = delete(BooksOrm).where(
            BooksOrm.is_deleted.is_(True),
            BooksOrm.deleted_at.is_not(None),
            BooksOrm.deleted_at <= cutoff,
        )


        result = await self.session.execute(statement)
        await self.session.flush()

        return result.rowcount or 0

    async def save(self, book: Book) -> Book:
        book_id = book.require_id()

        model = await self.session.get(BooksOrm, book_id)

        if model is None:
            raise NotFoundError(id=book_id)

        apply_book_to_orm(book, model)

        await self.session.flush()
        await self.session.refresh(model)

        return book_to_domain(model)