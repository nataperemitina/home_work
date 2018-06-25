import sys
import argparse
from scapy.all import *
from .gsn import SGSN, GGSN
from .xdr_validator import XDR_Validator

class GTPWrapperTest(object):
    def __init__(self):
        self.sgsn = SGSN()
        self.ggsn = GGSN()

    def pdp_creation(self, pdp_context):
        """ Emulate Control plain """
        self.sgsn.send_create_pdp_request(pdp_context)
        self.ggsn.send_create_pdp_response(pdp_context)

    def emulate_traffic(self, file_path, pdp_context):
        """ Emulate traffic sending"""
        dump = rdpcap(file_path)
        ip_address = pdp_context.get('ip')
        if ip_address:
            for packet in dump:
                if IP in packet:
                    if packet[IP].src == ip_address:
                        self.sgsn.send_gtpu(raw(packet[IP]))
                    else:
                        self.ggsn.send_gtpu(raw(packet[IP]))
                elif IPv6 in packet:
                    if packet[IPv6].src == ip_address:
                        self.sgsn.send_gtpu(raw(packet[IPv6]))
                    else:
                        self.ggsn.send_gtpu(raw(packet[IPv6]))

        else:
            for packet in dump:
                if IP in packet:
                    self.sgsn.send_gtpu(raw(packet[IP]))
                elif IPv6 in packet:
                    self.sgsn.send_gtpu(raw(packet[IPv6]))

    def validate(self, xdr_file, pdp_context):
        return XDR_Validator.get_instance('ipdr', xdr_file).validate(pdp_context, 0, 0)

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

    arguments = vars(parser.parse_args())
    print(arguments)

    test = GTPWrapperTest()
    test.pdp_creation(arguments)

    dump_file = arguments.pop('dump_file')
    if dump_file:
        test.emulate_traffic(dump_file, arguments)

    xdr_file = arguments.pop('xdr')
    if xdr_file:
        if not test.validate(xdr_file, arguments):
            raise TestException('GTPWrapperTest failure')

