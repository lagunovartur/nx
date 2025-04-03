from abstract import Command
from runner import run
from argparse import ArgumentParser, Namespace


@run(from_env='db', execute=True)
def al(*args):
    """alembic"""
    return f'alembic {" ".join(args)}'

class AlRev(Command):
    """alembic revision --autogenerate"""

    @run(from_env='db', execute=True)
    def __call__(self, args: Namespace):
        return f'alembic revision --autogenerate -m {args.revision}'

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument('revision', type=str, help='имя миграции')

class AlUp(Command):
    """alembic upgrade"""

    @run(from_env='db', execute=True)
    def __call__(self, args: Namespace):
        return f'alembic upgrade {args.revision}'

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument('revision', default='head', nargs='?')

class AlDown(Command):
    """alembic downgrade"""

    @run(from_env='db', execute=True)
    def __call__(self, args: Namespace):
        return f'alembic downgrade {args.revision}'

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument('revision', default=str(-1), nargs='?')


al_rev = AlRev()
al_up = AlUp()
al_down = AlDown()
