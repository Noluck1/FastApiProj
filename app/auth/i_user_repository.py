from abc import ABC, abstractmethod

from app.shared.dtos.auth_dto import UserDto, UserWithPasswordDto


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_username(
            self,
            username: str
    ) -> UserWithPasswordDto | None:
        raise NotImplementedError


    @abstractmethod
    async def get_by_id(
            self,
            user_id: int
    ) -> UserDto | None:
        raise NotImplementedError


    @abstractmethod
    async def add(
        self,
        username: str,
        password_hash: str,
    ) -> UserDto:
        raise NotImplementedError