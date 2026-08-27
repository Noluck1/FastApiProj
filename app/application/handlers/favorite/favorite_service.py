from app.application.repositories.i_favorite_repository import IFavoriteRepository
from app.application.i_unit_of_work import IUnitOfWork
from app.shared.dtos.auth_dto import UserDto
from app.shared.dtos.favorite_dto import FavoriteDto
from app.application.repositories.i_book_repository import IBookRepository
from app.shared.dtos.book_dto import BooksDto
from app.shared.dtos.pagination_dto import PaginatedDto
from app.application.queries.book_list import BookListFilters, BookListSortBy, SortOrder

class FavoriteService:

    def __init__(
        self,
        repository: IFavoriteRepository,
        book_repository: IBookRepository,
        uow: IUnitOfWork,
    ) -> None:
        self._repository = repository
        self._book_repository = book_repository
        self._uow = uow
        

    async def add_favorite_book(
            self,
            book_id: int,
            current_user: UserDto,
    ) -> FavoriteDto:
        async with self._uow:
            await self._book_repository.get_book_id(book_id)

            add_favorite = await self._repository.add_favorite_book(
                book_id,
                user_id=current_user.id, 
            )
            await self._uow.commit()

        return add_favorite
        

    async def get_favorite_books(
            self,
            *,
            current_user: UserDto,
            page: int,
            page_size: int,
            filters: BookListFilters,
            sort_by: BookListSortBy,
            sort_order: SortOrder,
    ) -> PaginatedDto[BooksDto]:
        async with self._uow:
            books, total = (
                await self._repository.get_favorite_book(
                    user_id=current_user.id,
                    page=page,
                    page_size=page_size,
                    filters=filters,
                    sort_by=sort_by,
                    sort_order=sort_order,
                )
            )

        total_pages = (total + page_size - 1) // page_size


        return PaginatedDto[BooksDto](
            item=books,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )
        

    async def delete_favorite_book(
            self,
            book_id: int,
            current_user: UserDto,
    ) -> FavoriteDto:
        async with self._uow:
            deleted_favorite = await self._repository.delete_favorite_book(
                book_id=book_id, 
                user_id=current_user.id
            )

            await self._uow.commit()

            return deleted_favorite