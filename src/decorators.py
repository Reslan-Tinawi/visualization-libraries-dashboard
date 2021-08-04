import functools
import time
from typing import Callable


def timer(func: Callable):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        result = func(*args, **kwargs)
        toc = time.perf_counter()
        execution_time = toc - tic
        print(f"function {func.__name__!r} finished in: {execution_time:.4f} seconds")
        return result

    return wrapper_timer
