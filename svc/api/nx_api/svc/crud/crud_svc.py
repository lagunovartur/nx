import copy
from typing import Any, Generic

from attrs import define
from sqlalchemy.ext.asyncio import AsyncSession

from nx_api.svc.crud.crud_abc import ICrudSvc
from nx_api.svc.crud.types_ import C, R, U, RP


@define
class CrudSvc(ICrudSvc, Generic[C, R, U, RP]):
    _db_sess: AsyncSession
    _repo: RP

    def __attrs_post_init__(self):
        self._C, self._R, self._U, self._RP = self.__orig_bases__[0].__args__

    @property
    def _model(self):
        return self._repo.model

    async def create(
        self,
        dto: C,
    ) -> R:
        return await self._upsert(dto)

    async def update(
        self,
        dto: U,
    ) -> R:
        return await self._upsert(dto)

    async def _upsert(
        self,
        dto: C | U,
    ) -> R:
        is_new = not isinstance(dto, self._U)

        if is_new:
            obj = await self._repo.add(**dto.model_dump())
            cur_obj = None
        else:
            id_ = getattr(dto, "id", None)
            if not id_:
                raise AttributeError("dto has no <id> attribute")

            obj = await self._repo.get(id_)
            self._db_sess.expunge(obj)
            cur_obj = copy.deepcopy(obj)
            obj = await self._repo.update(obj, **dto.model_dump())

        await self._before_flush(obj, dto, cur_obj)
        await self._db_sess.flush()

        await self._before_commit(obj, dto, cur_obj)
        await self._db_sess.commit()

        self._db_sess.expunge(obj)

        return await self.get(obj.id)

    async def get(
        self,
        pk: Any,
    ) -> R:
        opts = self._R.load_opts()()
        obj = await self._repo.one(id=pk, opts=opts)
        dto = self._R.model_validate(obj)
        return dto

    async def delete(self, pk) -> None:
        await self._repo.delete(pk)
        await self._db_sess.commit()

    async def _before_flush(self, obj, dto: C | U, cur_obj=None) -> None:
        pass

    async def _before_commit(self, obj, dto: C | U, cur_obj=None) -> None:
        pass
