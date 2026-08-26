"""add book audit fields

Revision ID: 3827fcb0c53d
Revises: 9fbce112ed5e
Create Date: 2026-08-26 11:45:59.837663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3827fcb0c53d'
down_revision: Union[str, Sequence[str], None] = '9fbce112ed5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table(
        "books",
        recreate="always",
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "updated_by_id",
                sa.Integer(),
                nullable=True,
            ),
        )
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
        )
        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
        )
        batch_op.create_index(
            "ix_books_updated_by_id",
            ["updated_by_id"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "books",
        recreate="always",
    ) as batch_op:
        batch_op.drop_index("ix_books_updated_by_id")
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")
        batch_op.drop_column("updated_by_id")