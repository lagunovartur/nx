from uuid import UUID

from attrs import define
from sqlalchemy.ext.asyncio import AsyncSession

import nx_api.repo as r
import nx_api.infra.db.models as m
from nx_api.svc.jwt.abstract import IJwtSetter


@define
class CloseSessIA:
    _sess_repo: r.AuthSess
    _jwt_setter: IJwtSetter
    _db_sess: AsyncSession

    async def __call__(
        self,
        session_id: UUID | None = None,
        status: m.SessStatus = m.SessStatus.COMPLETED,
    ) -> None:
        self._jwt_setter.unset()
        if session_id:
            await self._sess_repo.update(session_id, status=status)

        await self._db_sess.commit()

