"""Categories of an account's own (BR17): categories.user_id, and names unique per account.

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-15
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: str | Sequence[str] | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # batch_alter_table lets SQLite, which cannot drop a constraint in place, do the same.
    with op.batch_alter_table("categories") as batch:
        batch.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch.drop_constraint("uq_categories_name", type_="unique")
        batch.create_unique_constraint("uq_categories_user_id_name", ["user_id", "name"])
        batch.create_foreign_key(
            "fk_categories_user_id_users", "users", ["user_id"], ["id"], ondelete="CASCADE"
        )
        batch.create_index("ix_categories_user_id", ["user_id"])


def downgrade() -> None:
    # The categories accounts added go first: their entries keep their amounts, with no category.
    op.execute(
        "UPDATE transactions SET category_id = NULL WHERE category_id IN "
        "(SELECT id FROM categories WHERE user_id IS NOT NULL)"
    )
    op.execute("DELETE FROM categories WHERE user_id IS NOT NULL")
    with op.batch_alter_table("categories") as batch:
        batch.drop_index("ix_categories_user_id")
        batch.drop_constraint("fk_categories_user_id_users", type_="foreignkey")
        batch.drop_constraint("uq_categories_user_id_name", type_="unique")
        batch.create_unique_constraint("uq_categories_name", ["name"])
        batch.drop_column("user_id")
