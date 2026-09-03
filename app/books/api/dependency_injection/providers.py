from dishka import Provider
from app.books.api.dependency_injection.book_providers.book_handler_provider import BookHandlerProvider
from app.books.api.dependency_injection.book_providers.book_repository_provider import BookRepositoryProvider
from app.books.api.dependency_injection.favorite_providers.favorite_handler_provider import FavoriteHandlerProvider
from app.books.api.dependency_injection.favorite_providers.favorite_repository_provider import FavoriteRepositoryProvider




def get_books_providers() -> tuple[Provider, ...]:
    return(
        BookRepositoryProvider(),
        FavoriteRepositoryProvider(),
        BookHandlerProvider(),
        FavoriteHandlerProvider(),
    )