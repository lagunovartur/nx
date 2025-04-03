from uuid import UUID

from attrs import define
from sqlalchemy.ext.asyncio import AsyncSession

import nx_api.repo as r
from nx_api.svc.jwt.abstract import IJwtSvc, IJwtSetter


@define
class OpenSessIA:
    _sess_repo: r.AuthSess
    _token_repo: r.RefreshToken
    _jwt_svc: IJwtSvc
    _jwt_setter: IJwtSetter
    _db_sess: AsyncSession

    async def __call__(self, user_id: UUID) -> None:
        token_pair = self._jwt_svc.token_pair(sub=user_id)
        session = await self._sess_repo.add(
            id=token_pair.refresh_token.payload.sid,
            user_id=user_id,
            ip_addr="127.0.0.1",
            # ip_addr=self._request.client.host if self._request.client else "127.0.0.1",
        )
        refresh_payload = token_pair.refresh_token.payload
        token = await self._token_repo.add(
            id=refresh_payload.jti,
            expires_at=refresh_payload.exp,
        )
        token.session = session
        await self._db_sess.commit()
        return self._jwt_setter.set(token_pair)
