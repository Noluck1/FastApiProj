from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.sqllitdb.base import Model


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
    role: Mapped[str] = mapped_column(
        String(30),
        default='user',
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
    )