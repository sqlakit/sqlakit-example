"""The plugin runs each test marked `db` in a transaction that rolls back."""

import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest

from shop.models import Model
from shop.seed import seed


@pytest.fixture(scope="session")
def sqlakit_base() -> type[Model]:
    return Model


@pytest.fixture
def shop() -> None:
    """The rows of `shop.seed`, in the test's transaction."""
    seed()
