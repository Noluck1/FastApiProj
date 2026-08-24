from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.sqllitdb.base import Model
from app.shared.enums.user_role import UserRole
from sqlalchemy import Enum as SqlEnum, String

class UserOrm(Model):
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

    books: Mapped[list["BooksOrm"]] = relationship(
        back_populates="author",
    )