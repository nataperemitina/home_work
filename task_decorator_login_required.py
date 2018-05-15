import hashlib
from functools import wraps


def make_token(username, password):
    s = username + password
    return hashlib.md5(s.encode()).hexdigest()


allow = False


def check_login():
    global allow
    if allow:
        return True

    with open('token.txt') as f:
        token = f.readline().strip()
    for i in range(0, 3):
        allow = make_token(input(), input()) == token
        if allow:
            return True
    return False


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if check_login():
            return func(*args, **kwargs)
    return wrapper
