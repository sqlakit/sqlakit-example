"""The queries the shop runs, one function per template.

Each name in `db.sql("...")` is a template under `shop/sql`, and `sqlakit-lsp`
links it to its file, completes it and marks one that isn't there.
"""

from collections.abc import Sequence
from datetime import datetime

import sqlalchemy as sa
from sqlakit.sql import Inline

from .db import db
from .models import Team


def search_users(
    *,
    q: str | None = None,
    teams: Sequence[int] = (),
    sort: str | Sequence[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> Sequence[sa.Row]:
    """Active users, narrowed by the text, the teams and the page asked for."""
    return db.sql(
        "users/search.sql", q=q, teams=teams, sort=sort, limit=limit, offset=offset
    ).all()


def users_owned_by(
    *, teams: Sequence[int] = (), users: Sequence[int] = ()
) -> Sequence[sa.Row]:
    """Users of any of the teams, or any of the users."""
    return db.sql("users/owned.sql", teams=teams, users=users).all()


def users_of_team(team: Team) -> Sequence[sa.Row]:
    """The active users of a team."""
    return db.sql("users/of_team.sql", team=team).all()


def users_named(name: str) -> Sequence[sa.Row]:
    """The users of a name, whatever its case."""
    return db.sql("users/named.sql", name=name).all()


def recent_orders(
    *,
    since: datetime | None = None,
    until: datetime | None = None,
    statuses: Sequence[str] = (),
    exclude: bool = False,
) -> Sequence[sa.Row]:
    """Paid orders in a period, with some statuses kept or left out."""
    return db.sql(
        "orders/recent.sql",
        since=since,
        until=until,
        statuses=statuses,
        exclude=exclude,
    ).all()


def spending_by_user(
    *, since: datetime | None = None, sort: str | None = None
) -> Sequence[sa.Row]:
    """What each user spent on paid orders since a moment."""
    return db.sql(
        "orders/by_user.sql",
        since=since,
        until=None,
        statuses=(),
        exclude=False,
        sort=sort,
    ).all()


def monthly(team: Team) -> Sequence[sa.Row]:
    """A team's paid orders, per month."""
    return db.sql("orders/monthly.sql", team=team).all()


def filtered_orders(
    *, user_name: str | None = None, include_unpaid: bool = False
) -> Sequence[sa.Row]:
    """Orders, of one user by name if asked, and the unpaid ones if asked."""
    return db.sql(
        "orders/filtered.sql", user_name=user_name, include_unpaid=include_unpaid
    ).all()


def targets(rows: Sequence[tuple[int, int]]) -> Sequence[sa.Row]:
    """Each team's target, as `(team_id, target)`, against its orders."""
    return db.sql("reports/targets.sql", targets=rows).all()


def orders_per_status(statuses: Sequence[str]) -> Sequence[sa.Row]:
    """How many orders are in each status, and 0 for a status with none."""
    return db.sql("reports/statuses.sql", statuses=statuses).all()


def top_spenders(top: int) -> Sequence[sa.Row]:
    """The `top` users of each team by what they spent on paid orders."""
    return db.sql("reports/top_spenders.sql", top=top).all()


def count_rows(table: str) -> int:
    """The rows of `users` or `orders`, and of nothing else."""
    return (
        db.sql("reports/count.sql", table=Inline.name(table, "users", "orders"))
        .scalars()
        .one()
    )


def users_sorted_by(column: str) -> Sequence[sa.Row]:
    """Users sorted by `id`, `name` or `email`."""
    return db.sql("reports/sorted.sql", column=column).all()


def version() -> str:
    """The version of the database."""
    return db.sql("reports/version.sql").scalars().one()
