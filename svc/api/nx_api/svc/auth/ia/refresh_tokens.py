from attrs import define
from sqlalchemy.ext.asyncio import AsyncSession
import nx_api.infra.db.models as m
import nx_api.repo as r
from nx_api.svc.jwt.schemas import RefreshToken
from nx_api.svc.auth.svc.session.ia.close import CloseSessIA
from nx_api.svc.jwt.abstract import IJwtSvc, IJwtSetter
from nx_api.utils.result import Result


@define
class RefreshTokensIA:
    _refresh_token: Result[RefreshToken]
    _token_repo: r.RefreshToken
    _jwt_svc: IJwtSvc
    _sess_close: CloseSessIA
    _jwt_setter: IJwtSetter
    _db_sess: AsyncSession

    async def __call__(self) -> None:
        if self._refresh_token.is_err:
            raise self._refresh_token.err

        refresh_token = self._refresh_token.value
        if not await self._is_active(refresh_token):
            return await self._sess_close(
                refresh_token.payload.sid, m.SessStatus.HACKED
            )

        return await self._refresh_pair(refresh_token)

    async def _is_active(self, refresh_token: RefreshToken) -> bool:
        active_token = await self._token_repo.get_active(refresh_token.payload.sid)
        if active_token is None:
            return False
        return active_token.id == refresh_token.payload.jti

    async def _refresh_pair(self, refresh_token: RefreshToken) -> None:
        new_tokens = self._jwt_svc.refresh_pair(refresh_token)
        new_payload = new_tokens.refresh_token.payload

        await self._token_repo.add(
            id=new_payload.jti,
            parent_id=refresh_token.payload.jti,
            session_id=new_payload.sid,
            expires_at=new_payload.exp,
        )

        await self._db_sess.commit()

        return self._jwt_setter.set(new_tokens)
