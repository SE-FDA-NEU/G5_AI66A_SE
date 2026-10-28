"""Create the debts table: money borrowed and lent (US13).

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-28
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "debts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("direction", sa.String(length=8), nullable=False),
        sa.Column("person", sa.String(length=60), nullable=False),
        sa.Column("amount", sa.BigInteger(), nullable=False),
        sa.Column("note", sa.String(length=200), server_default="", nullable=False),
        sa.Column("started_on", sa.Date(), nullable=False),
        sa.Column("due_on", sa.Date(), nullable=True),
        sa.Column("settled_on", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "direction IN ('borrowed', 'lent')", name=op.f("ck_debts_direction_known")
        ),
        # BR13: a name of 1 to 60 characters, an amount above 0 (BR5), and a due date that is
        # not before the day the money changed hands.
        sa.CheckConstraint("amount > 0", name=op.f("ck_debts_amount_positive")),
        sa.CheckConstraint(
            "due_on IS NULL OR due_on >= started_on", name=op.f("ck_debts_due_not_before_start")
        ),
        sa.CheckConstraint(
            "length(person) BETWEEN 1 AND 60", name=op.f("ck_debts_person_length")
        ),
        # BR4: every debt belongs to one account; deleting the account deletes its debts.
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_debts_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_debts")),
    )
    # /debts reads one account's debts, the open ones first.
    with op.batch_alter_table("debts", schema=None) as batch_op:
        batch_op.create_index(
            "ix_debts_user_id_settled_on", ["user_id", "settled_on"], unique=False
        )


def downgrade() -> None:
    with op.batch_alter_table("debts", schema=None) as batch_op:
        batch_op.drop_index("ix_debts_user_id_settled_on")

    op.drop_table("debts")
