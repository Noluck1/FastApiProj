from collections.abc import Awaitable, Callable
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from backend.app_books.books.config.settings import books_settings
from backend.app_books.books.infrastructure.security.access_token_verifier import (
    AccessTokenVerifier,
    InvalidAccessTokenError,
)
from backend.app_books.books.application.ports.outbound.i_identity_gateway import IIdentityGateway
from backend.shared.api.exceptions import (
    ForbiddenError,
    UnAuthorizedError,
)
from backend.shared.auth.principal import Principal



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=books_settings.identity_token_url,
    auto_error=False,
)


@inject
async def get_current_principal(
    token: Annotated[
        str | None,
        Depends(oauth2_scheme),
    ],
    verifier: FromDishka[AccessTokenVerifier],
    identity_gateway: FromDishka[IIdentityGateway]
) -> Principal:
    if token is None:
        raise UnAuthorizedError()

    try:
        claims = verifier.verify(token)
    except InvalidAccessTokenError as error:
        raise UnAuthorizedError() from error

    user = await identity_gateway.get_user(
        claims.subject_id
    )

    if (
        user is None
        or not user.is_active
        or user.user_id != claims.subject_id
    ):
        raise UnAuthorizedError()

    return Principal(
        subject_id=user.user_id,
        roles=user.roles,
    )


def require_roles(
    *allowed_roles: str,
) -> Callable[..., Awaitable[Principal]]:
    async def check_role(
        principal: Annotated[
            Principal,
            Depends(get_current_principal),
        ],
    ) -> Principal:
        if not principal.has_any_role(*allowed_roles):
            current_role = next(
                iter(principal.roles),
                "unknown",
            )

            raise ForbiddenError(
                role=current_role,
            )

        return principal

    return check_role