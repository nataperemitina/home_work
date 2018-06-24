import sys
import argparse
from scapy.all import *

class GTP_Wrapper(object):
    pass

def main():
    parser = argparse.ArgumentParser(description='Тест на упаковку трафика в gtp-тунель')
    pdp_context = parser.add_argument_group('pdp_context', 'Параметры pdp-контекста абонента')
    pdp_context.add_argument('--imsi', help='IMSI абонента')
    pdp_context.add_argument('--msisdn', help='MSISDN абонента')
    pdp_context.add_argument('--imeisv', help='IMEI_SV абонента')

    parser.add_argument('--up', help='Интерфейс для передачи пакетов трафика uplink')
    parser.add_argument('--dn', help='Интерфейс для передачи пакетов трафика downlink')

    parser.add_argument('-f','--dump_file', help='Полный путь к файлу с дампом трафика, который необходимо упаковать в gtp-туннель')
    parser.add_argument('--ip', help='IP-адрес абонента для определения направления передачи пакета')

    parser.add_argument('--xdr',help='Полный путь к файлу с записями для валидации')

    arguments = vars(parser.parse_args())
    print(arguments)

    if 'dump_file' in arguments:
        dump = rdpcap(arguments['dump_file'])
        for packet in dump:
            if packet[IP] == 
        print(dump)