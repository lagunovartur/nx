from abc import ABC, abstractmethod
from typing import Generic
from typing import Type, TypeVar
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field

from nx_api.utils.pydantic.validators import UUID

T = TypeVar("T", bound=BaseModel)


class UrlPayload(BaseModel, Generic[T]):
    id: UUID = Field(default_factory=uuid4)
    action: str
    payload: T


class IUrlTokenSvc(ABC):
    @abstractmethod
    async def encode(self, payload: T) -> str:
        pass

    @abstractmethod
    async def decode(
        self, token: str, payload_type: Type[T], ttl: int = 15
    ) -> UrlPayload[T]:
        pass
