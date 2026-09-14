import logging
from dataclasses import dataclass

from backend.app_auth.identity.application.ports.i_user_repository import IUserRepository
from backend.shared.application.port.i_handler import IHandler

logger = logging.getLogger(__name__)

@dataclass(frozen=True, slots=True)
class GetUserStatusQuery:
    user_id: int

@dataclass(frozen=True, slots=True)
class UserStatusResult:
    user_id: int
    username: str
    full_name: str | None
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

        logger.debug(
            "User retrieved successfully: user_id=%s",
            user.require_id()
        )

        full_name = " ".join(
            part
            for part in (user.last_name, user.first_name, user.middle_name)
            if part is not None
        ) or None

        return UserStatusResult(
            user_id=user.require_id(),
            username=user.username.value,
            full_name=full_name,
            is_active=user.is_active,
            roles=frozenset({user.role.value}),
        )
