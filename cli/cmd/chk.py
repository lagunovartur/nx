from runner import run


def chk_style():
    """ruff check | ruff format --check """

    @run(from_env='src', check=True)
    def chk_ruff():
        return 'ruff check'

    @run(from_env='src', check=True)
    def chk_ruff_format():
        return 'ruff format --check'

    chk_ruff()
    chk_ruff_format()


@run(from_env='src', check=True)
def chk_mypy():
    """mypy"""
    return 'mypy --explicit-package-bases --enable-error-code ignore-without-code'


def chk():
    """chk-test | chk-style | chk-mypy"""
    chk_test()
    chk_style()
    chk_mypy()


def chk_test():
    """tests"""

    @run(from_env='docker', check=True)
    def be_test():
        return f'run --rm -T api pytest -n 2'

    be_test()
