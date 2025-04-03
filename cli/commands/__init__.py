from collections.abc import Callable

commands: dict['str', Callable[[],None]] = {
    '': lambda : None,
}



