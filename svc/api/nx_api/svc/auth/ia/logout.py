from attrs import define

from nx_api.svc.auth.svc.session.ia.close import CloseSessIA
from nx_api.utils.result import Result
from nx_api.svc.jwt.schemas import RefreshToken


@define
class LogoutIA:
    _token: Result[RefreshToken]
    _sess_close: CloseSessIA

    async def __call__(self) -> None:
        if self._token.is_err:
            return await self._sess_close()

        token = self._token.value
        await self._sess_close(token.payload.sid)
