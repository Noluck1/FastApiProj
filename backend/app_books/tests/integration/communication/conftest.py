from collections.abc import AsyncIterator
from typing import Annotated

import httpx
import pytest
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import DishkaRoute, setup_dishka
from fastapi import APIRouter, Depends, FastAPI

from backend.app_books.books.api.exception_handlers import register_books_exception_handlers
from backend.app_books.books.api.security.dependencies import get_current_principal
from backend.app_books.books.application.ports.outbound.i_identity_gateway import IIdentityGateway
from backend.app_books.books.infrastructure.clients.identity_http_gateway import IdentityHttpGateway
from backend.app_books.books.infrastructure.security.access_token_verifier import AccessTokenClaims, AccessTokenVerifier, InvalidAccessTokenError
from backend.shared.api.exception_handler import register_common_exception_handlers
from backend.shared.auth.principal import Principal

class StubAccessTokenVerifier(AccessTokenVerifier):
    def __init__(
        self, 
        subject_id: int
    ) -> None:
        self._subject_id = subject_id

    def verify(
        self, 
        token: str
    ) -> AccessTokenClaims:
        if token != "valid-token":
            raise InvalidAccessTokenError

        return AccessTokenClaims(
            subject_id=self._subject_id,
            roles=frozenset({"user"}),
        )

async def create_books_client(
    identity_handler: httpx.AsyncBaseTransport,
    *,
    jwt_user_id: int = 42,
) -> tuple[
    httpx.AsyncClient,
    object,
]:
    verifier = StubAccessTokenVerifier(jwt_user_id)

    class TestBooksProvider(Provider):
        @provide(scope=Scope.APP)
        def access_token_verifier(
            self,
        ) -> AccessTokenVerifier:
            return verifier

        @provide(scope=Scope.APP)
        async def identity_gateway(
            self,
        ) -> AsyncIterator[IIdentityGateway]:
            async with httpx.AsyncClient(
                transport=identity_handler,
                base_url="http://identity-test",
                headers={
                    "X-Service-Token": "test-service-token",
                },
            ) as client:
                yield IdentityHttpGateway(client)

    container = make_async_container(
        TestBooksProvider()
    )

    app = FastAPI()

    setup_dishka(
        container=container,
        app=app,
    )

    register_common_exception_handlers(app)
    register_books_exception_handlers(app)

    router = APIRouter(
        route_class=DishkaRoute,
    )

    @router.get("/protected")
    async def protected_endpoint(
        principal: Annotated[
            Principal,
            Depends(get_current_principal),
        ],
    ) -> dict[str, object]:
        return {
            "user_id": principal.subject_id,
            "roles": sorted(principal.roles),
        }

    app.include_router(router)

    book_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(
            app=app,
            raise_app_exceptions=False,
        ),
        base_url="http://book-test",
    )

    return book_client, container

@pytest.fixture
def books_client_factory():
    return create_books_client
