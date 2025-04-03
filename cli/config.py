import subprocess
import tomllib
from functools import cached_property
from pathlib import Path


class Config:

    def __init__(self):

        with open(self.config_file, 'rb') as file:
            self._config = tomllib.load(file)

    @cached_property
    def git_root_dir(self) -> Path:
        try:
            return Path(subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                check=True,
                capture_output=True,
                text=True,
                cwd=Path(__file__).resolve().parent,
            ).stdout.strip())
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Не удалось определить корень репозитория Git") from e

    @cached_property
    def config_file(self) -> Path:
        return self.git_root_dir.joinpath('cli/config.toml')

    @cached_property
    def cli_file(self) -> Path:
        return self.git_root_dir.joinpath('cli/run')

    @cached_property
    def compose_file(self) -> Path:
        return self.git_root_dir.joinpath(self._config['path']['compose'])

    @property
    def svc_src(self) -> dict[str, list[str]]:
        return self._config['svc_src']

    @property
    def db_dump_dir(self) -> Path:
        return Path(self._config['path']['db_dump'])

    @property
    def cli_cmd(self) -> str:
        return self._config['cmd']['cli']


config = Config()
