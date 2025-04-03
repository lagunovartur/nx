import subprocess
from functools import wraps
from typing import Literal, Callable, Iterable

from config import config


def _env_src(
    from_env: str | None = None,
    execute = False
) -> Iterable[tuple[str,str]]:

    svc_src = config.svc_src

    dc = f'docker compose -f {config.compose_file}'
    dc_do = f"{dc} {'exec' if execute else 'run --rm -T'}"
    svc_env = {svc: f'{dc_do} {svc}' for svc in svc_src.keys()}

    match from_env:
        case 'compose':
            yield dc, ''
        case 'svc':
            for env in svc_env.values():
                yield env, ''
        case 'src':
            for svc, env in svc_env.items():
                src = ' '.join(svc_src[svc])
                yield env, src
        case _:
            env = svc_env.get(from_env, '')
            yield env , ''


def run(
    *,
    from_env: Literal['compose', 'svc', 'src', 'db', 'api'] | None = None,
    execute = False,
    check: bool = False,
    capture_output: bool = False,
):


    def decorator(func: Callable[[Iterable[str]], str]):

        @wraps(func)
        def wrapper(*args, **kwargs):

            bcmd = func(*args, **kwargs)

            result = []

            for env, src in _env_src(from_env, execute):

                cmd = ' '.join([env, bcmd, src]).strip()
                print(cmd, '\n')

                try:

                    output = subprocess.run(
                        cmd,
                        check=check,
                        shell=True,
                        cwd='.',
                        capture_output=capture_output,
                        text=True
                    )

                    if capture_output:
                        print(output.stdout)
                        result.append(output)

                except subprocess.CalledProcessError as e:
                    print(e.stderr)
                    raise e

            return result

        return wrapper

    return decorator

__all__ = [
    "run"
]
