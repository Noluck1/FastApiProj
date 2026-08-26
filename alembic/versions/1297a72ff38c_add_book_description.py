"""add book description

Revision ID: 1297a72ff38c
Revises: 3827fcb0c53d
Create Date: 2026-08-26 12:44:44.234328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1297a72ff38c'
down_revision: Union[str, Sequence[str], None] = '3827fcb0c53d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table(
        "books",
        recreate="always",
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "description",
                sa.String(length=255),
                nullable=True,
            ),
        )

        batch_op.alter_column(
            "title",
            existing_type=sa.String(),
            type_=sa.String(length=100),
            existing_nullable=False,
        )

        batch_op.create_check_constraint(
            "ck_books_title_max_length",
            "length(title) <= 100",
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "books",
        recreate="always",
    ) as batch_op:
        batch_op.drop_constraint(
            "ck_books_title_max_length",
            type_="check",
        )

        batch_op.alter_column(
            "title",
            existing_type=sa.String(length=100),
            type_=sa.String(),
            existing_nullable=False,
        )

        batch_op.drop_column("description")
