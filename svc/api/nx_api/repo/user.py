from typing import Sequence

from sqlalchemy.orm.interfaces import ORMOption

from nx_api.infra.db.repo import Repo
from nx_api.infra.db import models as m
import sqlalchemy as sa


class User(Repo[m.User]):
    async def get_by_chat(
        self,
        chat_id: int,
        opts: Sequence[ORMOption] | None = None,
    ) -> Sequence[m.User]:
        opts = opts or []
        stmt = (
            sa.select(self.model)
            .select_from(m.user_chat)
            .join(self.model)
            .where(m.user_chat.c.chat_id == chat_id)
            .options(*opts)
        )
        result = await self._db_sess.execute(stmt)
        return result.scalars().all()

    # chat = await self._chat_repo.get(
    #     dto.chat_id, (orm.selectinload(self._chat_repo.model.users),)
    # )
