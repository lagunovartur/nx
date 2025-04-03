from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import mapped_column

from .base import Base
from nx_api.infra.db.models.mixins import UuidPk, Timestamp

if TYPE_CHECKING:
    from .auth_sess import AuthSess
    from .lead import Lead


class User(Base, UuidPk, Timestamp):
    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(50), unique=True, nullable=False
    )
    phone: orm.Mapped[str] = orm.mapped_column(
        sa.String(11), unique=True, nullable=False
    )
    password: orm.Mapped[str] = mapped_column(sa.String(60), nullable=False)
    email_verified: orm.Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, server_default=sa.text("false")
    )
    sessions: orm.Mapped[list["AuthSess"]] = orm.relationship(
        back_populates="user", lazy="noload"
    )
    leads: orm.Mapped[list["Lead"]] = orm.relationship(
        back_populates="user", lazy="noload"
    )
