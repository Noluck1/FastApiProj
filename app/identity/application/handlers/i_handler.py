from typing import Generic, Protocol, TypeVar


RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")

class IHandler(Protocol, Generic[RequestT, ResponseT]):
    async def handle(self, request: RequestT) -> ResponseT:
        raise NotImplementedError