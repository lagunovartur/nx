from attrs import define
from sqlalchemy.ext.asyncio import AsyncSession
import nx_api.dto as d
import nx_api.repo as r
import nx_api.infra.db.models as m
from nx_api.svc.auth.pwd_crypt import IPwdCrypt


@define
class RegisterIA:
    _user_repo: r.User
    _db_sess: AsyncSession
    _crypt: IPwdCrypt

    async def __call__(self, dto: d.NewUser) -> m.User:
        user = await self._user_repo.add(
            password=self._crypt.hash(dto.password),
            **dto.model_dump(exclude={"password"}),
        )
        await self._db_sess.commit()
        return user
