from random import choice
from string import printable


def password_generator(l):
    while 1:
        yield ''.join(choice(printable) for i in range(l))
