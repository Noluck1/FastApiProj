from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UserReference:
    user_id: int

class IIdentityCommunication(ABC):
    @abstractmethod
    async def get_active_user(
        self,
        user_id: int,
    ) -> UserReference | None:
        ...