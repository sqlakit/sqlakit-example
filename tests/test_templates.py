"""The templates and the macros, checked the way CI checks them."""

import subprocess
import sys
from pathlib import Path

from app.db import db

ROOT = Path(__file__).parent.parent


def test_every_template_reads() -> None:
    db.sql.check()


def test_the_command_line_finds_what_the_code_configures() -> None:
    ran = subprocess.run(  # noqa: S603 - the command this environment installed
        [Path(sys.executable).parent / "sqlakit", "check"],
        capture_output=True,
        check=False,
        cwd=ROOT,
        text=True,
    )

    assert ran.returncode == 0, ran.stdout
    assert ran.stdout.splitlines() == [
        "templates: app/sql (app/db.py:13)",
        "namespace: tpl (the default)",
        "macros: 5 in Python, 1 file of SQL macros",
        "dialect: sqlite (app/db.py:11)",
        "",
        "14 templates, 0 problems",
    ]
