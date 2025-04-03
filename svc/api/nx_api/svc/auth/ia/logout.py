from attrs import define
from fr_lib.utils.result import Result
from fr_lib.svc.jwt.schemas import RefreshToken
from nx_api.svc.auth.svc.session.ia.close import CloseSessIA


@define
class LogoutIA:
    _token: Result[RefreshToken]
    _sess_close: CloseSessIA

    async def __call__(self) -> None:
        if self._token.is_err:
            return await self._sess_close()

        token = self._token.value
        await self._sess_close(token.payload.sid)
