from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")

class PaginatedDro(BaseModel, Generic[T]):
    item: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int