from dishka import Provider
from app_books.books.api.dependency_injection.book_providers.book_handler_provider import BookHandlerProvider
from app_books.books.api.dependency_injection.book_providers.book_repository_provider import BookRepositoryProvider
from app_books.books.api.dependency_injection.favorite_providers.favorite_handler_provider import FavoriteHandlerProvider
from app_books.books.api.dependency_injection.favorite_providers.favorite_repository_provider import FavoriteRepositoryProvider
from app_books.books.api.dependency_injection.auth_provider import BooksAuthProvider
from app_books.books.api.dependency_injection.communication_provider import CommunicationProvider


def get_books_providers() -> tuple[Provider, ...]:
    return(
        BookRepositoryProvider(),
        FavoriteRepositoryProvider(),
        BookHandlerProvider(),
        FavoriteHandlerProvider(),
        BooksAuthProvider(),
        CommunicationProvider(),
    )