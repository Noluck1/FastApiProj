from dishka import AsyncContainer, make_async_container

from backend.app_books.books.api.dependency_injection.db_provider import BooksDbProvider
from backend.app_books.books.api.dependency_injection.providers import get_books_providers

def build_books_container() -> AsyncContainer:
    return make_async_container(
        BooksDbProvider(),
        *get_books_providers(),
    )