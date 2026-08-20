from typing import Generic, TypeVar, Literal
from pydantic import BaseModel


T = TypeVar("T")

class ApiResponseSchema(BaseModel, Generic[T]):
    status: Literal["success", "error"]
    message: str
    data: T | None = None