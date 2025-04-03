import re
from functools import partial
from typing import Annotated

from pydantic import BeforeValidator


def _validator(value: str) -> str:
    if not is_email(value):
        raise ValueError("Invalid email format")
    return value.lower()


def is_email(value: str) -> bool:
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(regex, value))


Email = Annotated[
    str,
    BeforeValidator(partial(_validator)),
]
