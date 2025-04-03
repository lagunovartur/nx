from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import AsyncContainer
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    ioc: AsyncContainer = app.state.dishka_container
    yield
    await ioc.close()
