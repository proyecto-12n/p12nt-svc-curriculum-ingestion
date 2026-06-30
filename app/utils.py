# -*- coding: utf-8 -*-
"""
NextProject © 2026
"""

import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def log_execution_time(func):
    """
    Decorator to log execution time of a function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"Function {func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper
