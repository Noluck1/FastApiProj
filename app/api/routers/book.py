from typing import Annotated

from fastapi import APIRouter, Depends
from app.application.handlers.book.service import BookService
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from app.shared.enums.user_role import UserRole
from app.shared.dtos.auth_dto import UserDto
from app.shared.dtos.book_dto import SBooksAdd, SBooksUpdate
from app.shared.responses.api_response import success
from app.shared.responses.api_response_schema import ApiResponseSchema
from app.shared.dtos.book_dto import BooksDto
from app.auth.dependencies import get_current_user, require_roles


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
        Depends(require_roles(UserRole.AUTHOR)),
    ],
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.add_book(book, current_user=current_user)

    return success(data=result, message="Book created successfully")

 
@router.get("")
async def get_books(
    service: FromDishka[BookService]
) -> ApiResponseSchema[list[BooksDto]]:
    
    result = await service.get_books()

    return success(data=result, message="Books retrieved successfully")

@router.get("/{book_id}")
async def get_book_id(
    book_id: int,
    service: FromDishka[BookService]
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.get_book_id(book_id)

    return success(data=result, message="Book retrieved successfully")
    

@router.put("/{book_id}")
async def update_book(
    book_id: int, 
    book: SBooksUpdate,
    service: FromDishka[BookService],
    current_user: Annotated[
        UserDto,
        Depends(require_roles(UserRole.AUTHOR, UserRole.ADMIN)),
    ],
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.update_book(book_id, book, current_user=current_user)

    return success(data=result, message="Book deleted successfully")

@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    service: FromDishka[BookService],
    current_user: Annotated[
        UserDto,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> ApiResponseSchema[BooksDto]:
    
    result = await service.delete_book(book_id, current_user=current_user)

    return success(data=result, message="Book deleted successfully")