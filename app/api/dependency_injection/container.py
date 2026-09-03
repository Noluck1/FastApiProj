from dishka import AsyncContainer, make_async_container
from app.api.dependency_injection.provider.db_provider import DbProvider
from app.books.api.dependency_injection.providers import get_books_providers
from app.identity.api.dependency_injection.providers import get_identity_providers


def build_container() -> AsyncContainer:
    return make_async_container(
        DbProvider(),
        *get_identity_providers(),
        *get_books_providers(),
    )