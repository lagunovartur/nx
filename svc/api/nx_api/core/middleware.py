from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https://localhost:\d+",
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        expose_headers=["Set-Cookie"],
    )
