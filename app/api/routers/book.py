from fastapi import APIRouter, Depends
from app.books.service import BookService
from app.shared.dtos.book_dto import SBooksAdd, SBookId, SBooks, SBooksUpdate
from app.shared.responses.api_response import success
from app.shared.responses.api_response_schema import ApiResponseSchema

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)

@router.post("")
async def add_book(book: SBooksAdd = Depends()) -> ApiResponseSchema:
    new_book = await BookService().add_book(book)
    return success(data=new_book, message="Book created successfully")


# не работает пофиксить 
@router.get("")
async def get_books() -> ApiResponseSchema:
    books = await BookService().get_books()
    return success(data=books, message="Books retrieved successfully")

@router.get("/{book_id}")
async def get_book_id(book_id: int) -> ApiResponseSchema:
    book = await BookService().get_book_id(book_id)
    return success(data=book, message="Book retrieved successfully")
    

@router.put("/{book_id}")
async def update_book(book_id: int, book: SBooksUpdate = Depends()) -> ApiResponseSchema:
    book = await BookService().update_book(book_id, book)
    return success(data=book, message="Book deleted successfully")

@router.delete("/{book_id}")
async def delete_book(book_id: int) -> ApiResponseSchema:
    result = await BookService().delete_book(book_id)
    return success(data=result, message="Book deleted successfully")