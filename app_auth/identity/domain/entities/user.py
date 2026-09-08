from dataclasses import dataclass
from app_auth.identity.domain.exceptions import InactiveUserError
from app_auth.identity.domain.enums.user_role import UserRole
from app_auth.identity.domain.value_objects.username import Username
from app_auth.identity.domain.value_objects.password_hash import PasswordHash

@dataclass(slots=True)
class User:
    id: int | None
    username: Username
    password_hash: PasswordHash
    role: UserRole
    is_active: bool

    def require_id(self) -> int:
        if self.id is None:
            raise RuntimeError(
                "Persisted user must have an id"
            )
        return self.id

    def ensure_active(self) -> None:
        if not self.is_active:
            raise InactiveUserError

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def change_role(self, role: UserRole) -> None:
        self.role = role