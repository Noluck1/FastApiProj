from dataclasses import dataclass
from app.identity.domain.exceptions import InvalidUsernameError


@dataclass(frozen=True, slots=True)
class Username:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not 5 <= len(normalized) <= 50:
            raise InvalidUsernameError


        object.__setattr__(
            self,
            "value",
            normalized,
        )

    def __str__(self) -> str:
        return self.value