from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import ForeignKey

from nx_api.infra.db.models.base import Base
from nx_api.infra.db.models.mixins import UuidPk, CreatedAt

if TYPE_CHECKING:
    from nx_api.infra.db.models.auth_sess import AuthSess


class RefreshToken(Base, UuidPk, CreatedAt):
    session_id: orm.Mapped[UUID] = orm.mapped_column(
        ForeignKey("auth_sess.id", ondelete="CASCADE")
    )
    session: orm.Mapped["AuthSess"] = orm.relationship(
        back_populates="tokens", lazy="noload"
    )
    parent_id: orm.Mapped[UUID] = orm.mapped_column(
        ForeignKey("refresh_token.id", ondelete="SET NULL"), nullable=True
    )
    parent: orm.Mapped["RefreshToken"] = orm.relationship(
        "RefreshToken", remote_side="RefreshToken.id", lazy="noload"
    )
    expires_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.TIMESTAMP(timezone=True), nullable=False
    )
