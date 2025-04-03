import datetime as dt
from enum import StrEnum

from pydantic import ConfigDict, Field

import nx_api.infra.db.models as m
from nx_api.utils.pydantic.base_model import BaseModel
from nx_api.utils.pydantic.validators import UUID
from .user import UserBase
from ..svc.crud.types_ import BaseLP


class BaseLead(BaseModel):
    _model = m.Lead
    comment: str | None = None
    name: str


class LeadBase(BaseLead):
    id: UUID
    created_at: dt.datetime
    status: m.LeadStatus


class NewLead(BaseLead):
    id: UUID | None = None
    user_id: UUID | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "заявка на покупку",
                    "id": "94203c3e-2a94-4638-ae60-77a9a875542d",
                    "comment": "Обслуживаем что то",
                },
            ]
        }
    )


class EditLead(BaseLead):
    id: UUID
    name: str | None = None
    user_id: UUID | None = None
    status: m.LeadStatus | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "94203c3e-2a94-4638-ae60-77a9a875542d",
                    "status": "CLOSED",
                },
            ]
        }
    )


class Lead(LeadBase):
    user: UserBase


class ListOrder(StrEnum):
    created_at = "created_at__desc"
    name = "name__asc"


class LeadLP(BaseLP):
    user_id__in: list[UUID] | None = None
    order: list[ListOrder] = Field(default_factory=list)
