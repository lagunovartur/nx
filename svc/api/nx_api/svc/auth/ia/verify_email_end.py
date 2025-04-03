from attrs import define
from fr_lib.svc.url_token.abstract import IUrlTokenSvc
from sqlalchemy.ext.asyncio import AsyncSession

import nx_api.repo as r
from nx_api.dto.auth import EmailReq


@define
class VerifyEmailEndIA:
    _token_svc: IUrlTokenSvc
    _user_repo: r.User
    _db_sess: AsyncSession

    async def __call__(self, token: str) -> None:

        token = await self._token_svc.decode(token, EmailReq)
        email = token.payload.email
        user = await self._user_repo.one(email=email)
        await self._user_repo.update(user, email_verified=True)
        await self._db_sess.commit()
