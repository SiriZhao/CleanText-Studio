import random
import time
from collections.abc import Callable

from .exceptions import (
    NetworkError,
    ProviderServerError,
    RateLimitError,
    RequestTimeoutError,
    UserCancelledError,
)

RETRYABLE = (NetworkError, ProviderServerError, RateLimitError, RequestTimeoutError)


def with_retry[T](operation: Callable[[], T], cancelled: Callable[[], bool], retries: int = 2) -> T:
    for attempt in range(retries + 1):
        if cancelled():
            raise UserCancelledError("Operation cancelled")
        try:
            return operation()
        except RETRYABLE:
            if attempt >= retries:
                raise
            time.sleep((2**attempt) * 0.25 + random.uniform(0, 0.1))
    raise AssertionError("unreachable")
