from abc import ABC, abstractmethod

from app_auth.identity.domain.entities.user import User
from app_auth.identity.domain.value_objects.username import Username



class IUserRepository(ABC):
    @abstractmethod
    async def get_by_username(
            self,
            username: Username
    ) -> User | None:
        raise NotImplementedError


    @abstractmethod
    async def get_by_id(
            self,
            user_id: int
    ) -> User | None:
        raise NotImplementedError


    @abstractmethod
    async def add(
        self,
        user: User,
    ) -> User:
        raise NotImplementedError