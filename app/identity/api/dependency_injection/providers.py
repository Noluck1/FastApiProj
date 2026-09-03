from dishka import Provider
from app.identity.api.dependency_injection.auth_handler_provider import AuthHandlerProvider
from app.identity.api.dependency_injection.auth_provider import AuthProvider
from app.identity.api.dependency_injection.auth_repository_provider import AuthRepositoryProvider
from app.identity.api.dependency_injection.identity_communication_provider import IdentityCommunicationProvider


def get_identity_providers() -> tuple[Provider, ...]:
    return (
        AuthRepositoryProvider(),
        AuthProvider(),
        AuthHandlerProvider(),
        IdentityCommunicationProvider(),
    )