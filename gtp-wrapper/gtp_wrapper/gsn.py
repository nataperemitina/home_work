import scapy.all
from scapy.contrib.gtp import *
from .socketut import UDPSocket

class GSN(object):
    GTP_C_PORT = 2123
    GTP_U_PORT = 2152

    def __init__(self, gtpcip, gtpuip):
        self.gtpc_socket = UDPSocket()
        self.gtpc_socket.bind(gtpcip, GSN.GTP_C_PORT)
        self.gtpu_socket = UDPSocket()
        self.gtpu_socket.bind(gtpuip, GSN.GTP_U_PORT)
        self.gtpc_seq = 1
        self.gtpu_seq = 1

    def get_gtpc_seq(self):
        self.gtpc_seq += 1
        return self.gtpc_seq

    def get_gtpu_seq(self):
        self.gtpu_seq += 1
        return self.gtpu_seq

    def send_gtpu_msg(self, data, ip, port):
        self.gtpu_socket.send(data, ip, port)

    def send_gtpc_msg(self, data, ip, port):
        self.gtpc_socket.send(data, ip, port)

    def recv_gtpc_msg(self, data, ip, port):
        return self.gtpc_socket.recv()

class GGSN(GSN):
    GTP_C_IP = "200.0.0.2"
    GTP_U_IP = "200.0.0.2"
    teid_c = 1
    teid_d = 1

    def __init__(self):
        super(GGSN, self).__init__(GGSN.GTP_C_IP, GGSN.GTP_U_IP)

        GGSN.teid_d = GGSN.teid_d + 1
        GGSN.teid_c = GGSN.teid_c + 1
        self.teid_c = GGSN.teid_c
        self.teid_d = GGSN.teid_d
        self.sgsn_teid_c = 1
        self.sgsn_teid_d = 1

    def receive_create_pdp_request(self):
        pkt  = self.recv_gtpc_msg()
        hexdump(pkt)

    def send_create_pdp_response(self, pdp_context):
        gtp = GTPHeader()/GTPCreatePDPContextResponse()

        gtp.S = 1
        gtp.gtp_type = "create_pdp_context_res"
        gtp.seq = self.get_gtpc_seq()

        gtp.IE_list.append(IE_Cause(CauseValue = "Request accepted"))
        gtp.IE_list.append(IE_ReorderingRequired(reordering_required = "False"))
        gtp.IE_list.append(IE_Recovery(restart_counter = 4))
        gtp.IE_list.append(IE_TEIDI(TEIDI = self.teid_c))
        gtp.IE_list.append(IE_TEICP(TEICI = self.teid_d))
        gtp.IE_list.append(IE_ChargingId())

        ip_address = pdp_context.get('ip')
        if ip_address:
            gtp.IE_list.append(IE_EndUserAddress(length = 6, PDPTypeNumber = 0x21, PDPAddress = ip_address))

        gtp.IE_list.append(IE_GSNAddress(address = GGSN.GTP_C_IP))
        gtp.IE_list.append(IE_GSNAddress(address = GGSN.GTP_U_IP))
        gtp.IE_list.append(IE_NotImplementedTLV(ietype=135, length=15, data=RandString(15)))

        gtp.show2()
        hexdump(gtp)

        super().send_gtpc_msg(raw(gtp), SGSN.GTP_C_IP, SGSN.GTP_C_PORT)

    def send_gtpu(self, payload):
        gtp = GTP_U_Header()/Raw()
        gtp.gtp_type = "g_pdu"
        gtp.seq = self.get_gtpu_seq()
        gtp.teid = self.sgsn_teid_d

        gtp.load = payload

        gtp.show2()
        hexdump(gtp)

        super().send_gtpu_msg(raw(gtp), SGSN.GTP_U_IP, GGSN.GTP_U_PORT)


class SGSN(GSN):
    GTP_C_IP = "200.0.0.1"
    GTP_U_IP = "200.0.0.1"
    teid_c = 1
    teid_d = 1

    def __init__(self):
        super(SGSN, self).__init__(SGSN.GTP_C_IP, SGSN.GTP_U_IP)

        SGSN.teid_d = SGSN.teid_d + 1
        SGSN.teid_c = SGSN.teid_c + 1
        self.teid_c = SGSN.teid_c
        self.teid_d = SGSN.teid_d

        self.ggsn_teid_c = 1
        self.ggsn_teid_d = 1

    def send_create_pdp_request(self, pdp_context):
        gtp = GTPHeader() / GTPCreatePDPContextRequest()

        gtp.S = 1
        gtp.gtp_type = "create_pdp_context_req"
        gtp.seq = self.get_gtpc_seq()

        gtp.IE_list.clear()
        imsi = pdp_context.get('imsi')
        if imsi:
            gtp.IE_list.append(IE_IMSI(imsi = int(imsi)))

        gtp.IE_list.append(IE_TEIDI(TEIDI = self.teid_d))
        gtp.IE_list.append(IE_TEICP(TEICI = self.teid_c))
        gtp.IE_list.append(IE_NSAPI())
        gtp.IE_list.append(IE_GSNAddress(address = SGSN.GTP_C_IP))
        gtp.IE_list.append(IE_GSNAddress(address = SGSN.GTP_U_IP))

        msisdn = pdp_context.get('msisdn')
        if msisdn:
            gtp.IE_list.append(IE_MSInternationalNumber(digits = int(msisdn), length = 7))

        gtp.IE_list.append(IE_NotImplementedTLV(ietype=135, length=15, data=RandString(15)))

        imeisv = pdp_context.get('imeisv')
        if imeisv:
            gtp.IE_list.append(IE_IMEI(IMEI = int(imei), length = 8))

        gtp.show2()
        hexdump(gtp)

        super().send_gtpc_msg(raw(gtp), GGSN.GTP_C_IP, GGSN.GTP_C_PORT)

    def send_gtpu(self, payload):
        gtp = GTP_U_Header()/Raw()
        gtp.gtp_type = "g_pdu"
        gtp.seq = self.get_gtpu_seq()
        gtp.teid = self.ggsn_teid_d

        gtp.load = payload

        gtp.show2()
        hexdump(gtp)

        super().send_gtpu_msg(raw(gtp), GGSN.GTP_U_IP, GGSN.GTP_U_PORT)




