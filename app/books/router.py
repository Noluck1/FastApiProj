from fastapi import APIRouter, Depends
from app.database import SessionDep
from repository import BookRepository
from schemas import SBooksAdd, SBookId, SBooks, SBooksUpdate

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)

@router.post("")
async def add_book(session: SessionDep, book: SBooksAdd = Depends()) -> SBookId:
    new_book = await BookRepository.add_book(book, session)
    return {"id": new_book}

@router.get("")
async def get_books(session: SessionDep) -> list[SBooks]:
    books = await BookRepository.get_book(session)
    return books

@router.put("/{book_id}")
async def update_book(session: SessionDep, book_id: int, book: SBooksUpdate = Depends()):
    book = await BookRepository.uppdate_book(book_id, session, book)
    return book

@router.delete("/{book_id}")
async def delete_book(book_id: int, session: SessionDep):
    book = await BookRepository.delete_book(session, book_id)
    return {"id": book}