from dataclasses import dataclass
from app_books.books.domain.exceptions import InvalidBookTitleError

@dataclass(frozen=True, slots=True)
class BookTitle:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not 5 <= len(normalized) <= 100:
            raise InvalidBookTitleError

        object.__setattr__(self, "value", normalized)


    def __str__(self) -> str:
        return self.value