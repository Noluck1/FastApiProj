from backend.app_auth.identity.domain.entities.user import User
from backend.app_auth.identity.api.dto.auth_dto import UserDto


def user_to_dto(user: User) -> UserDto:
    if user.id is None:
        raise RuntimeError(
            "Persisted user must have an id"
        )

    full_name_parts = (
        user.last_name,
        user.first_name,
        user.middle_name,
    )

    full_name=" ".join(
        part
        for part in full_name_parts
        if part is not None
    ) or None

    return UserDto(
        id=user.id,
        username=user.username.value,
        role=user.role,
        is_active=user.is_active,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        full_name=full_name,
    )