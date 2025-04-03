from dishka import Provider, from_context, provide, Scope, provide_all
from fastapi import Request
from passlib.context import CryptContext

from .exc import ExcRefreshTokenNotSent, ExcAccessTokenNotSent
from .guard import AuthGuard
from .ia.login import LoginIA
from .ia.verify_email import VerifyEmailIA
from .ia.logout import LogoutIA
from .ia.refresh_tokens import RefreshTokensIA
from .ia.register import RegisterIA
from .ia.verify_email_end import VerifyEmailEndIA
from .pwd_crypt import PwdCrypt, IPwdCrypt
from .reject_if_auth import RejectIfAuth
from .svc.session.ia.open import OpenSessIA
from .svc.session.ia.close import CloseSessIA
from typing import cast

from ..jwt.abstract import IJwtSvc
from ..jwt.schemas import AccessToken, RefreshToken
from ...utils.result import Result


class AuthProv(Provider):
    scope = Scope.REQUEST

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def access_token(self, request: Request) -> AccessToken:
        token = request.state.access_token
        if not token:
            raise ExcAccessTokenNotSent()
        return cast(AccessToken, token)

    @provide(scope=Scope.REQUEST)
    def access_token_or_none(self, request: Request) -> AccessToken | None:
        return request.state.access_token

    @provide(scope=Scope.REQUEST)
    def refresh_token(self, request: Request, jwt: IJwtSvc) -> Result[RefreshToken]:
        encoded = request.cookies.get(RefreshToken.COOKIE_KEY)
        if not encoded:
            return Result[RefreshToken](exc=ExcRefreshTokenNotSent())
        try:
            token: RefreshToken = jwt.decode(encoded)
            return Result[RefreshToken](value=token)
        except Exception as exc:
            return Result[RefreshToken](exc=exc)

    @provide(scope=Scope.APP)
    def crypt_context(self) -> CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    pwd_crypt = provide(PwdCrypt, scope=Scope.APP, provides=IPwdCrypt)

    guard = provide(AuthGuard, scope=Scope.APP)

    fs = provide_all(
        LoginIA,
        RegisterIA,
        VerifyEmailIA,
        OpenSessIA,
        CloseSessIA,
        LogoutIA,
        RefreshTokensIA,
        VerifyEmailEndIA,
        RejectIfAuth,
    )

    # active_sess_ia = provide(ActiveSessIA, scope=Scope.REQUEST)
