from abc import ABC, abstractmethod

from typing_extensions import TypeAlias

Email: TypeAlias = str

class ISendMail(ABC):

    @abstractmethod
    async def __call__(
        self,
        subject: str,
        template: str,
        data: dict,
        recipients: list[Email],
    ) -> dict[Email, Exception]:
        pass