from abc import ABC, abstractmethod
from typing import Generic, Sequence

from attrs import define, field
from sqlalchemy.sql.selectable import Select

from nx_api.svc.crud.types_ import R, M, LP, ListSlice, PageParams


@define
class IListSvc(ABC, Generic[R, M, LP]):
    _stmt: Select = field(init=False)

    @abstractmethod
    async def __call__(self, params: LP) -> ListSlice[R]:
        pass

    @abstractmethod
    async def _set_stmt(self) -> None:
        pass

    @abstractmethod
    async def _execute(self) -> Sequence[M]:
        pass

    @abstractmethod
    async def _apply_order(self, order) -> None:
        pass

    @abstractmethod
    async def _apply_filters(self, filters) -> None:
        pass

    @abstractmethod
    async def _apply_search(self, search: str) -> None:
        pass

    @abstractmethod
    async def _apply_load_opts(self) -> None:
        pass

    @abstractmethod
    async def _count(self) -> int:
        pass

    @abstractmethod
    async def _paginate(self, pagination: PageParams) -> None:
        pass
