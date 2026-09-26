"""The database, and where its templates and macros are."""

import os
from pathlib import Path

from sqlakit import Database
from sqlakit.sql import Templates

HERE = Path(__file__).parent

db = Database(
    os.environ.get("DATABASE_URL", "sqlite:///shop.db"),
    templates=Templates(HERE / "sql", macros=["shop.macros", "shop.tenant"]),
)
