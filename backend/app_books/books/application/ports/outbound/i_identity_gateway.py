from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class IdentityUser:
    user_id: int
    username: str
    full_name: str | None
    is_active: bool
    roles: frozenset[str]


class IIdentityGateway(ABC):
    @abstractmethod
    async def get_user(
        self,
        user_id: int,
    ) -> IdentityUser | None:
        raise NotImplementedError
