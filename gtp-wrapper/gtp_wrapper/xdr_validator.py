import json

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


if __name__ == '__main__':
    FIELD_NAMES_IPDR = [
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
    'Metadata']


    IPDR_SEPARATOR = ';'
    ipdr = RecordContainer('../detailed_ipdr.log', FIELD_NAMES_IPDR, IPDR_SEPARATOR, 'Metadata')
    print(ipdr)
    print(ipdr.validate({'http.uri': '/10m',}, {'UplinkBytes':217327, 'DownlinkBytes':10667183}))
    print(ipdr.validate({'http.uri': '/10m',}, {'UplinkBytes':217328, 'DownlinkBytes':10667183}))
    print(ipdr.sum_field_values('UplinkBytes', {'http.uri': '/1k',}))
    print(ipdr.sum_field_values('DownlinkBytes', {'http.uri': '/1k',}))
    print(ipdr.validate({'http.uri': '/1k'},{'UplinkBytes':6510}))
    print(ipdr.validate({'SubscriberID': '1.1.1.3',}))
    print(ipdr.validate({'SubscriberPort': '50166',}))