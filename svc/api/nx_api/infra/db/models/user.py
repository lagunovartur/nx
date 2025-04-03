from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UuidPk
from .mixins.timestamp import Timestamp
from .user_chat import user_chat

if TYPE_CHECKING:
    from .chat import Chat
    from .message import Message


class User(Base, UuidPk, Timestamp):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(String(60), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    chats: Mapped[List["Chat"]] = relationship(
        "Chat", secondary=user_chat, back_populates="users"
    )
    messages: Mapped[List["Message"]] = relationship(
        back_populates="sender", lazy="noload"
    )


class CurrentUser(User):
    __abstract__ = True
