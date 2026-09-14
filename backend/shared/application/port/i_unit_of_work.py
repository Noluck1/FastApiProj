from abc import ABC, abstractmethod
from types import TracebackType

class IUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> IUnitOfWork:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self, 
        exc_type: type[BaseException] | None, 
        exc: BaseException | None, 
        tb: TracebackType | None,

    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError