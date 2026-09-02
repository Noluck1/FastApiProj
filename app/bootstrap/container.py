from dishka import AsyncContainer, make_async_container
from app.identity.bootstrap.providers.auth_provider import AuthProvider
from app.bootstrap.provider.db_provider import DbProvider
from app.identity.bootstrap.providers.auth_handler_provider import AuthHandlerProvider
from app.identity.bootstrap.providers.auth_repository_provider import AuthRepositoryProvider
from app.books.bootstrap.providers.book_repository_provider import BookRepositoryProvider
from app.books.bootstrap.providers.book_handler_provider import BookHandlerProvider
from app.favorite.bootstrap.providers.favorite_handler_provider import FavoriteHandlerProvider
from app.favorite.bootstrap.providers.favorite_repository_provider import FavoriteRepositoryProvider


def build_container() -> AsyncContainer:
    return make_async_container(
        DbProvider(),
        AuthProvider(),
        AuthHandlerProvider(),
        AuthRepositoryProvider(),
        BookHandlerProvider(),
        BookRepositoryProvider(),
        FavoriteRepositoryProvider(),
        FavoriteHandlerProvider()
    )