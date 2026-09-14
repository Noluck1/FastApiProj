import asyncio
from typing import Annotated
from datetime import datetime
from backend.shared.dtos.pagination_dto import PaginatedDto
from fastapi import APIRouter, Depends, Query
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from backend.app_books.books.api.dto.book.book_dto import SBooksAdd, SBooksUpdate, SPutBookUpdate
from backend.shared.responses.api_response import success
from backend.shared.responses.api_response_schema import ApiResponseSchema
from backend.app_books.books.api.dto.book.book_dto import BooksDto
from backend.app_books.books.shared.dto.book_list import BookListFilters, BookListSortBy, SortOrder
from backend.app_books.books.application.handlers.books.command.create_book import CreateBookCommand, CreateBookHandler
from backend.app_books.books.application.handlers.books.command.delete_book import DeleteBookCommand, DeleteBookHandler
from backend.app_books.books.application.handlers.books.command.put_update_book import PutUpdateBookCommand, PutUpdateBookHandler
from backend.app_books.books.application.handlers.books.command.patch_update_book import PatchUpdateBookCommand, PatchUpdateBookHandler
from backend.app_books.books.application.handlers.books.queries.get_books import GetBooksQuery, GetBooksHandler
from backend.app_books.books.application.handlers.books.queries.get_book_id import GetBookIdQuery, GetBookIdHandler
from backend.app_books.books.application.ports.outbound.i_identity_gateway import IIdentityGateway
from backend.shared.auth.principal import Principal
from backend.app_books.books.api.security.dependencies import (
    require_roles,
)
from backend.app_books.books.domain.access.book_access_subject import BookAccessSubject
from backend.app_books.books.infrastructure.persistence.mappers.book.book_mapper import book_to_dto


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
    
    result = await handler.handle(
        CreateBookCommand(
            title=book.title,
            description=book.description, 
            author_id=principal.subject_id
        )
    )

    return success(data=book_to_dto(result), message="Book created successfully")

 
@router.get("")
async def get_books(
    handler: FromDishka[GetBooksHandler],
    identity_gateway: FromDishka[IIdentityGateway],
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

    author_ids = {book.author_id for book in result.item}
    authors = await asyncio.gather(
        *(identity_gateway.get_user(author_id) for author_id in author_ids)
    )
    authors_by_id = {
        author.user_id: author
        for author in authors
        if author is not None
    }

    response = PaginatedDto[BooksDto](
        item=[
            book_to_dto(
                book,
                author_username=(
                    authors_by_id[book.author_id].username
                    if book.author_id in authors_by_id
                    else None
                ),
                author_full_name=(
                    authors_by_id[book.author_id].full_name
                    if book.author_id in authors_by_id
                    else None
                ),
            )
            for book in result.item
        ],
        page=result.page,
        page_size=result.page_size,
        total=result.total,
        total_pages=result.total_pages,
    )

    return success(data=response, message="Books retrieved successfully")

@router.get("/created-by-me")
async def get_created_by_my(
    handler: FromDishka[GetBooksHandler],
    identity_gateway: FromDishka[IIdentityGateway],
    principal: Annotated[
        Principal,
        Depends(require_roles("author", "admin"))
    ],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    title_contains: str | None = None,
    is_deleted: bool | None = None,
    include_deleted: bool = False,
    sort_by: BookListSortBy = "id",
    sort_order: SortOrder = "asc",
) -> ApiResponseSchema[PaginatedDto[BooksDto]]:
    result = await handler.handle(
        GetBooksQuery(
            page=page,
            page_size=page_size,
            filters=BookListFilters(
                author_id=principal.subject_id,
                title_contains=title_contains,
                is_deleted=is_deleted,
                include_deleted=include_deleted,
            ),
            sort_by=sort_by,
            sort_order=sort_order,
        )
    )

    author = await identity_gateway.get_user(
        principal.subject_id
    )

    response = PaginatedDto[BooksDto](
        item=[
            book_to_dto(
                book,
                author_username=(
                    author.username
                    if author is not None
                    else None
                ),
                author_full_name=(
                    author.full_name
                    if author is not None
                    else None
                ),
            )
            for book in result.item
        ],
        page=result.page,
        page_size=result.page_size,
        total=result.total,
        total_pages=result.total_pages,
    )

    return success(
        data=response,
        message="Created books retrieved successfully",
    )

@router.get("/{book_id}")
async def get_book_id(
    book_id: int,
    handler: FromDishka[GetBookIdHandler]
) -> ApiResponseSchema[BooksDto]:
    
    result = await handler.handle(GetBookIdQuery(book_id))

    return success(data=book_to_dto(result), message="Book retrieved successfully")
    

@router.put("/{book_id}")
async def put_update_book(
    book_id: int, 
    book: SPutBookUpdate,
    handler: FromDishka[PutUpdateBookHandler],
    principal: Annotated[
        Principal,
        Depends(require_roles("author", "admin")),
    ],
) -> ApiResponseSchema[BooksDto]:

    author = BookAccessSubject(
                user_id=principal.subject_id,
                roles=principal.roles,
            )
    
    result = await handler.handle(
        PutUpdateBookCommand(
            book_id, 
            title=book.title,
            description=book.description, 
            author=author,
        )
    )

    return success(data=book_to_dto(result), message="Book updated successfully")

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

    result = await handler.handle(
        PatchUpdateBookCommand(
            book_id=book_id, 
            title=book.title,
            description=book.description,
            changed_fields=frozenset(book.model_fields_set),
            author=author,
        )
    )

    return success(data=book_to_dto(result), message="Book updated successfully")

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

    return success(data=book_to_dto(result), message="Book deleted successfully")
