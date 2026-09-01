from dataclasses import dataclass
from app.shared.dtos.book_list import BookListFilters, BookListSortBy, SortOrder
from app.application.handlers.i_handler import IHandler
from app.shared.dtos.book_dto import BooksDto
from app.shared.dtos.pagination_dto import PaginatedDto
from app.application.repositories.i_favorite_repository import IFavoriteRepository
from app.domain.auth.entities.user import User

@dataclass(frozen=True)
class GetFavoriteBooksQuery:
    current_user: User
    page: int
    page_size: int
    filters: BookListFilters
    sort_by: BookListSortBy
    sort_order: SortOrder


class GetFavoriteBooksHandle(IHandler[GetFavoriteBooksQuery, PaginatedDto[BooksDto]]):
    def __init__(self, repository: IFavoriteRepository):
        self._repository = repository


    async def handle(self, request: GetFavoriteBooksQuery) -> PaginatedDto[BooksDto]:
        user_id = request.current_user.require_id()

        books, total = (
            await self._repository.get_favorite_book(
                user_id=user_id,
                page=request.page,
                page_size=request.page_size,
                filters=request.filters,
                sort_by=request.sort_by,
                sort_order=request.sort_order,
            )
        )

        total_pages = (total + request.page_size - 1) // request.page_size

        return PaginatedDto[BooksDto](
            item=books,
            page=request.page,
            page_size=request.page_size,
            total=total,
            total_pages=total_pages,
        )
        