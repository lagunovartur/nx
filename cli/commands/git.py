from runner import run

@run()
def git(*args):
    """git"""
    return f'git {" ".join(args)}'