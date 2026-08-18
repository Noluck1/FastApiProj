from fastapi import APIRouter, Depends
from app.books.service import BookService
from app.books.schemas import SBooksAdd, SBookId, SBooks, SBooksUpdate

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)

@router.post("")
async def add_book(book: SBooksAdd = Depends()) -> SBookId:
    new_book = await BookService().add_book(book)
    return {"id": new_book}

@router.get("")
async def get_books():
    books = await BookService().get_books()
    return books

@router.get("/{book_id}")
async def get_book_id(book_id: int):
    book = await BookService().get_book_id(book_id)
    return book
    

@router.put("/{book_id}")
async def update_book(book_id: int, book: SBooksUpdate = Depends()) -> SBooks:
    book = await BookService().update_book(book_id, book)
    return book

@router.delete("/{book_id}")
async def delete_book(book_id: int):
    await BookService().delete_book(book_id)
    return None