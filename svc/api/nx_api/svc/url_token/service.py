import datetime as dt
from typing import Type

from attrs import define
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from redis.asyncio import Redis

from .abstract import UrlPayload, IUrlTokenSvc, T
from .exc import ExcInvalidToken, ExcTokenExpired, ExcTokenAlreadyUsed


@define
class UrlTokenSvc(IUrlTokenSvc):
    _url_serializer: URLSafeTimedSerializer
    _redis: Redis

    def _action_salt(self, action: str) -> str:
        base_salt = self._url_serializer.salt or "default_salt"
        return f"{base_salt}:{action}"

    async def encode(self, payload: T) -> str:
        action = payload.__class__.__name__
        url_payload = UrlPayload(action=action, payload=payload)

        redis_key = f"{payload.__class__.__name__}:{url_payload.id}"
        await self._redis.setex(redis_key, dt.timedelta(days=1), 1)

        return self._url_serializer.dumps(
            url_payload.model_dump(), salt=self._action_salt(action)
        )

    async def decode(
        self, token: str, payload_type: Type[T], ttl: int = 15
    ) -> UrlPayload[T]:
        if ttl > 1440:
            raise ValueError("ttl must be less than 1 day 1440 minutes")

        action = payload_type.__name__

        try:
            decoded = self._url_serializer.loads(
                token, max_age=ttl * 60, salt=self._action_salt(action)
            )
            token_payload = UrlPayload[payload_type].model_validate(decoded)
        except SignatureExpired:
            raise ExcTokenExpired()
        except Exception:
            raise ExcInvalidToken()

        if token_payload.action != action:
            raise ExcInvalidToken()

        redis_key = f"{payload_type.__name__}:{token_payload.id}"
        stored_key = await self._redis.getdel(redis_key)

        if stored_key is None:
            raise ExcTokenAlreadyUsed()

        return token_payload
