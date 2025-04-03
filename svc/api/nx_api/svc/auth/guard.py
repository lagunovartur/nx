import re

from attr import define
from fastapi import Request

from nx_api.svc.auth.exc import ExcNotAuth
from nx_api.svc.jwt.abstract import IJwtSvc
from nx_api.svc.jwt.schemas import AccessToken


@define
class AuthGuard:
    UNPROTECTED = [
        r"auth/",
    ]

    _jwt: IJwtSvc

    def __call__(self, request: Request) -> None:
        request.state.access_token = None

        access_token = None
        protected_path = self._is_protected(request.url.path)

        encoded_token = request.cookies.get(AccessToken.COOKIE_KEY, None)
        if protected_path and not encoded_token:
            raise ExcNotAuth()

        if encoded_token:
            try:
                access_token = self._jwt.decode(encoded_token)
            except Exception:
                if protected_path:
                    raise

        request.state.access_token = access_token

    @classmethod
    def _is_protected(cls, path: str) -> bool:
        return not any(re.search(pattern, path) for pattern in cls.UNPROTECTED)

    def __hash__(self):
        return id(self)
