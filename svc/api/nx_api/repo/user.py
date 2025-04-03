from nx_api.infra.db import models as m
from nx_api.infra.db.repo import Repo
from nx_api.utils.pydantic.validators.email import is_email
from nx_api.utils.pydantic.validators.phone import is_phone


class User(Repo[m.User]):

    async def get_by_username(self, username: str) -> m.User | None:

        if is_phone(username):
            return await self.one_or_none(phone=username)
        elif is_email(username):
            return await self.one_or_none(email=username)
        else:
            raise ValueError("Invalid username")

