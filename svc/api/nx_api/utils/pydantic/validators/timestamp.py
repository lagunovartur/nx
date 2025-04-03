from typing import Annotated
import datetime as dt
from pydantic import BeforeValidator, PlainSerializer


Timestamp = Annotated[
    dt.datetime,
    BeforeValidator(
        lambda v: dt.datetime.fromtimestamp(v) if isinstance(v, (int, float)) else v
    ),
    PlainSerializer(lambda v: int(v.timestamp())),
]
