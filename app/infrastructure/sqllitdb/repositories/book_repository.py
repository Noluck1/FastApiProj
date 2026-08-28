from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from sqlalchemy import select, delete, func
from app.infrastructure.sqllitdb.models import BooksOrm
from app.shared.dtos.book_dto import SBooksAdd, SBooksUpdate, SPutBookUpdate, BooksDto
from app.application.exceptions import NotFoundError
from app.application.repositories.i_book_repository import IBookRepository
from app.application.queries.book_list import BookListFilters, BookListSortBy, SortOrder
from app.shared.dtos.auth_dto import UserDto
from app.shared.enums.user_role import UserRole
from app.auth.auth_exceptions import BookAccessDeniedError

class BookRepository(IBookRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_book(self, book: SBooksAdd, author_id: int,) -> BooksDto:
        new_book = BooksOrm(
            title=book.title,
            description=book.description,
            author_id=author_id,
        )

        self.session.add(new_book)
        await self.session.flush()

        return BooksDto.model_validate(new_book)


    async def get_books(
            self, 
            page: int, 
            page_size: int,
            filters: BookListFilters,
            sort_by: BookListSortBy,
            sort_order: SortOrder,
    ) -> tuple[list[BooksDto], int]:
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

        return ([BooksDto.model_validate(book) for book in books], total)


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
       


    async def put_update_book(self, book_id: int, book: SPutBookUpdate, updated_by_id: int) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)

        data = book.model_dump()

        for key, value in data.items():
            setattr(book_model, key, value)

        book_model.updated_by_id = updated_by_id

        await self.session.flush()
        await self.session.refresh(book_model)


        return BooksDto.model_validate(book_model)

    async def patch_update_book(self, book_id: int, book: SBooksUpdate, updated_by_id: int) -> BooksDto:
            book_model = await self._get_model_by_id(book_id)
    
            data = book.model_dump(exclude_unset=True)
    
            for key, value in data.items():
                setattr(book_model, key, value)
    
            book_model.updated_by_id = updated_by_id
    
            await self.session.flush()
            await self.session.refresh(book_model)
    
            return BooksDto.model_validate(book_model)

    async def delete_book(self, book_id: int, updated_by_id: int) -> BooksDto:
        book_model = await self._get_model_by_id(book_id)

        book_model.updated_by_id = updated_by_id
        book_model.is_deleted = True
        book_model.deleted_at = datetime.now(timezone.utc)

        await self.session.flush()
        await self.session.refresh(book_model)

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

    def ensure_can_manage(self, user: UserDto, book: BooksDto) -> None:
            
        if user.role == UserRole.ADMIN or (user.role == UserRole.AUTHOR and book.author_id == user.id):
            return

        raise BookAccessDeniedError(
            user_id=user.id,
            book_id=book.id,
        )