from abc import ABCMeta, abstractmethod

class Command(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class Menu(metaclass=ABCMeta):
    def __init__(self):
        self.__commands = {}
        self.__index = 0

    def add_command(self, name, klass):
        if not name:
            raise CommandException('Command must have a name!')

        if not issubclass(klass, Command):
            raise CommandException('Class "{}" is not Command!'.format(klass))

        self.__commands[name] = klass

    def execute(self, name, *args, **kwargs):
        command = self.__commands.get(name)
        if command:
            command.execute(args, kwargs)
        else:
            raise CommandException('Command with name "{}" not found'.format(name))

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index < len(self.__commands):
            command = (list(self.__commands.items()))[self.__index]
            self.__index += 1
            return command
        else:
            self.__index = 0
            raise StopIteration



class CommandException(Exception):
    pass


