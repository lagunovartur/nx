import asyncio
import nx_api.repo as r
from attrs import define

from nx_api.core.config import ApiConfig
from nx_api.dto.auth import EmailReq
from nx_api.svc.email.abstract import ISendMail
from nx_api.svc.url_token.abstract import IUrlTokenSvc


@define
class VerifyEmailIA:
    _token_svc: IUrlTokenSvc
    _user_repo: r.User
    _config: ApiConfig
    _sender: ISendMail

    async def __call__(self, email: str) -> None:
        user = await self._user_repo.one_or_none(email=email)
        if not user:
            return

        token = await self._token_svc.encode(EmailReq(email=user.email))

        confirm_url = self._config.API_URL / "auth" / "verify" / "email" / token

        loop = asyncio.get_running_loop()
        loop.create_task(
            self._sender(
                subject="Подтверждение email",
                template="msg_email_confirm.html",
                data={"confirm_url": str(confirm_url)},
                recipients=[user.email],
            )
        )
