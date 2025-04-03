from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base
from .mixins import UuidPk
from .mixins.timestamp import Timestamp
from .user_chat import user_chat

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Chat(Base, UuidPk, Timestamp):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    users: Mapped[List["User"]] = relationship(
        "User", secondary=user_chat, back_populates="chats"
    )
    messages: Mapped[List["Message"]] = relationship(
        back_populates="chat", lazy="noload"
    )
