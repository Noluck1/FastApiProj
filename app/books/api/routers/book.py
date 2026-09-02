from typing import Annotated
from datetime import datetime
from app.shared.dtos.pagination_dto import PaginatedDto
from fastapi import APIRouter, Depends, Query
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from app.shared.dtos.book_dto import SBooksAdd, SBooksUpdate, SPutBookUpdate
from app.shared.responses.api_response import success
from app.shared.responses.api_response_schema import ApiResponseSchema
from app.shared.dtos.book_dto import BooksDto
from app.shared.dtos.book_list import BookListFilters, BookListSortBy, SortOrder
from app.books.application.handlers.command.create_book import CreateBookCommand, CreateBookHandler
from app.books.application.handlers.command.delete_book import DeleteBookCommand, DeleteBookHandler
from app.books.application.handlers.command.put_update_book import PutUppdateBookCommand, PutUppdateBookHandler
from app.books.application.handlers.command.patch_update_book import PatchUpdateBookCommand, PatchUpdateBookHandler
from app.books.application.handlers.queries.get_books import GetBooksQuery, GetBooksHandler
from app.books.application.handlers.queries.get_book_id import GetBookIdQuery, GetBookIdHandler
from app.shared.auth.principal import Principal
from app.api.security.dependencies import require_roles
from app.books.domain.access.book_access_subject import BookAccessSubject


router = APIRouter(
    prefix="/books",
    tags=["Книги"],
    route_class=DishkaRoute
)

@router.post("")
async def add_book(
    book: SBooksAdd,
    handler: FromDishka[CreateBookHandler],
    principal: Annotated[
        Principal,
        Depends(require_roles("author", "admin")),
    ],
) -> ApiResponseSchema[BooksDto]:
    
    result = await handler.handle(CreateBookCommand(book, author_id=principal.subject_id))

    return success(data=result, message="Book created successfully")

 
@router.get("")
async def get_books(
    handler: FromDishka[GetBooksHandler],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    book_id: Annotated[int | None, Query(ge=1)] = None,
    title: str | None = None,
    title_contains: str | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    updated_from: datetime | None = None,
    updated_to: datetime | None = None,
    is_deleted: bool | None = None,
    include_deleted: bool = False,
    sort_by: BookListSortBy = "id",
    sort_order: SortOrder = "asc",
) -> ApiResponseSchema[PaginatedDto[BooksDto]]:
    
    result = await handler.handle(
        GetBooksQuery(
            page=page,
            page_size=page_size,
            filters = BookListFilters(
                    id=book_id,
                    title=title,
                    title_contains=title_contains,
                    created_from=created_from,
                    created_to=created_to,
                    updated_from=updated_from,
                    updated_to=updated_to,
                    is_deleted=is_deleted,
                    include_deleted=include_deleted,
                ),
            sort_by=sort_by,
            sort_order=sort_order,
        ),
    )

    return success(data=result, message="Books retrieved successfully")

@router.get("/{book_id}")
async def get_book_id(
    book_id: int,
    handler: FromDishka[GetBookIdHandler]
) -> ApiResponseSchema[BooksDto]:
    
    result = await handler.handle(GetBookIdQuery(book_id))

    return success(data=result, message="Book retrieved successfully")
    

@router.put("/{book_id}")
async def put_update_book(
    book_id: int, 
    book: SPutBookUpdate,
    handler: FromDishka[PutUppdateBookHandler],
    principal: Annotated[
        Principal,
        Depends(require_roles("author", "admin")),
    ],
) -> ApiResponseSchema[BooksDto]:

    author = BookAccessSubject(
                user_id=principal.subject_id,
                roles=principal.roles,
            )
    
    result = await handler.handle(PutUppdateBookCommand(book_id, book, author=author))

    return success(data=result, message="Book updated successfully")

@router.patch("/{book_id}")
async def patch_update_book(
    book_id: int,
    book: SBooksUpdate,
    handler: FromDishka[PatchUpdateBookHandler],
    principal: Annotated[
        Principal,
        Depends(require_roles("author", "admin")),
    ],
) -> ApiResponseSchema[BooksDto]:

    author = BookAccessSubject(
            user_id=principal.subject_id,
            roles=principal.roles,
        )

    result = await handler.handle(PatchUpdateBookCommand(book_id, book, author=author))

    return success(data=result, message="Book updated successfully")

@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    handler: FromDishka[DeleteBookHandler],
    principal: Annotated[
        Principal,
        Depends(require_roles("author", "admin")),
    ],
) -> ApiResponseSchema[BooksDto]:

    author = BookAccessSubject(
        user_id=principal.subject_id,
        roles=principal.roles,
    )
    
    result = await handler.handle(DeleteBookCommand(book_id, author=author))

    return success(data=result, message="Book deleted successfully")