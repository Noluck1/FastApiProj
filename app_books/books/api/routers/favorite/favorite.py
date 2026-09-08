from datetime import datetime
from fastapi import APIRouter, Depends, Query
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from shared.responses.api_response import success
from shared.responses.api_response_schema import ApiResponseSchema
from shared.dtos.favorite_dto import FavoriteDto
from typing import Annotated
from shared.dtos.pagination_dto import PaginatedDto
from app_books.books.api.dto.book.book_dto import BooksDto
from shared.dtos.book_list import BookListSortBy, SortOrder, BookListFilters
from app_books.books.application.handlers.favorite.command.add_favorite import AddFavoriteBookCommand, AddFavoriteBookHandler
from app_books.books.application.handlers.favorite.command.delete_favorite import DeleteFavoriteBookCommand, DeleteFavoriteBookHandler
from app_books.books.application.handlers.favorite.queries.get_favorite_books import GetFavoriteBooksQuery, GetFavoriteBooksHandle
from shared.auth.principal import Principal
from app_books.books.infrastructure.persistence.mappers.favorite.favorite_mapper import favorite_to_dto
from app_books.books.infrastructure.persistence.mappers.book.book_mapper import book_to_dto
from app_books.books.api.security.dependencies import (
    get_current_principal,
)
from app_books.books.domain.entities.book_entity.book import Book

router = APIRouter(
    prefix="/favorite",

    tags=["Избранное"],
    route_class=DishkaRoute
)


@router.post("/{book_id}")
async def add_favorite_book(
    book_id: int,
    handler: FromDishka[AddFavoriteBookHandler],
    principal: Annotated[
        Principal,
        Depends(get_current_principal),
    ],
) -> ApiResponseSchema[FavoriteDto]:
    result = await handler.handle(AddFavoriteBookCommand(book_id, user_id=principal.subject_id))

    return success(data=favorite_to_dto(result), message="Book add favorite")

@router.get("")
async def get_favorite_books(
    principal: Annotated[
        Principal,
        Depends(get_current_principal),
    ],
    handler: FromDishka[GetFavoriteBooksHandle],
    page: Annotated[int, Query(ge=1)]= 1,
    page_size: Annotated[int, Query(ge=1, le=100)]= 20,
    book_id: Annotated[int | None, Query(ge=1)] = None,
    title: str | None = None,
    title_contains: str | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    updated_from: datetime | None = None,
    updated_to: datetime | None = None,
    sort_by: BookListSortBy = "id",
    sort_order: SortOrder = "asc",
) -> ApiResponseSchema[PaginatedDto[BooksDto]]:
    
    result = await handler.handle(
        GetFavoriteBooksQuery(
            user_id=principal.subject_id,
            page=page,
            page_size=page_size,
            filters = BookListFilters(
                    id=book_id,
                    title=title,
                    title_contains=title_contains,
                    created_from=created_from,
                    created_to=created_to,
                    updated_from=updated_from,
                    updated_to=updated_to
                ),
            sort_by=sort_by,
            sort_order=sort_order,
        )
    )


    response = PaginatedDto[BooksDto](
        item=[book_to_dto(book) for book in result.item],
        page=result.page,
        page_size=result.page_size,
        total=result.total,
        total_pages=result.total_pages,
    )

    return success(
        data=response, 
        message="Favorite books retrieved successfully"
    )

@router.delete("/{book_id}")
async def delete_favorite_book(
    book_id: int,
    handler: FromDishka[DeleteFavoriteBookHandler],
    principal: Annotated[
        Principal,
        Depends(get_current_principal),
    ],
) -> ApiResponseSchema[FavoriteDto]:
    result = await handler.handle(DeleteFavoriteBookCommand(book_id, user_id=principal.subject_id))

    return success(data=favorite_to_dto(result), message="Book removed from favorites")