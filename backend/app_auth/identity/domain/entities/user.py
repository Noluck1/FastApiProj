from dataclasses import dataclass
from backend.app_auth.identity.domain.exceptions import InactiveUserError
from backend.app_auth.identity.domain.enums.user_role import UserRole
from backend.app_auth.identity.domain.value_objects.username import Username
from backend.app_auth.identity.domain.value_objects.password_hash import PasswordHash

@dataclass(slots=True)
class User:
    id: int | None
    username: Username
    password_hash: PasswordHash
    role: UserRole
    is_active: bool

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None


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

    def change_first_name(
        self,
        first_name: str,
    ) -> None:
        self.first_name = first_name


    def change_last_name(
        self,
        last_name: str,
    ) -> None:
        self.last_name = last_name


    def change_middle_name(
        self,
        middle_name: str | None,
    ) -> None:
        self.middle_name = middle_name