from dishka import AsyncContainer, make_async_container
from app.api.dependency_injection.auth_provider import AuthProvider
from app.api.dependency_injection.db_provider import DbProvider
from app.api.dependency_injection.repository_provider import RepositoryProvider
from app.api.dependency_injection.service_provider import ServiceProvider

def build_container() -> AsyncContainer:
    return make_async_container(
        DbProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        AuthProvider(),
    )