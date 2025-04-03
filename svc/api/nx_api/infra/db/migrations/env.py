import asyncio
import os
from contextlib import asynccontextmanager
from logging.config import fileConfig
from types import ModuleType
from typing import AsyncIterator

from dishka import make_async_container
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


from nx_api.infra.db import models
from nx_api.infra.db.provider import DbProv


@asynccontextmanager
async def engine_manager() -> AsyncIterator[AsyncEngine]:
    container = make_async_container(DbProv())
    engine = await container.get(AsyncEngine)

    try:
        yield engine
    finally:
        await engine.dispose()


@asynccontextmanager
async def session_manager() -> AsyncIterator[AsyncSession]:
    container = make_async_container(DbProv())
    factory = await container.get(async_sessionmaker[AsyncSession])

    async with factory() as session:
        yield session


def alembic_context(conn: Connection) -> ModuleType:
    from alembic import context

    os.umask(0)

    target_metadata = models.Base.metadata

    context.configure(
        connection=conn,
        target_metadata=target_metadata,
    )

    config_file = context.config.config_file_name
    if config_file:
        fileConfig(config_file)

    return context


def migrate_sync(conn: Connection):
    context = alembic_context(conn)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    async with engine_manager() as engine:
        async with engine.begin() as conn:
            await conn.run_sync(migrate_sync)


asyncio.run(run_migrations_online())
