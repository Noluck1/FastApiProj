from typing import Annotated
from app.shared.dtos.pagination_dto import PaginatedDro
from fastapi import APIRouter, Depends, Query
from app.application.handlers.book.service import BookService
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from app.shared.enums.user_role import UserRole
from app.shared.dtos.auth_dto import UserDto
from app.shared.dtos.book_dto import SBooksAdd, SBooksUpdate, SPutBookUpdate
from app.shared.responses.api_response import success
from app.shared.responses.api_response_schema import ApiResponseSchema
from app.shared.dtos.book_dto import BooksDto
from app.auth.dependencies import get_current_user, require_roles
from app.application.queries.book_list import BookListFilters, BookListSortBy, SortOrder
from datetime import datetime

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
    route_class=DishkaRoute
)

@router.post("")
async def add_book(
    book: SBooksAdd,
    service: FromDishka[BookService],
    current_user: Annotated[
        UserDto,
        Depends(require_roles(UserRole.AUTHOR, UserRole.ADMIN)),
    ],
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.add_book(book, current_user=current_user)

    return success(data=result, message="Book created successfully")

 
@router.get("")
async def get_books(
    service: FromDishka[BookService],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    book_id: Annotated[int | None, Query(ge=1)] = None,
    title: str | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    updated_from: datetime | None = None,
    updated_to: datetime | None = None,
    is_deleted: bool | None = None,
    include_deleted: bool = False,
    sort_by: BookListSortBy = "id",
    sort_order: SortOrder = "asc",
) -> ApiResponseSchema[PaginatedDro[BooksDto]]:
    filters = BookListFilters(
        id=book_id,
        title=title,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        is_deleted=is_deleted,
        include_deleted=include_deleted,
    )
    
    result = await service.get_books(
        page=page,
        page_size=page_size,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return success(data=result, message="Books retrieved successfully")

@router.get("/{book_id}")
async def get_book_id(
    book_id: int,
    service: FromDishka[BookService]
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.get_book_id(book_id)

    return success(data=result, message="Book retrieved successfully")
    

@router.put("/{book_id}")
async def put_update_book(
    book_id: int, 
    book: SPutBookUpdate,
    service: FromDishka[BookService],
    current_user: Annotated[
        UserDto,
        Depends(require_roles(UserRole.AUTHOR, UserRole.ADMIN)),
    ],
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.put_update_book(book_id, book, current_user=current_user)

    return success(data=result, message="Book updated successfully")

@router.patch("/{book_id}")
async def patch_update_book(
    book_id: int,
    book: SBooksUpdate,
    service: FromDishka[BookService],
    current_user: Annotated[
        UserDto,
        Depends(require_roles(UserRole.AUTHOR, UserRole.ADMIN)),
    ],
) -> ApiResponseSchema[BooksDto]:

    result = await service.patch_update_book(book_id, book, current_user=current_user)

    return success(data=result, message="Book updated successfully")

@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    service: FromDishka[BookService],
    current_user: Annotated[
        UserDto,
        Depends(require_roles(UserRole.ADMIN, UserRole.AUTHOR)),
    ],
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.delete_book(book_id, current_user=current_user)

    return success(data=result, message="Book deleted successfully")