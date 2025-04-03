from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UuidPk, Timestamp

if TYPE_CHECKING:
    from .user import User


class LeadStatus(StrEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    IN_PROGRESS = "IN_PROGRESS"


class Lead(UuidPk, Timestamp, Base):
    __tablename__ = "leads"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="leads")
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, native_enum=False),
        nullable=False,
        server_default=LeadStatus.OPEN,
    )
