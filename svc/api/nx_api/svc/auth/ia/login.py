from attrs import define
import nx_api.infra.db.models as m

import nx_api.dto as d
import nx_api.repo as r
from nx_api.svc.auth.exc import ExcInvalidCreds
from nx_api.svc.auth.pwd_crypt import IPwdCrypt
from nx_api.svc.auth.reject_if_auth import RejectIfAuth
from nx_api.svc.auth.svc.session.ia.open import OpenSessIA


@define
class LoginIA:
    _user_repo: r.User
    _crypt: IPwdCrypt
    _open_sess: OpenSessIA
    _not_auth: RejectIfAuth

    async def __call__(self, dto: d.Login) -> None:
        user = await self._authenticate(dto)
        await self._open_sess(user.id)

    async def _authenticate(self, dto: d.Login) -> m.User:
        user = await self._user_repo.get_by_username(dto.username)
        if not user:
            raise ExcInvalidCreds()

        if not self._crypt.verify(dto.password, user.password):
            raise ExcInvalidCreds()

        return user

