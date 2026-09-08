from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class FavoriteBook:
    user_id: int
    book_id: int