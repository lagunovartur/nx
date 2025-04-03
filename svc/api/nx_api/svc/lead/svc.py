from attrs import define
from sqlalchemy.ext.asyncio import AsyncSession

from nx_api.svc.crud.crud_svc import CrudSvc
from nx_api.svc.crud.list_svc import ListSvc
from nx_api import dto as d
from nx_api import repo as r
from nx_api.infra.db import models as m


@define
class LeadList(ListSvc[d.Lead, m.Lead, d.LeadLP]):
    _db_sess: AsyncSession


@define
class LeadSvc(CrudSvc[d.NewLead, d.Lead, d.EditLead, r.Lead]):
    _db_sess: AsyncSession
    _repo: r.Lead
