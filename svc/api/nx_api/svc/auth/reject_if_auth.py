from attrs import define

from nx_api.svc.auth.exc import ExcAlreadyAuth
from nx_api.svc.jwt.schemas import AccessToken


@define
class RejectIfAuth:
    _access_token: AccessToken | None

    def __attrs_post_init__(self):
        if self._access_token:
            raise ExcAlreadyAuth()
