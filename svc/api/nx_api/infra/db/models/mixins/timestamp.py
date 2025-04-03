import datetime as dt

import sqlalchemy as sa
from sqlalchemy import orm as orm


class CreatedAt:
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )


class UpdatedAt:
    updated_at: orm.Mapped[dt.datetime | None] = orm.mapped_column(
        sa.DateTime(timezone=True),
        onupdate=sa.func.now(),
        nullable=True,
        default=None,
    )


class Timestamp:
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
    updated_at: orm.Mapped[dt.datetime | None] = orm.mapped_column(
        sa.DateTime(timezone=True),
        onupdate=sa.func.now(),
        nullable=True,
        default=None,
    )
