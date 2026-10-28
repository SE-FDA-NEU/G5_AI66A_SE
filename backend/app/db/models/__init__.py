"""Every table, imported in one place.

Alembic and the seed script import this package so that all five tables are registered on
Base.metadata. A model missing from this list is a table Alembic never creates.
"""

from app.db.models.budget import Budget
from app.db.models.category import KIND_INCOME, KIND_SPENDING, Category
from app.db.models.debt import BORROWED, LENT, Debt
from app.db.models.transaction import Transaction
from app.db.models.user import User

__all__ = [
    "BORROWED",
    "KIND_INCOME",
    "KIND_SPENDING",
    "LENT",
    "Budget",
    "Category",
    "Debt",
    "Transaction",
    "User",
]
