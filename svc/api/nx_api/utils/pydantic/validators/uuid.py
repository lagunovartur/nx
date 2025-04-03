import uuid
from typing import Annotated

from pydantic import BeforeValidator, PlainSerializer

UUID = Annotated[
    uuid.UUID,
    BeforeValidator(lambda v: uuid.UUID(v) if isinstance(v, str) else v),
    PlainSerializer(lambda v: str(v)),
]
