"""The database, and where its templates and macros are."""

import os
from pathlib import Path

from sqlakit import Database
from sqlakit.sql import Templates

HERE = Path(__file__).parent

db = Database(
    os.environ.get("DATABASE_URL", "sqlite:///app.db"),
    templates=Templates(HERE / "sql", macros=["app.macros", "app.tenant"]),
)
