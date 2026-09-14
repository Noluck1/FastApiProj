from dishka import AsyncContainer, make_async_container

from backend.app_auth.identity.api.dependency_injection.db_provider import IdentityDbProvider
from backend.app_auth.identity.api.dependency_injection.providers import get_identity_providers


def build_identity_container() -> AsyncContainer:
    return make_async_container(
        IdentityDbProvider(),
        *get_identity_providers(),
    )