"""add login security fields

Revision ID: e7532d872e0d
Revises: 91fdc74e94cb
Create Date: 2026-07-27 15:56:16.651217

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7532d872e0d"
down_revision: Union[str, Sequence[str], None] = "91fdc74e94cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "failed_login_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0"
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "locked_until",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.alter_column(
        "users",
        "failed_login_attempts",
        server_default=None
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "users",
        "locked_until"
    )

    op.drop_column(
        "users",
        "failed_login_attempts"
    )