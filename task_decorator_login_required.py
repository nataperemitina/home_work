import hashlib
from functools import wraps


def make_token(username, password):
    s = username + password
    return hashlib.md5(s.encode()).hexdigest()


def cache(func):
    allow = False
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal allow
        if allow:
            return True

        allow = func(*args, **kwargs)
        return allow
    return wrapper

@cache
def check_login():
    with open('token.txt') as f:
        token = f.readline().strip()
    for i in range(0, 3):
        if make_token(input(), input()) == token:
            return True

    return False


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if check_login():
            return func(*args, **kwargs)
    return wrapper


