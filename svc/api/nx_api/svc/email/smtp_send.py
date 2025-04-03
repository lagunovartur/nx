from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from jinja2 import Environment
from attrs import define
from asyncio import gather, create_task

from nx_api.infra.smtp.config import SmtpConfig
from nx_api.svc.email.abstract import ISendMail, Email


@define
class SmtpSend(ISendMail):

    _smtp: SMTP
    _templates: Environment
    _config: SmtpConfig

    async def __call__(
        self,
        subject: str,
        template: str,
        data: dict,
        recipients: list[Email]
    ) -> dict[Email, Exception]:

        body = self._templates.get_template(template).render(data)
        tasks = [
            create_task(
                self._smtp.send_message(
                    self._msg(subject, body, recipient)
                )
            ) for recipient in recipients
        ]
        send_result = zip(await gather(*tasks, return_exceptions=True), recipients)

        send_errors = {recipient: task_result for task_result, recipient in send_result if isinstance(task_result, Exception)}

        return send_errors

    def _msg(self, subject: str, content: str, recipient: Email) -> MIMEMultipart:

        msg = MIMEMultipart()
        msg['From'] = self._config.EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'html', _charset="utf-8"))

        return msg

