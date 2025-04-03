from attr import define
from nx_api.infra.db import models as m
from nx_api.infra.db.repo import Repo


@define
class AuthSess(Repo[m.AuthSess]):
    pass
