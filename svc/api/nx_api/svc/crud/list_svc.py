from typing import Generic, Sequence

import sqlalchemy as sa
from attrs import define
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from attrs import field

from nx_api.svc.crud.list_abc import IListSvc
from nx_api.svc.crud.query_utils import QueryUtils
from nx_api.svc.crud.types_ import R, M, LP, ListSlice, PageParams


@define
class ListSvc(IListSvc, Generic[R, M, LP]):
    _db_sess: AsyncSession

    _R = field(init=False)
    _M = field(init=False)
    _LP = field(init=False)

    def __attrs_post_init__(self):
        self._R, self._M, self._LP = self.__orig_bases__[0].__args__

    async def __call__(self, params: LP) -> ListSlice[R]:
        await self._set_stmt()

        await self._apply_load_opts()

        params = params.model_dump(exclude_none=True)
        search = params.pop("search", None)
        order = params.pop("order", None)
        pagination = PageParams(limit=params.pop("limit"), offset=params.pop("offset"))

        if search:
            await self._apply_search(search)

        await self._apply_filters(params)
        await self._apply_order(order)

        count = await self._count()
        await self._paginate(pagination)

        items = await self._execute()

        return ListSlice[self._R](
            items=items, total=count, limit=pagination.limit, offset=pagination.offset
        )

    async def _set_stmt(self) -> None:
        self._stmt = sa.select(self._M)

    async def _execute(self) -> Sequence[M]:
        res = await self._db_sess.execute(self._stmt)
        objects = res.scalars().all()
        return objects

    async def _apply_order(self, order: list[str]) -> None:
        if order:
            order = QueryUtils.parse_sort(self._M, order)
            self._stmt = self._stmt.order_by(*order)
        else:
            if attr := getattr(self._M, "created_at", None):
                self._stmt = self._stmt.order_by(desc(attr))

    async def _apply_filters(self, filters) -> None:
        filters = QueryUtils.parse_filters(self._M, filters)
        self._stmt = self._stmt.filter(*filters)

    async def _apply_search(self, search: str) -> None:
        pass

    async def _apply_load_opts(self) -> None:
        self._stmt = self._stmt.options(*self._R.load_opts()())

    async def _count(self) -> int:
        count_stmt = sa.select(sa.func.count()).select_from(self._stmt.subquery())
        count = (await self._db_sess.execute(count_stmt)).scalar()
        return count

    async def _paginate(self, pagination: PageParams) -> None:
        self._stmt = self._stmt.limit(pagination.limit).offset(pagination.offset)
