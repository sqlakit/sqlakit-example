"""The tables: teams, their users, and the orders the users place."""

from datetime import datetime

from sqlakit.orm import ModelMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .db import db


class Model(ModelMixin, DeclarativeBase):
    pass


Model.set_db(db)


class Team(Model):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    archived: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None]


class Order(Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str]
    total_cents: Mapped[int]
    placed_at: Mapped[datetime]
