"""Macros written in Python, for SQL that depends on the values of a call.

`Templates(macros=["app.macros"])` registers every macro of this module.
"""

from typing import Literal

from sqlakit.sql import Context, Param, Sql, sql_macro, tpl


@sql_macro
def owned_by(row: Sql, team_ids: Param, user_ids: Param) -> str:
    """Rows of any of the teams or the users, and none when neither is given."""
    criteria = [
        f"{row}.{column} IN ({param})"
        for column, param in (("team_id", team_ids), ("id", user_ids))
        if param.value
    ]
    return f"({' OR '.join(criteria)})" if criteria else "FALSE"


@sql_macro
def search(q: Param, *columns: Sql) -> str:
    """Rows where any of the columns holds the text, regardless of case."""
    if not q.value:
        return "TRUE"
    return "(" + " OR ".join(tpl.icontains(column, q) for column in columns) + ")"


@sql_macro
def money(ctx: Context, cents: Sql) -> str:
    """An amount in cents, as a decimal with two places."""
    if ctx.dialect == "sqlite":
        return f"printf('%.2f', {cents} / 100.0)"
    return f"round({cents} / 100.0, 2)"


PERIODS = {"'day'": ("%Y-%m-%d", "YYYY-MM-DD"), "'month'": ("%Y-%m", "YYYY-MM")}
"""Each period, as SQLite's `strftime` and PostgreSQL's `to_char` spell it."""


@sql_macro
def period(ctx: Context, at: Sql, size: Literal["'day'", "'month'"]) -> str:
    """The day or the month a timestamp falls in, as text that sorts."""
    sqlite, postgresql = PERIODS[size]
    if ctx.dialect == "sqlite":
        return f"strftime('{sqlite}', {at})"
    return f"to_char({at}, '{postgresql}')"
