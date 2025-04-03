from dishka import Provider, provide, Scope
from itsdangerous import URLSafeTimedSerializer

from .abstract import IUrlTokenSvc
from .config import UrlTokenConfig
from .service import UrlTokenSvc


class UrlTokenProv(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> UrlTokenConfig:
        return UrlTokenConfig()

    @provide(scope=Scope.APP)
    def url_serializer(self, config: UrlTokenConfig) -> URLSafeTimedSerializer:
        return URLSafeTimedSerializer(secret_key=config.SECRET_KEY, salt=config.SALT)

    service = provide(UrlTokenSvc, scope=Scope.APP, provides=IUrlTokenSvc)
