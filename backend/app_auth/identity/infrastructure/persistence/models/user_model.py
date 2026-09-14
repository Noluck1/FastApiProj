from sqlalchemy.orm import Mapped, mapped_column
from backend.app_auth.identity.infrastructure.persistence.base import IdentityBase
from backend.app_auth.identity.domain.enums.user_role import UserRole
from sqlalchemy import Enum as SqlEnum, String

class UserOrm(IdentityBase):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
    )
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(
            UserRole,
            name="user_role",
            native_enum=False,
            values_callable=lambda roles: [
                role.value for role in roles
            ],
            create_constraint=True,
        ),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )