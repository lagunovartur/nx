from enum import Enum, auto
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as orm

from nx_api.infra.db.models.base import Base
from nx_api.infra.db.models.mixins import UuidPk, Timestamp

if TYPE_CHECKING:
    from nx_api.infra.db.models.refresh_token import RefreshToken
    from nx_api.infra.db.models.user import User



class SessStatus(Enum):
    ACTIVE = auto()
    COMPLETED = auto()
    HACKED = auto()


class AuthSess(Base, UuidPk, Timestamp):

    tokens: orm.Mapped[list["RefreshToken"]] = orm.relationship(
        back_populates="session", passive_deletes=True
    )

    user_id: orm.Mapped[UUID] = orm.mapped_column(
        sa.ForeignKey("user.id", ondelete="CASCADE")
    )
    user: orm.Mapped["User"] = orm.relationship(
        back_populates="sessions", lazy="noload"
    )

    ip_addr: orm.Mapped[str] = orm.mapped_column(sa.String(45))

    status: orm.Mapped[SessStatus] = orm.mapped_column(
        sa.Enum(SessStatus, native_enum=False),
        default=SessStatus.ACTIVE,
        nullable=False,
    )
