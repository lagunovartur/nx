from nx_api.core.provider import CoreProv
from nx_api.infra.db.provider import DbProv
from nx_api.infra.redis.provider import RedisProv
from nx_api.infra.smtp.provider import SmtpProv
from nx_api.repo.provider import RepoProv
from nx_api.svc.auth.provider import AuthProv
from nx_api.svc.jwt.provider import JwtProv
from nx_api.svc.url_token.provider import UrlTokenProv
from nx_api.svc.user.provider import UserProv
from nx_api.utils.ioc_builder import IocBuilder


def ioc_builder() -> IocBuilder:
    providers = [
        DbProv(),
        CoreProv(),
        RepoProv(),
        AuthProv(),
        JwtProv(),
        UserProv(),
        SmtpProv(),
        UrlTokenProv(),
        RedisProv(),
    ]

    builder = IocBuilder(*providers)

    return builder
