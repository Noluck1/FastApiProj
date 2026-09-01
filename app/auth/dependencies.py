from collections.abc import Awaitable, Callable
from typing import Annotated
from app.domain.auth.enums.user_role import UserRole
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.domain.auth.entities.user import User
from app.auth.auth_exceptions import ForbiddenError, UnAuthorizedError
from app.auth.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    auto_error=False
)


@inject
async def get_current_user(
        token: Annotated[str | None, Depends(oauth2_scheme)],
        service: FromDishka[AuthService],
) -> User:

    if token is None:
        raise UnAuthorizedError()
    
    return await service.get_current_user(token)

def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., Awaitable[User]]:
    async def check_role(
        current_user: Annotated[
            User,
            Depends(get_current_user)
        ],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenError(
                role=current_user.role.value

            )

        return current_user

    return check_role