import re
from functools import partial
from typing import Annotated

from pydantic import BeforeValidator


def _validator(value: str) -> str:
    if not is_password(value):
        raise ValueError(
            "Password must be at least 8 characters long and include uppercase, lowercase, digits, and special characters."
        )
    return value


def is_password(value: str) -> bool:
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]).{8,}"
    return bool(re.match(regex, value))


Password = Annotated[
    str,
    BeforeValidator(partial(_validator)),
]
