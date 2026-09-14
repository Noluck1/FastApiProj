from dishka import Provider
from backend.app_books.books.api.dependency_injection.book_providers.book_handler_provider import BookHandlerProvider
from backend.app_books.books.api.dependency_injection.book_providers.book_repository_provider import BookRepositoryProvider
from backend.app_books.books.api.dependency_injection.favorite_providers.favorite_handler_provider import FavoriteHandlerProvider
from backend.app_books.books.api.dependency_injection.favorite_providers.favorite_repository_provider import FavoriteRepositoryProvider
from backend.app_books.books.api.dependency_injection.auth_provider import BooksAuthProvider
from backend.app_books.books.api.dependency_injection.communication_provider import CommunicationProvider


def get_books_providers() -> tuple[Provider, ...]:
    return(
        BookRepositoryProvider(),
        FavoriteRepositoryProvider(),
        BookHandlerProvider(),
        FavoriteHandlerProvider(),
        BooksAuthProvider(),
        CommunicationProvider(),
    )