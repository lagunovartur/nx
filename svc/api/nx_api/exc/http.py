from copy import deepcopy
from typing import Type
from fastapi import Request
from fastapi.responses import JSONResponse
from typing import cast


class JsonExample(dict):
    def __init__(self, cls: Type):
        super().__init__()
        self["content"] = {
            "application/json": {
                "examples": {
                    cls.__name__: {
                        "value": {
                            "type": cls.__name__,
                            **{
                                key: value
                                for key, value in cls.__dict__.items()
                                if not (key.startswith("__") and key.endswith("__"))
                            },
                        }
                    }
                }
            }
        }

    @property
    def _examples(self):
        return self["content"]["application/json"]["examples"]

    @_examples.setter
    def _examples(self, value):
        self["content"]["application/json"]["examples"] = value

    def __or__(self, other):
        if isinstance(other, self.__class__):
            new = deepcopy(self)
            new._examples = self._examples | other._examples
            return new
        return super().__or__(other)


class ExcHttp(Exception):
    status_code = 500
    message: str = None
    type: str = None

    def __init__(
        self,
        status_code: int | None = None,
        message: str = None,
        headers: dict[str, str] | None = None,
        **detail,
    ) -> None:
        self.status_code = status_code or self.status_code
        self.payload = detail | {
            "message": message or self.message,
            "type": self.__class__.__name__,
        }
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code}: {self.payload}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return (
            f"{class_name}(status_code={self.status_code!r}, detail={self.payload!r})"
        )

    @classmethod
    def example(cls) -> JsonExample:
        return JsonExample(cls)


class ExcNotFound(ExcHttp):
    status_code = 404
    message = "Объект не найден"


class ExcDuplicateKey(ExcHttp):
    status_code = 409
    message = "Ключ уже существует"


def http_handler(request: Request, exc: Exception) -> JSONResponse:
    exc = cast(ExcHttp, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.payload,
        headers=exc.headers,
    )
