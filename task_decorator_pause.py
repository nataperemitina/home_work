import time

def pause(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(n)
            return func(*args, **kwargs)
        return wrapper
    return decorator


