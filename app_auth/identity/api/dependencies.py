from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app_auth.identity.domain.entities.user import User
from shared.api.exceptions import UnAuthorizedError
from app_auth.identity.application.handlers.queries.get_me import GetCurrentUserHandler, GetCurrentUserCommand


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    auto_error=False
)


@inject
async def get_current_user(
        token: Annotated[str | None, Depends(oauth2_scheme)],
        handler: FromDishka[GetCurrentUserHandler],
) -> User:

    if token is None:
        raise UnAuthorizedError()
    
    return await handler.handle(GetCurrentUserCommand(token))