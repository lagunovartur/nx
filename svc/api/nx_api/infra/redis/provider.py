from typing import AsyncIterator

from dishka import Provider, provide, Scope
from redis.asyncio import Redis

from .config import RedisConfig


class RedisProv(Provider):

    @provide(scope=Scope.APP)
    def config(self) -> RedisConfig:
        return RedisConfig()

    @provide(scope=Scope.APP)
    async def client(self, config: RedisConfig) -> AsyncIterator[Redis]:
        async with Redis(
                host=config.HOST,
                port=config.PORT,
                db=config.DB,
                encoding="utf-8",
                decode_responses=True
        ) as client:
            yield client
