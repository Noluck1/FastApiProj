from dataclasses import dataclass
from backend.app_books.books.domain.exceptions import InvalidBookDescriptionError


@dataclass(frozen=True, slots=True)
class BookDescription:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if len(normalized) > 255:
            raise InvalidBookDescriptionError


        object.__setattr__(self, "value", normalized)


    def __str__(self) -> str:
        return self.value