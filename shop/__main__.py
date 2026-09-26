"""Run every query once, and print what it returns.

```console
$ python -m shop.seed
$ python -m shop
```
"""

from datetime import datetime

from . import queries
from .db import db
from .models import Team

with db.connect():
    red = db.session.get_one(Team, 1)
    runs = {
        "search_users(q='a', sort='name.desc')": queries.search_users(
            q="a", sort="name.desc"
        ),
        "users_owned_by(teams=[2])": queries.users_owned_by(teams=[2]),
        "users_of_team(red)": queries.users_of_team(red),
        "recent_orders(since=February)": queries.recent_orders(
            since=datetime(2026, 2, 1)
        ),
        "spending_by_user()": queries.spending_by_user(),
        "monthly(red)": queries.monthly(red),
        "filtered_orders(user_name='Linus', include_unpaid=True)": queries.filtered_orders(
            user_name="Linus", include_unpaid=True
        ),
        "targets([(1, 3), (2, 5)])": queries.targets([(1, 3), (2, 5)]),
        "count_rows('orders')": queries.count_rows("orders"),
        "users_sorted_by('email')": queries.users_sorted_by("email"),
        "version()": queries.version(),
    }
    for call, result in runs.items():
        print(f"{call}\n    {result}")  # noqa: T201
