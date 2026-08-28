from dataclasses import dataclass
from app.application.queries.book_list import BookListFilters, BookListSortBy, SortOrder
from app.application.handlers.i_handler import IHandler
from app.shared.dtos.book_dto import BooksDto
from app.shared.dtos.pagination_dto import PaginatedDto
from app.application.repositories.i_book_repository import IBookRepository



@dataclass(frozen=True)
class GetBooksQuery:
    page: int
    page_size: int
    filters: BookListFilters
    sort_by: BookListSortBy
    sort_order: SortOrder


class GetBooksHandler(IHandler[GetBooksQuery, PaginatedDto[BooksDto]]):
    def __init__(self, repository: IBookRepository):
        self._repository = repository


    async def handle(self, request: GetBooksQuery) -> PaginatedDto[BooksDto]:
        books, total = await self._repository.get_books(
            page=request.page,
            page_size=request.page_size,
            filters=request.filters,
            sort_by=request.sort_by,
            sort_order=request.sort_order,
        )

        total_pages = (total + request.page_size - 1) // request.page_size

        return PaginatedDto[BooksDto](
            item=books,
            page=request.page,
            page_size=request.page_size,
            total=total,
            total_pages=total_pages
        )