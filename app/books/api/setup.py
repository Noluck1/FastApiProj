from fastapi import FastAPI
from app.books.api.routers.book.book import router as book_router
from app.books.api.routers.favorite.favorite import router as favorite_router
from app.books.api.exception_handlers import register_books_exception_handlers



def register_books_api(app: FastAPI) -> None:
    app.include_router(book_router)
    app.include_router(favorite_router)

    register_books_exception_handlers(app)