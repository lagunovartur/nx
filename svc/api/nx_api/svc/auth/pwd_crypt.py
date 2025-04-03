from attrs import define
from passlib.context import CryptContext
from abc import ABC, abstractmethod


class IPwdCrypt(ABC):
    @abstractmethod
    def hash(self, secret: str) -> str:
        pass

    @abstractmethod
    def verify(self, secret: str, hash: str) -> bool:
        pass


@define
class PwdCrypt(IPwdCrypt):
    _crypt: CryptContext

    def hash(self, secret: str) -> str:
        return self._crypt.hash(secret)

    def verify(self, secret: str, hash: str) -> bool:
        return self._crypt.verify(secret, hash)
