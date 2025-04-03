from nx_api.infra.db import models as m
from nx_api.infra.db.repo import Repo


class Lead(Repo[m.Lead]):
    pass
