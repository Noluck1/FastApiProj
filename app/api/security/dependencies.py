from collections.abc import Awaitable, Callable
from typing import Annotated
from fastapi import Depends
from app.identity.domain.entities.user import User
from app.identity.api.exceptions import ForbiddenError
from app.shared.auth.principal import Principal
from app.identity.api.dependencies import get_current_user


async def get_current_principal(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> Principal:
    return Principal(
    subject_id=current_user.require_id(),
    roles=frozenset({current_user.role.value}),
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
            raise ForbiddenError(role=current_role)
        return principal

    return check_role