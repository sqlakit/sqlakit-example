"""Every query of the shop, run on SQLite against the rows of `shop.seed`."""

from collections.abc import Sequence
from datetime import datetime

import pytest
import sqlalchemy as sa
from sqlakit import InlineValueError, UnknownIdentifierError

from shop import queries
from shop.db import db
from shop.models import Team

pytestmark = [pytest.mark.db, pytest.mark.usefixtures("shop")]


def rows(found: Sequence[sa.Row]) -> list[tuple[object, ...]]:
    return [tuple(row) for row in found]


def test_users_are_searched_sorted_and_paged() -> None:
    assert rows(queries.search_users(q="a", sort="name.desc")) == [
        (3, "Linus", "linus@example.com"),
        (2, "Grace", "grace@example.com"),
        (1, "Ada", "ada@example.com"),
    ]
    assert rows(queries.search_users(teams=[1], limit=1, offset=1)) == [
        (2, "Grace", "grace@example.com"),
    ]


def test_every_active_user_is_found_when_nothing_narrows_them() -> None:
    assert [name for _, name, _ in queries.search_users()] == ["Ada", "Grace", "Linus"]


def test_users_are_owned_by_teams_or_by_ids() -> None:
    assert rows(queries.users_owned_by(teams=[2])) == [(3, "Linus"), (4, "Old")]
    assert rows(queries.users_owned_by(users=[1])) == [(1, "Ada")]
    assert rows(queries.users_owned_by()) == []


def test_a_name_is_found_whatever_its_case() -> None:
    assert rows(queries.users_named("ada")) == [(1, "Ada")]
    assert rows(queries.users_named("GRACE")) == [(2, "Grace")]


def test_a_team_is_passed_as_the_object() -> None:
    red = db.session.get_one(Team, 1)

    assert rows(queries.users_of_team(red)) == [(1, "Ada"), (2, "Grace")]


def test_recent_orders_are_the_paid_ones_in_the_period() -> None:
    february = datetime(2026, 2, 1)

    assert [order.id for order in queries.recent_orders(since=february)] == [2, 3, 5]
    assert [
        order.id
        for order in queries.recent_orders(
            until=february, statuses=["paid"], exclude=True
        )
    ] == []


def test_spending_reads_the_included_orders() -> None:
    assert rows(queries.spending_by_user()) == [
        ("Grace", 1, "40.00", "3"),
        ("Ada", 2, "20.50", "1, 2"),
        ("Linus", 1, "3.00", "5"),
    ]
    assert [row.name for row in queries.spending_by_user(sort="name")] == [
        "Ada",
        "Grace",
        "Linus",
    ]


def test_a_team_is_summed_per_month() -> None:
    red = db.session.get_one(Team, 1)

    assert rows(queries.monthly(red)) == [
        ("2026-01", '{"orders":1,"cents":1250}'),
        ("2026-02", '{"orders":2,"cents":4800}'),
    ]


def test_orders_join_their_user_only_when_asked() -> None:
    assert rows(queries.filtered_orders()) == [
        (1, "paid"),
        (2, "shipped"),
        (3, "paid"),
        (5, "paid"),
    ]
    assert rows(queries.filtered_orders(user_name="Linus", include_unpaid=True)) == [
        (4, "cancelled"),
        (5, "paid"),
    ]


def test_targets_travel_as_a_table_of_values() -> None:
    assert rows(queries.targets([(1, 3), (2, 5)])) == [("blue", 5, 1), ("red", 3, 3)]


def test_each_status_asked_for_is_counted() -> None:
    assert rows(queries.orders_per_status(["paid", "refunded", "shipped"])) == [
        ("paid", 3),
        ("refunded", 0),
        ("shipped", 1),
    ]


def test_the_top_spenders_of_each_team_are_ranked() -> None:
    assert rows(queries.top_spenders(1)) == [
        ("blue", "Linus", 1, "3.00"),
        ("red", "Grace", 1, "40.00"),
    ]
    assert [(row.team, row.name, row.place) for row in queries.top_spenders(2)] == [
        ("blue", "Linus", 1),
        ("red", "Grace", 1),
        ("red", "Ada", 2),
    ]


def test_a_table_name_is_written_only_when_it_is_one_listed() -> None:
    assert queries.count_rows("orders") == 5

    with pytest.raises(InlineValueError):
        queries.count_rows("teams; DROP TABLE users")


def test_a_sort_column_is_one_of_those_listed() -> None:
    assert [row.email for row in queries.users_sorted_by("email")] == [
        "ada@example.com",
        "grace@example.com",
        "linus@example.com",
        "old@example.com",
    ]

    with pytest.raises(UnknownIdentifierError):
        queries.users_sorted_by("password")


def test_each_database_reports_its_version_its_own_way() -> None:
    assert queries.version().count(".") == 2
