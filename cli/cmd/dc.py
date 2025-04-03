from argparse import ArgumentParser, Namespace

from abstract import Command
from runner import run

@run(from_env='compose')
def dc(*args):
    """docker compose"""
    return f'{" ".join(args)}'

class DcAttach(Command):
    """docker compose exec {svc} bash"""

    @run(from_env='compose')
    def __call__(self, args: Namespace):
        return f'exec {args.svc} bash'

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument('svc', help='Сервис к которому выполняется подключение')

dc_attach = DcAttach()