from dishka import Provider, provide_all, Scope

from .user import User
from .chat import Chat
from .message import Message


class RepoProv(Provider):
    scope = Scope.REQUEST

    pd = provide_all(User, Chat, Message)
