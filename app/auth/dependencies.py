from collections.abc import Awaitable, Callable
from typing import Annotated
from app.shared.enums.user_role import UserRole
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.auth_exceptions import ForbiddenError, UnAuthorizedError
from app.auth.auth_service import AuthService
from app.shared.dtos.auth_dto import UserDto

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False
)


@inject
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: FromDishka[AuthService],
) -> UserDto:

    if token is None:
        raise UnAuthorizedError()
    
    return await service.get_current_user(token)

def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., Awaitable[UserDto]]:
    async def check_role(
        current_user: Annotated[
            UserDto,
            Depends(get_current_user)
        ],
    ) -> UserDto:
        if current_user.role not in allowed_roles:
            raise ForbiddenError(
                role=current_user.role.value

            )

        return current_user

    return check_role