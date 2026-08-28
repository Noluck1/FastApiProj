from datetime import datetime
from fastapi import APIRouter, Depends, Query
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from app.shared.dtos.auth_dto import UserDto
from app.shared.responses.api_response import success
from app.shared.responses.api_response_schema import ApiResponseSchema
from app.shared.dtos.favorite_dto import FavoriteDto
from typing import Annotated
from app.auth.dependencies import get_current_user
from app.shared.dtos.pagination_dto import PaginatedDto
from app.shared.dtos.book_dto import BooksDto
from app.shared.dtos.book_list import BookListSortBy, SortOrder, BookListFilters
from app.application.handlers.favorite.command.add_favorite import AddFavoriteBookCommand, AddFavoriteBookHandler
from app.application.handlers.favorite.command.delete_favorite import DeleteFavoriteBookCommand, DeleteFavoriteBookHandler
from app.application.handlers.favorite.queries.get_favorite_books import GetFavoriteBooksQuery, GetFavoriteBooksHandle



router = APIRouter(
    prefix="/favorite",

    tags=["Избранное"],
    route_class=DishkaRoute
)


@router.post("/{book_id}")
async def add_favorite_book(
    book_id: int,
    handler: FromDishka[AddFavoriteBookHandler],
    current_user: Annotated[
        UserDto,
        Depends(get_current_user),
    ],
) -> ApiResponseSchema[FavoriteDto]:
    result = await handler.handle(AddFavoriteBookCommand(book_id, current_user=current_user))

    return success(data=result, message="Book add favorite")

@router.get("")
async def get_favorite_books(
    current_user: Annotated[
            UserDto,
            Depends(get_current_user),
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
            current_user=current_user,
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

    return success(
        data=result, 
        message="Favorite books retrieved successfully"
    )

@router.delete("/{book_id}")
async def delete_favorite_book(
    book_id: int,
    handler: FromDishka[DeleteFavoriteBookHandler],
    current_user: Annotated[
            UserDto,
            Depends(get_current_user),
        ],
) -> ApiResponseSchema[FavoriteDto]:
    result = await handler.handle(DeleteFavoriteBookCommand(book_id, current_user=current_user))

    return success(data=result, message="Book removed from favorites")