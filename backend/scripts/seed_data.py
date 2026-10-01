"""Create the database and fill it with demo data. Run from backend/:

    python -m scripts.seed_data    create the tables, then add the demo data once

The Alembic migrations run first, so the tables always match app/db/models. Running the script a
second time adds nothing.
"""

import argparse
from dataclasses import dataclass

from alembic import command
from alembic.config import Config
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import BACKEND_DIR, settings
from app.core.security import hash_password
from app.db.models import KIND_INCOME, KIND_SPENDING, Budget, Category, Transaction, User
from app.db.repositories import user_repo
from app.db.session import make_engine

DEMO_EMAIL = "mai@example.com"
DEMO_PASSWORD = "demo1234"

# BR6 names the eight kinds of spending; BR8 names the three kinds of money received.
CATEGORIES = [
    ("Food", KIND_SPENDING),
    ("Transport", KIND_SPENDING),
    ("Shopping", KIND_SPENDING),
    ("Bills", KIND_SPENDING),
    ("Entertainment", KIND_SPENDING),
    ("Health", KIND_SPENDING),
    ("Education", KIND_SPENDING),
    ("Other", KIND_SPENDING),
    ("Salary", KIND_INCOME),
    ("Bonus", KIND_INCOME),
    ("Other income", KIND_INCOME),
]


@dataclass
class RowCounts:
    categories: int
    users: int
    transactions: int
    budgets: int


def alembic_config(database_url: str) -> Config:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    # Alembic reads its settings with % interpolation, so a literal % has to be doubled.
    config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
    return config


def add_categories(db: Session) -> dict[str, Category]:
    existing = {category.name: category for category in db.scalars(select(Category))}
    for name, kind in CATEGORIES:
        if name not in existing:
            existing[name] = Category(name=name, kind=kind)
            db.add(existing[name])
    db.commit()
    return existing


def add_demo_account(db: Session) -> User:
    account = user_repo.get_by_email(db, DEMO_EMAIL)
    if account is None:
        account = user_repo.create(
            db, email=DEMO_EMAIL, password_hash=hash_password(DEMO_PASSWORD)
        )
    return account


def count_rows(db: Session) -> RowCounts:
    def count(model) -> int:
        return db.scalar(select(func.count()).select_from(model)) or 0

    return RowCounts(count(Category), count(User), count(Transaction), count(Budget))


def seed(database_url: str) -> RowCounts:
    """Migrate the database at `database_url`, add the demo data once, and count the rows."""
    config = alembic_config(database_url)
    command.upgrade(config, "head")

    engine = make_engine(database_url)
    try:
        with Session(engine) as db:
            add_categories(db)
            add_demo_account(db)
            return count_rows(db)
    finally:
        engine.dispose()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Create the database and fill it with demo data.")
    parser.parse_args(argv)

    counts = seed(settings.DATABASE_URL)
    print(f"Database ready: {settings.DATABASE_URL.removeprefix('sqlite:///')}")
    print(f"  categories    {counts.categories}")
    print(f"  users         {counts.users}")
    print(f"  transactions  {counts.transactions}")
    print(f"  budgets       {counts.budgets}")
    print(f"Sign in as {DEMO_EMAIL} with the password {DEMO_PASSWORD}")


if __name__ == "__main__":
    main()
