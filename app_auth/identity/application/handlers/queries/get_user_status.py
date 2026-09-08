from dataclasses import dataclass

from app_auth.identity.application.ports.i_user_repository import IUserRepository
from shared.application.port.i_handler import IHandler

@dataclass(frozen=True, slots=True)
class GetUserStatusQuery:
    user_id: int

@dataclass(frozen=True, slots=True)
class UserStatusResult:
    user_id: int
    is_active: bool
    roles: frozenset[str]


class GetUserStatusHandler(
    IHandler[
        GetUserStatusQuery, 
        UserStatusResult | None
    ]
):
    def __init__(
        self,
        repository: IUserRepository,
    ) -> None:
        self._repository = repository

    async def handle(
        self,
        request: GetUserStatusQuery,
    ) -> UserStatusResult | None:
        user = await self._repository.get_by_id(
            request.user_id
        )

        if user is None:
            return None

        return UserStatusResult(
            user_id=user.require_id(),
            is_active=user.is_active,
            roles=frozenset({user.role.value}),
        )