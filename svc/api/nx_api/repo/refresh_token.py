from uuid import UUID
from nx_api.infra.db import models as m

import sqlalchemy as sa
from attr import define
from sqlalchemy.orm import contains_eager

from nx_api.infra.db.repo import Repo


@define
class RefreshToken(Repo[m.RefreshToken]):
    async def get_active(self, session_id: UUID) -> m.RefreshToken | None:
        stmt = (
            sa.select(m.RefreshToken)
            .join(m.AuthSess)
            .options(contains_eager(m.RefreshToken.session))
            .where(
                sa.and_(
                    m.RefreshToken.session_id == session_id,
                    m.AuthSess.status == m.SessStatus.ACTIVE,
                )
            )
            .order_by(m.RefreshToken.expires_at.desc())
            .limit(1)
        )

        return await self._db_sess.scalar(stmt)
