from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class IdentityUser:
    user_id: int
    is_active: bool
    roles: frozenset[str]


class IIdentityGateway(ABC):
    @abstractmethod
    async def get_user(
        self,
        user_id: int,
    ) -> IdentityUser | None:
        raise NotImplementedError