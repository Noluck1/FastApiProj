from collections.abc import AsyncIterator

import httpx
from dishka import Provider, Scope, provide

from backend.app_books.books.application.ports.outbound.i_identity_gateway import IIdentityGateway
from backend.app_books.books.config.settings import books_settings
from backend.app_books.books.infrastructure.clients.identity_http_gateway import IdentityHttpGateway


class CommunicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def identity_gateway(
        self,
    ) -> AsyncIterator[IIdentityGateway]:
        headers = {
            "X-Service-Token": (
                books_settings
                .identity_service_token
                .get_secret_value()
            ),
        }

        async with httpx.AsyncClient(
            base_url=books_settings.identity_base_url,
            headers=headers,
            timeout=(
                books_settings
                .identity_request_timeout_seconds
            ),
        ) as client:
            yield IdentityHttpGateway(client)