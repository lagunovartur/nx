from typing import Generic, TypeVar

T = TypeVar("T")


class Result(Generic[T]):
    def __init__(self, *, value: T | None = None, exc: Exception | None = None) -> None:
        self._value = value
        self._exc = exc

    @property
    def value(self) -> T:
        if self.is_err:
            raise ValueError("Cannot access value of an error result")
        return self._value

    @property
    def err(self) -> Exception:
        if not self.is_err:
            raise ValueError("Cannot access error of a value result")
        return self._exc

    @property
    def is_err(self) -> bool:
        return self._exc is not None
