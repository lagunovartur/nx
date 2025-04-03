import datetime as dt
from dataclasses import dataclass

from pydantic import ConfigDict

import nx_api.infra.db.models as m

from nx_api.utils.pydantic.base_model import BaseModel
from nx_api.utils.pydantic.validators import UUID

from .user import UserBase
from ..svc.crud.types_ import BaseLP


class BaseLead(BaseModel):
    _model = m.Lead
    comment: str | None = None


class LeadBase(BaseLead):
    id: UUID
    created_at: dt.datetime


class NewLead(BaseLead):
    id: UUID | None = None
    user_id: UUID

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "94203c3e-2a94-4638-ae60-77a9a875542d",
                    "user_id": "05095dd9-57d2-4911-9b1d-638a60bdd653",
                    "comment": "Обслуживаем что то",
                },
            ]
        }
    )




class EditLead(BaseLead):
    id: UUID
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


@dataclass
class LeadLP(BaseLP):
    user_id__in: list[UUID] | None = None
