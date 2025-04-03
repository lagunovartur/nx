import datetime as dt
from dataclasses import dataclass
import nx_api.infra.db.models as m

from nx_api.utils.pydantic.base_model import BaseModel
from nx_api.utils.pydantic.validators import UUID

from .user import UserBase
from ..svc.crud.types_ import BaseLP


class BaseLead(BaseModel):
    _model = m.Lead
    comment: str | None = None
    status: m.LeadStatus


class LeadBase(BaseLead):
    id: int
    created_at: dt.datetime


class NewLead(BaseLead):
    user_id: UUID


class EditLead(BaseLead):
    id: int
    user_id: int | None = None


class Lead(LeadBase):
    user: UserBase


@dataclass
class LeadLP(BaseLP):
    user_id__in: list[int] | None = None
