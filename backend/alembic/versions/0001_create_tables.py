"""Create the four tables: users, categories, transactions and budgets.

Revision ID: 0001
Revises:
Create Date: 2026-09-28
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.Column("kind", sa.String(length=7), nullable=False),
        # BR6 and BR8: a category is a kind of spending or a kind of money received.
        sa.CheckConstraint("kind IN ('expense', 'income')", name=op.f("ck_categories_kind_known")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("name", name=op.f("uq_categories_name")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        # BR2: a one-way hash, never the password.
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        # BR1: stored in lower case, so UNIQUE also rejects the same address in capitals.
        sa.CheckConstraint("email = lower(email)", name=op.f("ck_users_email_lower_case")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("month", sa.String(length=7), nullable=False),
        sa.Column("amount", sa.BigInteger(), nullable=False),
        sa.CheckConstraint("month LIKE '____-__'", name=op.f("ck_budgets_month_yyyy_mm")),
        sa.CheckConstraint("amount > 0", name=op.f("ck_budgets_amount_positive")),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_budgets_category_id_categories"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_budgets_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_budgets")),
        # BR7: one cap per account, per kind of spending, per month.
        sa.UniqueConstraint(
            "user_id",
            "category_id",
            "month",
            name=op.f("uq_budgets_user_id_category_id_month"),
        ),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("kind", sa.String(length=7), nullable=False),
        sa.Column("amount", sa.BigInteger(), nullable=False),
        sa.Column("note", sa.String(length=200), server_default="", nullable=False),
        sa.Column("occurred_on", sa.Date(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "kind IN ('expense', 'income')", name=op.f("ck_transactions_kind_known")
        ),
        # BR5: whole dong, greater than zero.
        sa.CheckConstraint("amount > 0", name=op.f("ck_transactions_amount_positive")),
        # BR6: at most one kind of spending, and it must exist.
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_transactions_category_id_categories"),
        ),
        # BR4: every entry belongs to one account; deleting the account deletes its entries.
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_transactions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transactions")),
    )
    # US05 reads one account's entries, newest first.
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_transactions_user_id_occurred_on", ["user_id", "occurred_on"], unique=False
        )


def downgrade() -> None:
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.drop_index("ix_transactions_user_id_occurred_on")

    op.drop_table("transactions")
    op.drop_table("budgets")
    op.drop_table("users")
    op.drop_table("categories")
