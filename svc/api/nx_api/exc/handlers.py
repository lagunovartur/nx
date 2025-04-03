from fastapi import FastAPI

from nx_api.exc import ExcHttp
from nx_api.exc.http import http_handler


def add_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ExcHttp, http_handler)
