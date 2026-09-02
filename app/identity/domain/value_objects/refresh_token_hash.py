from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RefreshTokenHash:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) != 64:
            raise ValueError(
                "Refresh token hash must be SHA-256"
            )

        try:
            int(self.value, 16)

        except ValueError as error:
            raise ValueError(
                "Refresh token hash must by hexadecimal"
            ) from error


    def __str__(self) -> str:
        return self.value