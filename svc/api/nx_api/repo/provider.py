from dishka import Provider, provide_all, Scope

from .user import User
from .refresh_token import RefreshToken
from .auth_sess import AuthSess
from .lead import Lead


class RepoProv(Provider):
    scope = Scope.REQUEST

    pd = provide_all(User, RefreshToken, AuthSess, Lead)
