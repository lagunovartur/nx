import re
from functools import partial
from typing import Annotated

from pydantic import BeforeValidator


def _validator(value: str) -> str:
    if not is_phone(value):
        raise ValueError("Phone number must consist of 11 digits")
    return value


def is_phone(value: str) -> bool:
    regex = r"^\d{11}$"
    return bool(re.match(regex, value))


Phone = Annotated[
    str,
    BeforeValidator(partial(_validator)),
]
