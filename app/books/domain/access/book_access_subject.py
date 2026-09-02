from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BookAccessSubject:
    user_id: int
    roles: frozenset[str]

    def has_role(self, role: str) -> bool:
        return role in self.roles