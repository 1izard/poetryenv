from functools import wraps
from typing import Callable

from poetryenv.exceptions import RunnerError


def runner(cmd: str, is_available: bool = False):
    def wrapper(func: Callable):
        @wraps(func)
        def validate(*args, **kwargs):
            if is_available:
                return func(*args, **kwargs)
            else:
                raise RunnerError(f'{cmd} is not available. Please install {cmd}.')
        return validate
    return wrapper
