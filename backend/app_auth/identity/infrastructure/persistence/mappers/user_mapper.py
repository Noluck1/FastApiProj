from backend.app_auth.identity.infrastructure.persistence.models.user_model import UserOrm
from backend.app_auth.identity.domain.entities.user import User
from backend.app_auth.identity.domain.value_objects.username import Username
from backend.app_auth.identity.domain.value_objects.password_hash import PasswordHash


def user_to_domain(model: UserOrm) -> User:
    return User(
        id=model.id,
        username=Username(model.username),
        password_hash=PasswordHash(model.password_hash),
        role=model.role,
        is_active=model.is_active,
        first_name=model.first_name,
        last_name=model.last_name,
        middle_name=model.middle_name,
    )



def user_to_orm(user: User) -> UserOrm:
    return UserOrm(
        username=user.username.value,
        password_hash=user.password_hash.value,
        role=user.role,
        is_active=user.is_active,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )

def update_orm_from_domain(
    model: UserOrm,
    user: User,
) -> None:
    model.username = user.username.value
    model.password_hash = user.password_hash.value
    model.role = user.role
    model.is_active = user.is_active
    model.first_name = user.first_name
    model.last_name = user.last_name
    model.middle_name = user.middle_name

