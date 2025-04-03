from abc import abstractmethod, ABC
from argparse import ArgumentParser, Namespace


class Command(ABC):

    @abstractmethod
    def __call__(self, args: Namespace):
        raise NotImplementedError


    @abstractmethod
    def add_args(self, parser: ArgumentParser) -> None:
        raise NotImplementedError

