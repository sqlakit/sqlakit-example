"""Create the tables and fill them with a few teams, users and orders.

```console
$ python -m app.seed
```
"""

from datetime import datetime

from .db import db
from .models import Model, Order, Team, User


def seed() -> None:
    """Add the rows every example reads, in the transaction around the call."""
    db.session.add_all(
        [
            Team(id=1, name="red"),
            Team(id=2, name="blue"),
            User(id=1, name="Ada", email="ada@example.com", team_id=1),
            User(id=2, name="Grace", email="grace@example.com", team_id=1),
            User(id=3, name="Linus", email="linus@example.com", team_id=2),
            User(id=4, name="Old", email="old@example.com", team_id=2, archived=True),
            Order(
                id=1,
                user_id=1,
                status="paid",
                total_cents=1250,
                placed_at=datetime(2026, 1, 5),
            ),
            Order(
                id=2,
                user_id=1,
                status="shipped",
                total_cents=800,
                placed_at=datetime(2026, 2, 10),
            ),
            Order(
                id=3,
                user_id=2,
                status="paid",
                total_cents=4000,
                placed_at=datetime(2026, 2, 11),
            ),
            Order(
                id=4,
                user_id=3,
                status="cancelled",
                total_cents=999,
                placed_at=datetime(2026, 2, 12),
            ),
            Order(
                id=5,
                user_id=3,
                status="paid",
                total_cents=300,
                placed_at=datetime(2026, 3, 1),
            ),
        ]
    )


if __name__ == "__main__":
    with db.transaction() as connection:
        Model.metadata.drop_all(connection)
        Model.metadata.create_all(connection)
        seed()
    print("seeded")  # noqa: T201
