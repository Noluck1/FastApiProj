from dataclasses import dataclass
from datetime import datetime
from typing import Literal


BookListSortBy = Literal["id", "created_at", "updated_at"]
SortOrder = Literal["asc", "desc"]


@dataclass(frozen=True)
class BookListFilters:
    id: int | None = None
    title: str | None = None
    title_contains: str | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    updated_from: datetime | None = None
    updated_to: datetime | None = None
    is_deleted: bool | None = None
    include_deleted: bool = False