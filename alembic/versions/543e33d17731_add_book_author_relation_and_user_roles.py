"""add book author relation and user roles

Revision ID: 543e33d17731
Revises: 8e37c01b8903
Create Date: 2026-08-24 16:53:58.491193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "543e33d17731"
down_revision: Union[str, Sequence[str], None] = "8e37c01b8903"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role_enum = sa.Enum(
        "user",
        "author",
        "admin",
        name="user_role",
        native_enum=False,
        create_constraint=True,
    )

    with op.batch_alter_table("books", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("author_id", sa.Integer(), nullable=False)
        )
        batch_op.create_index(
            "ix_books_author_id",
            ["author_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "fk_books_author_id_users",
            "users",
            ["author_id"],
            ["id"],
            ondelete="CASCADE",
        )
        batch_op.drop_column("author")

    with op.batch_alter_table("users", recreate="always") as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sa.String(length=30),
            type_=user_role_enum,
            existing_nullable=False,
        )


def downgrade() -> None:
    user_role_enum = sa.Enum(
        "user",
        "author",
        "admin",
        name="user_role",
        native_enum=False,
        create_constraint=True,
    )

    with op.batch_alter_table("users", recreate="always") as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=user_role_enum,
            type_=sa.String(length=30),
            existing_nullable=False,
        )

    with op.batch_alter_table("books", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("author", sa.String(), nullable=False)
        )
        batch_op.drop_constraint(
            "fk_books_author_id_users",
            type_="foreignkey",
        )
        batch_op.drop_index("ix_books_author_id")
        batch_op.drop_column("author_id")