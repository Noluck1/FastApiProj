from dishka import Provider
from app_auth.identity.api.dependency_injection.auth.auth_handler_provider import AuthHandlerProvider
from app_auth.identity.api.dependency_injection.auth.auth_provider import AuthProvider
from app_auth.identity.api.dependency_injection.auth.auth_repository_provider import AuthRepositoryProvider

def get_identity_providers() -> tuple[Provider, ...]:
    return (
        AuthRepositoryProvider(),
        AuthProvider(),
        AuthHandlerProvider(),
    )