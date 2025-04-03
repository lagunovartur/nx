from runner import run


@run(from_env='src')
def fmt():
    """fmt_ruff"""
    return 'ruff format'
