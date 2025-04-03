import sqlalchemy as sa
from .base import Base


user_chat = sa.Table(
    "user_chat",
    Base.metadata,
    sa.Column(
        "user_id", sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    ),
    sa.Column(
        "chat_id", sa.ForeignKey("chat.id", ondelete="CASCADE"), primary_key=True
    ),
)
