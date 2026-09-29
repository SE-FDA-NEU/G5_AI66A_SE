"""The declarative base every model inherits from.

Only Base lives here. The models import it and app/db/models/__init__.py imports the models, so
nothing imports in a circle.
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Every constraint gets a predictable name, so a later migration can find it and change it,
# on SQLite as well as on any other database.
NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
