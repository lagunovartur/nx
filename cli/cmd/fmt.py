from runner import run


@run(from_env='src')
def fmt():
    """ruff format"""
    return 'ruff format'
