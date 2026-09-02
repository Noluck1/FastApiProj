from app.identity.domain.entities.user import User
from app.identity.api.dto.auth_dto import UserDto


def user_to_dto(user: User) -> UserDto:
    if user.id is None:
        raise RuntimeError(
            "Persisted user must have an id"
        )

    return UserDto(
        id=user.id,
        username=user.username.value,
        role=user.role,
        is_active=user.is_active,
    )