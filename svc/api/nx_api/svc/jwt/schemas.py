import datetime as dt
from uuid import uuid4
from typing import ClassVar
from pydantic import BaseModel
from pydantic import Field

from nx_api.utils.pydantic.validators import UUID, Timestamp

_now = lambda: dt.datetime.now(tz=dt.timezone.utc)


class JwtPayload(BaseModel):
    jti: UUID = Field(description="jwt token identifier", default_factory=uuid4)
    iat: Timestamp = Field(
        default_factory=_now, description="issued at момент издания unix time"
    )
    typ: str = Field(description="тип токена", default="jwt")
    knd: str = Field(description="вид токена refresh или access")
    exp: Timestamp = Field(
        description="expired действует до unix time", default_factory=_now
    )
    iss: str = Field(default="http://localhost", description="issuer издатель")

    sub: UUID = Field(description="subject идентификатор пользователя")
    sid: UUID = Field(description="идентификатор сессии", default_factory=uuid4)
    ttl: int = Field(description="Сколько минут живет токен", default=15, exclude=True)

    def model_post_init(self, __context):
        self.exp = self.iat + dt.timedelta(minutes=self.ttl)


class JwtToken(BaseModel):
    encoded: str
    payload: JwtPayload


class AccessToken(JwtToken):
    knd: str = Field(description="вид токена refresh или access", default="access")
    COOKIE_KEY: ClassVar[str] = "X-Access-Token"


class RefreshToken(JwtToken):
    knd: str = Field(description="вид токена refresh или access", default="refresh")
    COOKIE_KEY: ClassVar[str] = "X-Refresh-Token"


class JwtPair(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken
