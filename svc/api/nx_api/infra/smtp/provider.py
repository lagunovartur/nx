from collections.abc import AsyncIterator

from dishka import provide, Scope, Provider
from aiosmtplib import SMTP
from .config import SmtpConfig


class SmtpProv(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> SmtpConfig:
        return SmtpConfig()

    @provide(scope=Scope.APP)
    async def client(self, config: SmtpConfig) -> AsyncIterator[SMTP]:
        async with SMTP(
            hostname=config.HOST, port=config.PORT, validate_certs=True, use_tls=True
        ) as client:
            await client.login(config.EMAIL, config.PASS)
            yield client
