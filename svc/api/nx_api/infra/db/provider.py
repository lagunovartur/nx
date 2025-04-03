from typing import AsyncIterator, Iterator

from dishka import Provider, Scope, provide
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from nx_api.infra.db.config import DbConfig


class DbProv(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> DbConfig:
        return DbConfig()

    @provide(scope=Scope.APP)
    def sync_engine(self, config: DbConfig) -> Engine:
        return create_engine(
            config.SYNC_URL,
            echo=config.ECHO,
            future=True,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW,
        )

    @provide(scope=Scope.APP)
    def async_engine(self, config: DbConfig) -> AsyncEngine:
        print(config.model_dump(mode="json"))

        return create_async_engine(
            config.ASYNC_URL,
            echo=config.ECHO,
            future=True,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW,
        )

    @provide(scope=Scope.APP)
    def sync_session_factory(self, engine: Engine) -> sessionmaker[Session]:
        return sessionmaker(bind=engine)

    @provide(scope=Scope.APP)
    def async_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST)
    def session(self, sess_factory: sessionmaker[Session]) -> Iterator[Session]:
        with sess_factory() as sess:
            yield sess

    @provide(scope=Scope.REQUEST)
    async def async_session(
        self, sess_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with sess_factory() as sess:
            yield sess
