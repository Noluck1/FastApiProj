from app.identity.infrastructure.persistence.models.user_model import UserOrm
from app.identity.domain.entities.user import User
from app.identity.domain.value_objects.username import Username
from app.identity.domain.value_objects.password_hash import PasswordHash


def user_to_domain(model: UserOrm) -> User:
    return User(
        id=model.id,
        username=Username(model.username),
        password_hash=PasswordHash(model.password_hash),
        role=model.role,
        is_active=model.is_active,
    )



def user_to_orm(user: User) -> UserOrm:
    return UserOrm(
        username=user.username.value,
        password_hash=user.password_hash.value,
        role=user.role,
        is_active=user.is_active,
    )

