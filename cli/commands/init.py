import os
from argparse import ArgumentParser, Namespace
from pathlib import Path

from abs import Command
from config import config
from runner import run


class InLink(Command):
    """ln -s ./run /usr/local/bin/fr"""

    @run()
    def __call__(self, args: Namespace):

        src = config.cli_file
        dst = Path('/usr/local/bin').joinpath(args.name)

        if not os.path.isdir('/usr/local/bin'):
            raise FileNotFoundError("Директория /usr/local/bin не существует.")

        if dst.exists() and dst.is_symlink():
            dst.unlink()

        return f'ln -s {src} {dst}'

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument('name', nargs='?', default='mg', help='alo')

class Init(Command):

    def __call__(self, args: Namespace):
        in_link(args)
        in_hook()

    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument('name', nargs='?', default='fr', help='alo')


in_link = InLink()
init = Init()



@run()
def in_hook():
    """unset git hooks"""

    src = config.git_root_dir.joinpath('cli/git_hooks')
    dst = config.git_root_dir.joinpath('.git/hooks')

    return f'cp {src}/* {dst}'


def in_unhook():
    """set git hooks"""

    src = config.git_root_dir.joinpath('cli/git_hooks')
    dst = config.git_root_dir.joinpath('.git/hooks')

    for src_file in src.iterdir():
        if not src_file.is_file():
            continue
        dst_file = dst.joinpath(src_file.name)
        print(dst_file)
        os.unlink(dst_file)


__all__ = [
    'init',
    'in_link',
    'in_hook',
    'in_unhook',
]
