from collections import namedtuple


def return_namedtuple(*names):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, tuple):
                new_result = namedtuple("NamedTuple", names)
                return new_result(*result)
            return result
        return wrapper
    return decorator

