from typing import TypeVar, Generic, Sequence, List

from nx_api.infra.db.models import Base
from nx_api.infra.db.repo import Repo
from nx_api.utils.pydantic.base_model import BaseModel
from pydantic import Field


class PageParams(BaseModel):
    offset: int = 0
    limit: int = 10

class BaseLP(PageParams):
    search: str | None = None
    order: List[str] = Field(default_factory=list, examples=['created_at__desc',])


C = TypeVar("C", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)
M = TypeVar("M", bound=Base)
RP = TypeVar("RP", bound=Repo)
LP = TypeVar("LP", bound=BaseLP)

D = TypeVar("D", bound=BaseModel)


class ListSlice(BaseModel, Generic[D]):
    items: Sequence[D]
    limit: int
    offset: int
    total: int
