import json
from abc import ABCMeta, abstractmethod

class Record(object):
    __slots__ = ('__fields')

    def __init__(self, raw, names, separator, json_field=None):
        values = raw.split(separator)

        if len(values) != len(names):
            return

        self.__fields = dict(zip(names,values))
        if json_field in self.__fields:
            meta = self.__fields.pop(json_field)
            self.__fields.update(json.loads(meta))

    def __str__(self):
        return str(self.__fields)

    def contains(self, fields):
        if fields:
            return fields.items() <= self.__fields.items()

        return True

    def get_field_value(self, name):
        return self.__fields.get(name)


class RecordContainer(object):
    __slots__ = ('__records')

    def __init__(self, file_path, names, separator, json_field=None, keys=None):
        self.__records = []
        with open(file_path) as f:
            for line in f:
                record = Record(line, names, separator, json_field)
                if record.contains(keys):
                    self.__records.append(record)

    def __repr__(self):
        return '\n'.join([str(record) for record in self.__records])

    def sum_field_values(self, field_name, fields=None):
        result = 0
        for record in self.__records:
            if record.contains(fields):
                value = record.get_field_value(field_name)
                if value:
                    result += int(value)
                else:
                    raise AssertionError("Can't find field: {}".format(field_name))
        return result

    def validate(self, keys, calculated_values=None):
        if calculated_values:
            for key, value in calculated_values.items():
                if self.sum_field_values(key, keys) != value:
                    return False
        else:
            for record in self.__records:
                if not record.contains(keys):
                    return False
        return True


class XDR_Validator(metaclass=ABCMeta):
    validators = {}

    @abstractmethod
    def validate(self, pdp_context, up_bytes, dn_bytes):
        pass

    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise XDR_ValidatorException('Validator must have a name!')

        if not issubclass(klass, XDR_Validator):
            raise XDR_ValidatorException('Class "{}" is not Validator!'.format(klass))

        cls.validators[name] = klass

    @classmethod
    def get_instance(cls, name, *args, **kwargs):
        klass = cls.validators.get(name)
        if klass is None:
            raise XDR_ValidatorException('Validator with name "{}" not found!'.format(name))

        return klass(*args, **kwargs)

class XDR_ValidatorException(Exception):
    pass


def type_hold(name):
    def decorator(cls):
        XDR_Validator.add_type(name, cls)
        return cls
    return decorator


@type_hold('ipdr')
class IPDRValidator(XDR_Validator):
    def __init__(self, file_path):
        self.records = RecordContainer(file_path,
                                       [
                                           'Time',
                                           'SubscriberID',
                                           'SubscriberIPAddress',
                                           'SubscriberPort',
                                           'NetworkIPAddress',
                                           'NetworkPort',
                                           'ProtocolID',
                                           'ServiceID',
                                           'UplinkBytes',
                                           'DownlinkBytes',
                                           'SessionDuration',
                                           'Metadata'],
                                        ';')

    def validate(self, pdp_context, up_bytes, dn_bytes):
        return self.records.validate(pdp_context, {'UplinkBytes':up_bytes, 'DownlinkBytes':dn_bytes})
