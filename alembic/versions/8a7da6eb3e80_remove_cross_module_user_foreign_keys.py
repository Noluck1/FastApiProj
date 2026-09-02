"""remove cross module user foreign keys

Revision ID: 8a7da6eb3e80
Revises: 03461f7b340a
Create Date: 2026-09-02 13:49:44.226189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a7da6eb3e80'
down_revision: Union[str, Sequence[str], None] = '03461f7b340a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMING_CONVENTION = {
    "fk": (
        "fk_%(table_name)s_"
        "%(column_0_name)s_"
        "%(referred_table_name)s"
    ),
}


def upgrade() -> None:
    with op.batch_alter_table(
        "favorite_book",
        recreate="always",
        naming_convention=NAMING_CONVENTION,
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_favorite_book_user_id_users",
            type_="foreignkey",
        )

    with op.batch_alter_table(
        "books",
        recreate="always",
        naming_convention=NAMING_CONVENTION,
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_books_author_id_users",
            type_="foreignkey",
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "books",
        recreate="always",
        naming_convention=NAMING_CONVENTION,
    ) as batch_op:
        batch_op.create_foreign_key(
            "fk_books_author_id_users",
            "users",
            ["author_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table(
        "favorite_book",
        recreate="always",
        naming_convention=NAMING_CONVENTION,
    ) as batch_op:
        batch_op.create_foreign_key(
            "fk_favorite_book_user_id_users",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )