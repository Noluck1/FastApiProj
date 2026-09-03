from app.books.application.ports.favorite.i_favorite_repository import IFavoriteRepository
from app.books.infrastructure.persistence.models.favorite.favorite_books_model import FavoriteBookOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.books.application.exceptions import FavoriteNotFoundError
from app.books.infrastructure.persistence.models.book.book_model import BooksOrm
from app.shared.dtos.book_list import BookListSortBy, BookListFilters, SortOrder
from app.books.domain.entities.favorite_entity.favorite_book import FavoriteBook
from app.books.infrastructure.persistence.mappers.favorite.favorite_mapper import favorite_to_domain, favorite_to_orm
from app.books.domain.entities.book_entity.book import Book
from app.books.infrastructure.persistence.mappers.book.book_mapper import book_to_domain
from app.books.application.exceptions import FavoriteAlreadyExistsError

class FavoriteRepository(IFavoriteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def add_favorite_book(
        self, 
        favorite: FavoriteBook
    ) -> FavoriteBook:
        model = favorite_to_orm(favorite)
        self.session.add(model)

        try:
            await self.session.flush()
        except IntegrityError as exc:
            message = str(exc.orig)

            if(
                "UNIQUE constraint failed: "
                "favorite_book.user_id, favorite_book.book_id"
                not in message
            ):
                raise

            raise FavoriteAlreadyExistsError(
                user_id=favorite.user_id,
                book_id=favorite.book_id,
            ) from exc

        return favorite_to_domain(model)

    async def get_favorite_book(
        self,
        *,
        user_id: int,
        page: int,
        page_size: int,
        filters: BookListFilters,
        sort_by: BookListSortBy,
        sort_order: SortOrder,
    ) -> tuple[list[Book], int]:
        where_clauses = [
            FavoriteBookOrm.user_id == user_id,
            BooksOrm.is_deleted.is_(False)
        ]
        
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


        sort_column = {
            "id": BooksOrm.id,
            "created_at": BooksOrm.created_at,
            "updated_at": BooksOrm.updated_at
        }[sort_by]

        order_by = sort_column.desc() if sort_order == "desc" else sort_column.asc()
        
        count_stmt = (
            select(func.count(BooksOrm.id))
            .select_from(BooksOrm)
            .join(
                FavoriteBookOrm, 
                FavoriteBookOrm.book_id == BooksOrm.id
            )
            .where(*where_clauses)
        )

        total = await self.session.scalar(count_stmt) or 0

        result = await self.session.scalars(
            select(BooksOrm)
            .join(
                FavoriteBookOrm, 
                FavoriteBookOrm.book_id == BooksOrm.id
            )
            .where(*where_clauses)
            .order_by(order_by)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        books = result.all()
        
        return [book_to_domain(book) for book in books], total,

    async def delete_favorite_book(
        self,
        book_id: int,
        user_id: int,
    ) -> FavoriteBook:

        favorite = await self.session.get(
            FavoriteBookOrm, 
            {
                "user_id": user_id, 
                "book_id": book_id,
            },
        )

        if favorite is None:
            raise FavoriteNotFoundError(
                user_id=user_id,
                book_id=book_id,
            )

        deleted_favorite = favorite_to_domain(favorite)

        await self.session.delete(favorite)
        await self.session.flush()

        return deleted_favorite