from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UuidPk, CreatedAt

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class Message(Base, UuidPk, CreatedAt):
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chat.id", ondelete="CASCADE"), index=True, nullable=False
    )
    chat: Mapped["Chat"] = relationship(back_populates="messages", lazy="noload")
    sender_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False
    )
    sender: Mapped["User"] = relationship(back_populates="messages", lazy="noload")
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=sa.text("false")
    )
