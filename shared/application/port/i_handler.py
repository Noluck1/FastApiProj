from typing import Generic, Protocol, TypeVar


RequestT = TypeVar(
    "RequestT",
    contravariant=True,
)
ResponseT = TypeVar(
    "ResponseT",
    covariant=True,
)

class IHandler(Protocol, Generic[RequestT, ResponseT]):
    async def handle(self, request: RequestT) -> ResponseT:
        raise NotImplementedError