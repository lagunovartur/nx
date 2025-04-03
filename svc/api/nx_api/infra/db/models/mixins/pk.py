from sqlalchemy import BigInteger, UUID, text
from sqlalchemy.orm import Mapped, mapped_column
import uuid


class SerialPk:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class UuidPk:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
