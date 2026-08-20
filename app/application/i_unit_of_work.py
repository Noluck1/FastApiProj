from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> IUnitOfWork:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError