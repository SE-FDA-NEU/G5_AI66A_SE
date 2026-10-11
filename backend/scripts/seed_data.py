"""Create the database and fill it with demo data. Run from backend/:

    python -m scripts.seed_data            create the tables, then add the demo data once
    python -m scripts.seed_data --reset    empty the database and seed it again

The Alembic migrations run first, so the tables always match app/db/models. Running the script a
second time adds nothing.
"""

import argparse
from dataclasses import dataclass
from datetime import date, timedelta

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

# Mai, persona 1: a student who lives on 4,000,000 dong a month sent by her family.
# Each entry: (days before today, category, amount in dong, the note exactly as she typed it).
# 25 entries, so the list on / shows the newest 20 and leaves 5 out (US05). Every date is today
# or earlier, never later (BR11), and never before the 1st of this month (see entry_date).
ENTRIES = [
    (12, "Food", 35_000, "com trua"),
    (11, "Food", 45_000, "pho"),
    (11, "Other", 30_000, "qua sinh nhat"),
    (10, "Food", 40_000, "com trua"),
    (10, "Bills", 50_000, "nap dien thoai"),
    (9, "Bills", 1_500_000, "tien nha"),
    (9, "Other income", 4_000_000, "tien bo me gui"),
    (8, "Entertainment", 150_000, "karaoke"),
    (8, "Transport", 28_000, "grab"),
    (7, "Education", 180_000, "sach giao trinh"),
    (7, "Food", 50_000, "tra sua"),
    (6, "Health", 60_000, "thuoc cam"),
    (6, "Food", 45_000, "com trua"),
    (5, "Bills", 150_000, "tien dien"),
    (5, "Food", 20_000, "banh mi"),
    (4, "Food", 25_000, "ca phe"),
    (4, "Transport", 7_000, "xe buyt"),
    (3, "Shopping", 189_000, "shopee"),
    (3, "Food", 50_000, "com toi"),
    (2, "Food", 40_000, "bun bo"),
    (2, "Entertainment", 90_000, "xem phim"),
    (1, "Transport", 32_000, "grab ve nha"),
    (1, "Education", 15_000, "photo tai lieu"),
    (0, "Food", 45_000, "com trua"),
    (0, "Food", 55_000, "tra sua"),
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


def entry_date(today: date, days_ago: int) -> date:
    """`days_ago` days before today, but never before the 1st of this month.

    The overview totals this month only (US04). Run on the 1st to the 12th of a month, the oldest
    entries would otherwise fall in last month, Mai's 4,000,000 allowance among them, and the
    overview would show more spent than received. Moving them up to the 1st keeps all 25 entries,
    and their order, in the month the demo is run.
    """
    return max(today - timedelta(days=days_ago), today.replace(day=1))


def add_entries(db: Session, account: User, categories: dict[str, Category], today: date) -> None:
    already_seeded = db.scalar(
        select(func.count()).select_from(Transaction).where(Transaction.user_id == account.id)
    )
    if already_seeded:
        return
    # Oldest first, so ids grow with time, as they would if Mai had typed them day by day.
    for days_ago, category_name, amount, note in ENTRIES:
        category = categories[category_name]
        occurred_on = entry_date(today, days_ago)
        assert occurred_on <= today, "BR11: an entry is never dated later than today"
        db.add(
            Transaction(
                user_id=account.id,
                kind=category.kind,
                amount=amount,
                note=note,
                occurred_on=occurred_on,
                category_id=category.id,
            )
        )
    db.commit()


def count_rows(db: Session) -> RowCounts:
    def count(model) -> int:
        return db.scalar(select(func.count()).select_from(model)) or 0

    return RowCounts(count(Category), count(User), count(Transaction), count(Budget))


def seed(database_url: str, *, reset: bool = False, today: date | None = None) -> RowCounts:
    """Migrate the database at `database_url`, add the demo data once, and count the rows."""
    config = alembic_config(database_url)
    if reset:
        command.downgrade(config, "base")
    command.upgrade(config, "head")

    engine = make_engine(database_url)
    try:
        with Session(engine) as db:
            categories = add_categories(db)
            account = add_demo_account(db)
            add_entries(db, account, categories, today or date.today())
            return count_rows(db)
    finally:
        engine.dispose()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Create the database and fill it with demo data.")
    parser.add_argument(
        "--reset", action="store_true", help="empty the database first, then seed it again"
    )
    args = parser.parse_args(argv)

    counts = seed(settings.DATABASE_URL, reset=args.reset)
    print(f"Database ready: {settings.DATABASE_URL.removeprefix('sqlite:///')}")
    print(f"  categories    {counts.categories}")
    print(f"  users         {counts.users}")
    print(f"  transactions  {counts.transactions}")
    print(f"  budgets       {counts.budgets}")
    print(f"Sign in as {DEMO_EMAIL} with the password {DEMO_PASSWORD}")


if __name__ == "__main__":
    main()
