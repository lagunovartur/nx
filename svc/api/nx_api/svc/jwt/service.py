from fastapi import Response
from typing import Type, TypeVar
from uuid import uuid4
import jwt
from attr import define
from uuid import UUID

from nx_api.exc import ExcHttp
from nx_api.svc.jwt.abstract import IJwtSvc, IJwtSetter
from nx_api.svc.jwt.config import JwtConfig
from nx_api.svc.jwt.exc import ExcAccessTokenExpired, ExcRefreshTokenExpired
from nx_api.svc.jwt.schemas import JwtToken, JwtPair, AccessToken, RefreshToken, JwtPayload

T = TypeVar('T', bound=JwtToken)


@define
class JwtSvc(IJwtSvc):

    _config: JwtConfig
    # _iss: str = 'http://localhost'

    def token_pair(self, sub: UUID, **kwargs) -> JwtPair:

        kwargs['sub'] = sub
        kwargs['sid'] = kwargs.get('sid') or uuid4()

        return JwtPair(
            access_token=self._token(AccessToken, **kwargs),
            refresh_token=self._token(RefreshToken, **kwargs),
        )

    def refresh_pair(self, refresh_token: RefreshToken) -> JwtPair:
        kwargs = refresh_token.payload.model_dump(exclude={'iat', 'exp', 'jti', 'knd'})

        return JwtPair(
            access_token=self._token(cls=AccessToken, **kwargs),
            refresh_token=self._token(cls=RefreshToken, **kwargs),
        )

    def _token(
            self, cls: Type[T], **kwargs
    ) -> T:

        ttl = self._config.ACCESS_EXP if cls == AccessToken else self._config.REFRESH_EXP
        kwargs['ttl'] = ttl

        payload = JwtPayload(knd=cls.__name__, **kwargs)

        encoded = jwt.encode(
            payload=payload.model_dump(),
            key=self._config.SECRET_KEY,
            algorithm=self._config.ALG,
        )

        return cls(encoded=encoded, payload=payload)

    def decode(self, token: str, **options) -> JwtToken:

        def token_payload(encoded, params) -> JwtPayload:
            return JwtPayload(**jwt.decode(
                encoded,
                key=self._config.SECRET_KEY,
                algorithms=[self._config.ALG],
                options=params,
            ))

        try:
            payload = token_payload(token, options)
        except jwt.ExpiredSignatureError:
            payload = token_payload(token, options | {'verify_exp': False})
            if payload.knd == AccessToken.__name__:
                raise ExcAccessTokenExpired()
            elif payload.knd == RefreshToken.__name__:
                raise ExcRefreshTokenExpired()
            else:
                raise ValueError(payload.knd)
        except jwt.InvalidTokenError as exc:
            raise ExcHttp(400, str(exc))

        cls = globals()[payload.knd]

        return cls(payload=payload, encoded=token)

@define
class JwtSetter(IJwtSetter):

    _response: Response

    def set(self, token_pair: JwtPair) -> None:
        exp = token_pair.refresh_token.payload.exp

        self._response.set_cookie(
            key=AccessToken.COOKIE_KEY,
            value=f"{token_pair.access_token.encoded}",
            httponly=True,
            samesite="lax",
            expires=exp,
            secure=True,
        )
        self._response.set_cookie(
            key=RefreshToken.COOKIE_KEY,
            value=f"{token_pair.refresh_token.encoded}",
            httponly=True,
            path="/api/auth/refresh",
            samesite="strict",
            expires=exp,
            secure=True,
        )
        self._response.set_cookie(
            key=RefreshToken.COOKIE_KEY,
            value=f"{token_pair.refresh_token.encoded}",
            httponly=True,
            path="/api/auth/logout",
            samesite="strict",
            expires=exp,
            secure=True,
        )


    def unset(self) -> None:

        self._response.delete_cookie(AccessToken.COOKIE_KEY, path="/")
        self._response.delete_cookie(RefreshToken.COOKIE_KEY, path="/api/auth/refresh")
        self._response.delete_cookie(RefreshToken.COOKIE_KEY, path="/api/auth/logout")

