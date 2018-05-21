"""Функциональный подход"""


read_types = {}
write_types = {}


def read(type):
    def decorator(func):
        read_types[type] = func
        return func
    return decorator

def write(type):
    def decorator(func):
        write_types[type] = func
        return func
    return decorator

@read('db')
def read_db(path, params):
    params = {}
    return params

@write('db')
def write_db(path, params):
    pass

@read('xml')
def read_xml(path, params):
    params = {}
    return params

@write('xml')
def write_xml(path, params):
    pass

params = {
    'key1' : 'val1',
    'key2' : 'val2',
}

path = './source.xml'
read_type = read_types.get('xml')
if read_type:
    read_type(path, params)


""" ООП-подход """

class ConfigData(object):
    """
    Класс с конфигурационными параметрами, который будет реализовывать определенный механизм их получения и записи
    """
    def __init__(self):
        self.__params = {} #Словарь конфигурационных параметров
        self.load() # Читаем параметры в конструкторе

    def load(self):
        """Здесь получение параметров из файла xml, либо из бд, либо любым другим способом"""
        pass

    def dump(self):
        """Здесь запись всех параметров в необходимое хранилище """
        pass

    def add_param(self, key, value):
        self.__params[key] = value

    def get_param(self, key):
        return self.__params.get(key)

    def remove_param(self, key):
        if key in self.__params:
            del self.__params[key]



class ConfigInterface(object):
    """Класс типа singleton для обращения из любого места программы для получения конфигурационных параметров"""
    __slots__ = ('__config_data') # содержит в себе объект конфигурационных данных
    __instance = None

    def __init__(self):
        self.__config_data = ConfigData

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def add_param(self, key, value):
        self.__config_data.add_param(key, value)

    def get_param(self, key):
        return self.__config_data.get_param(key)

    def remove_param(self, key):
        self.__config_data.remove_param(key)
