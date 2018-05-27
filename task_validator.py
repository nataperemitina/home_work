from abc import ABCMeta, abstractmethod
from datetime import datetime
import string

class Validator(metaclass=ABCMeta):
    validators = {}

    @abstractmethod
    def validate(self, value):
        pass

    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise ValidatorException('Validator must have a name!')

        if not issubclass(klass, Validator):
            raise ValidatorException('Class "{}" is not Validator!'.format(klass))

        cls.validators[name] = klass

    @classmethod
    def get_instance(cls, name, *args, **kwargs):
        klass = cls.validators.get(name)
        if klass is None:
            raise ValidatorException('Validator with name "{}" not found!'.format(name))

        return klass(*args, **kwargs)


class ValidatorException(Exception):
    pass


def type_hold(name):
    def decorator(cls):
        Validator.add_type(name, cls)
        return cls
    return decorator


@type_hold('email')
class EMailValidator(Validator):
    valid_range = string.ascii_letters + string.digits + "._-'+"

    def get_valid_range(self):
        return self.valid_range

    def validate(self, value):
        user_host = value.strip().split('@')
        if len(user_host) != 2:
            return False

        for char in user_host[0]:
            if char not in self.get_valid_range():
                return False

        return True


@type_hold('datetime')
class DateTimeValidator(Validator):
    delimiters = ['-', '.', '/']

    def get_delimiters(self):
        return self.delimiters

    def validate(self, value):
        date_and_time = value.strip().split(' ')

        if len(date_and_time) > 2:
            return False

        date = []
        for delim in self.get_delimiters():
            date = [int(item)  for item in date_and_time[0].split(delim) if item.isdigit()]
            if len(date) == 3:
                if delim == '-':
                    date.reverse()
                break

        if len(date) != 3:
            return False

        time = [0, 0, 0]
        if len(date_and_time) > 1:
            time = [int(item) for item in date_and_time[1].split(':') if item.isdigit()]
            if len(time) == 2:
                time.append(0)
            elif len(time) > 3:
                return False

        try:
            date_time = datetime(date[2], date[1], date[0], time[0], time[1], time[2])
        except:
            return False

        return True

