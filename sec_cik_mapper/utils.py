from functools import lru_cache
from typing import Callable

from .types import T


def with_cache(func: Callable[..., T]) -> T:
    return lru_cache()(func)  # type: ignore
