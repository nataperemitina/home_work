import sys
import argparse
from scapy.all import *
from .gsn import SGSN, GGSN
from .xdr_validator import XDR_Validator

class GTPWrapperTest(object):
    def __init__(self):
        self.sgsn = SGSN()
        self.ggsn = GGSN()
        self.cached = {}

    def pdp_creation(self, pdp_context):
        """ Emulate Control plain """
        self.sgsn.send_create_pdp_request(pdp_context)
        self.ggsn.send_create_pdp_response(pdp_context)

    def emulate_traffic(self, dump_file, pdp_context):
        """ Emulate traffic sending"""
        up_bytes = 0
        dn_bytes = 0
        dump = rdpcap(dump_file)
        ip_address = pdp_context.get('ip')
        if ip_address:
            for packet in dump:
                if IP in packet:
                    if packet[IP].src == ip_address:
                        self.sgsn.send_gtpu(raw(packet[IP]))
                        up_bytes += len(packet[IP])
                    else:
                        self.ggsn.send_gtpu(raw(packet[IP]))
                        dn_bytes += len(packet[IP])
                elif IPv6 in packet:
                    if packet[IPv6].src == ip_address:
                        self.sgsn.send_gtpu(raw(packet[IPv6]))
                        up_bytes += len(packet[IP])
                    else:
                        self.ggsn.send_gtpu(raw(packet[IPv6]))
                        dn_bytes += len(packet[IPv6])
        else:
            for packet in dump:
                if IP in packet:
                    self.sgsn.send_gtpu(raw(packet[IP]))
                    up_bytes += len(packet[IP])
                elif IPv6 in packet:
                    self.sgsn.send_gtpu(raw(packet[IPv6]))
                    up_bytes += len(packet[IPv6])

        self.cached[dump_file] = (up_bytes,dn_bytes)
        return (up_bytes,dn_bytes)

    def validate(self, dump_file, pdp_context, xdr_file):
        if dump_file in self.cached:
            traffic = self.cached[dump_file]
            return XDR_Validator.get_instance('ipdr', xdr_file).validate(pdp_context, traffic[0], traffic[1])

class TestException(Exception):
    pass

def main():
    parser = argparse.ArgumentParser(description='Тест на упаковку трафика в gtp-туннель')
    pdp_context = parser.add_argument_group('pdp_context', 'Параметры pdp-контекста абонента')
    pdp_context.add_argument('--imsi', help='IMSI абонента')
    pdp_context.add_argument('--msisdn', help='MSISDN абонента')
    pdp_context.add_argument('--imeisv', help='IMEI_SV абонента')
    pdp_context.add_argument('--ip', help='IP-адрес абонента')

    parser.add_argument('-f','--dump_file', help='Полный путь к файлу с дампом трафика, который необходимо упаковать в gtp-туннель')
    parser.add_argument('--xdr',help='Полный путь к файлу с записями для валидации')

    all_arguments = vars(parser.parse_args())
    arguments = {i:all_arguments[i] for i in all_arguments if all_arguments[i] is not None}

    print(arguments)

    test = GTPWrapperTest()
    test.pdp_creation(arguments)

    dump_file = arguments.pop('dump_file')
    if dump_file:
        test.emulate_traffic(dump_file, arguments)

        xdr_file = arguments.pop('xdr')
        if xdr_file:
            if not test.validate(dump_file, arguments, xdr_file):
                raise TestException('GTPWrapperTest failure')

