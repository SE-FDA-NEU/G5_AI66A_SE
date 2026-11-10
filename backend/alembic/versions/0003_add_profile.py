"""Add the profile to users: full name, the name to call them, phone and picture (US16).

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | Sequence[str] | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # batch_alter_table lets SQLite, which cannot add several columns in one ALTER, do the same.
    with op.batch_alter_table("users") as batch:
        batch.add_column(sa.Column("full_name", sa.String(length=80), nullable=True))
        batch.add_column(sa.Column("nickname", sa.String(length=40), nullable=True))
        batch.add_column(sa.Column("phone", sa.String(length=30), nullable=True))
        batch.add_column(sa.Column("avatar", sa.Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("users") as batch:
        batch.drop_column("avatar")
        batch.drop_column("phone")
        batch.drop_column("nickname")
        batch.drop_column("full_name")
