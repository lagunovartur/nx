import re
from functools import partial
from typing import Annotated

from pydantic import BeforeValidator


def _validator(value: str) -> str:
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(regex, value):
        raise ValueError("Invalid email format")
    return value.lower()


Email = Annotated[
    str,
    BeforeValidator(partial(_validator)),
]
