import pickle
import json
import os.path as Path
from abc import ABCMeta, abstractmethod

class ParamHandler(metaclass=ABCMeta):
    types = {}
    def __init__(self, source):
        self.source = source
        self.params = {}

    def add_param(self, key, value):
         self.params[key] = value

    def get_all_params(self):
        return self.params

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise ParamHandlerException('Type must have a name!')

        if not issubclass(klass, ParamHandler):
            raise ParamHandlerException('Class "{}" is not ParamHandler!'.format(klass))

        cls.types[name] = klass

    @classmethod
    def get_instance(cls, source, *args, **kwargs):
        _, ext = Path.splitext(str(source).lower())
        ext = ext.lstrip('.')
        klass = cls.types.get(ext)
        if klass is None:
            raise ParamHandlerException('Type "{}" not found!'.format(ext))

        return klass(source, *args, **kwargs)


class ParamHandlerException(Exception):
    """Base class for exceptions in this module."""
    pass


def type_hold(name):
    def decorator(cls):
        ParamHandler.add_type(name, cls)
        return cls
    return decorator


@type_hold('json')
class JsonParamHandler(ParamHandler):
    def read(self):
        with open(self.source) as f:
            self.params = json.load(f)

    def write(self):
        with open(self.source, 'w') as f:
            json.dump(self.params, f, indent=4)


@type_hold('pickle')
class PickleParamHandler(ParamHandler):
    def read(self):
        with open(self.source, 'rb') as f:
            self.patams = pickle.load(f)

    def write(self):
        with open(self.source, 'wb') as f:
            pickle.dump(self.params, f)



config = ParamHandler.get_instance('./params.pickle')
config.add_param('key1', 'val1')
config.add_param('key2', 'val2')
config.add_param('key3', 'val3')
config.write() # запись файла в pickle формате

config = ParamHandler.get_instance('./params.json')
config.read() # читаем данные из текстового файла