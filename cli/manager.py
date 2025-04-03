import argparse
from collections.abc import Callable

from abstract import Command



class CommandManager:

    def __init__(self):
        self._commands: dict[str, Callable] = {}

    def __setitem__(self, key: str, value: Callable | Command) -> None:
        self._commands[key] = value

    def __call__(self):
        inp = self._cli_input()
        cmd = self._commands[inp.command]
        if hasattr(inp, 'args'):
            cmd(*inp.args)
        else:
            cmd(inp)

    def _cli_input(self):
        return self._arg_parser().parse_args()

    def _arg_parser(self) -> argparse.ArgumentParser:

        parser = argparse.ArgumentParser(description="Project cli")
        sparsers = parser.add_subparsers(dest="command", help="command")

        for cmd, handler in self._commands.items():
            sparser = sparsers.add_parser(cmd, help=handler.__doc__)

            if isinstance(handler, Command):
                handler.add_args(sparser)
            else:
                sparser.add_argument('args', nargs=argparse.REMAINDER, help="Arguments for the command")

        return parser





