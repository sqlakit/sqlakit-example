"""The plugin runs each test marked `db` in a transaction that rolls back."""

import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest

from app.models import Model
from app.seed import seed


@pytest.fixture(scope="session")
def sqlakit_base() -> type[Model]:
    return Model


@pytest.fixture
def shop() -> None:
    """The rows of `app.seed`, in the test's transaction."""
    seed()
