import json
import math
import functools
import logging

import logging

def log_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Called {func.__qualname__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__qualname__}: {e}")
            raise
    return wrapper

def pretty_print_solution(solution):
        print(json.dumps(solution, indent=4))

