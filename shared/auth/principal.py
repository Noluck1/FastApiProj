from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Principal:
    subject_id: int
    roles: frozenset[str]

    def has_any_role(self, *roles: str) -> bool:
        return not self.roles.isdisjoint(roles)