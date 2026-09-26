"""A macro whose SQL is in a file, and whose values Python works out."""

from typing import Any

from sqlakit.sql import Param, Sql, sql_macro


@sql_macro("tenant.sql")
def of_team(u: Sql, team: Param) -> dict[str, Any]:  # noqa: ARG001 - tenant.sql reads `u`
    """Rows of the team, given as the `Team` itself."""
    return {"team_id": team.value.id}
