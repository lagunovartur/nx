from dishka import Provider, provide, Scope

from .abstract import IJwtSvc, IJwtSetter
from .config import JwtConfig
from .service import JwtSvc, JwtSetter


class JwtProv(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> JwtConfig:
        return JwtConfig()

    token_svc = provide(JwtSvc, scope=Scope.APP, provides=IJwtSvc)
    token_setter = provide(JwtSetter, scope=Scope.REQUEST, provides=IJwtSetter)
