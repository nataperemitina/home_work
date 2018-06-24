import scapy.all
from scapy.contrib.gtp import *
from socketut import UDPSocket

class GSN(object):
    GTP_C_PORT = 2123
    GTP_U_PORT = 2152

    def __init__(self, gtpcip, gtpcport, gtpuip, gtpuport):
        self.gtpc_socket = UDPSocket()
        self.gtpc_socket.bind(gtpcip, gtpcport)
        self.gtpu_socket = UDPSocket()
        self.gtpu_socket.bind(gtpuip, gtpuport)
        self.gtpc_seq = 1
        self.gtpu_seq = 1

    def getGTPCSeq(self):
        self.gtpc_seq = self.gtpc_seq + 1
        return self.gtpc_seq

    def getGTPUSeq(self):
        self.gtpu_seq = self.gtpu_seq + 1
        return self.gtpu_seq

    def sendGTPUMsg(self, data, ip, port):
        self.gtpu_socket.send(data, ip, port)

    def sendGTPCMsg(self, data, ip, port):
        self.gtpc_socket.send(data, ip, port)

    def recvGTPCMsg(self, data, ip, port):
        return self.gtpc_socket.recv()

class GGSN(GSN):
    GTP_C_IP = "200.0.0.2"
    GTP_U_IP = "200.0.0.2"
    teid_c = 1
    teid_d = 1

    def __init__(self):
        super(GGSN, self).__init__(GGSN.GTP_C_IP, GGSN.GTP_C_PORT, GGSN.GTP_U_IP, GGSN.GTP_U_PORT)

        GGSN.teid_d = GGSN.teid_d + 1
        GGSN.teid_c = GGSN.teid_c + 1
        self.teid_c = GGSN.teid_c
        self.teid_d = GGSN.teid_d
        self.sgsn_teid_c = 1
        self.sgsn_teid_d = 1

    def receiveCreatePDPContextRequest(self):
        pkt  = self.recvGTPCMsg()
        hexdump(pkt)

    def sendCreatePDPContextResponse(self,
                                     endUserIP,
                                     GSNAddressForSignaling,
                                     GSNAddressForUserTraffic,
                                     ):
        gtp = GTPHeader()/GTPCreatePDPContextResponse()
        # Fill in GTP Header
        gtp.S = 1
        gtp.gtp_type = "create_pdp_context_res"
        gtp.seq = self.getGTPCSeq()

        gtp.IE_list.append(IE_Cause(CauseValue = "Request accepted"))
        gtp.IE_list.append(IE_ReorderingRequired(reordering_required = "False"))
        gtp.IE_list.append(IE_Recovery(restart_counter = 4))
        gtp.IE_list.append(IE_TEIDI(TEIDI = self.teid_c))
        gtp.IE_list.append(IE_TEICP(TEICI = self.teid_d))
        gtp.IE_list.append(IE_ChargingId())
        gtp.IE_list.append(IE_EndUserAddress(length = 6, PDPTypeNumber = 0x21, PDPAddress = endUserIP))
        gtp.IE_list.append(IE_GSNAddress(address = GSNAddressForSignaling))
        gtp.IE_list.append(IE_GSNAddress(address = GSNAddressForUserTraffic))
        gtp.IE_list.append(IE_NotImplementedTLV(ietype=135, length=15, data=RandString(15)))

        gtp.show2()
        hexdump(gtp)

        super().sendGTPCMsg(raw(gtp), SGSN.GTP_C_IP, SGSN.GTP_C_PORT)

    def sendGTPU(self, payload):
        gtp = GTP_U_Header()/Raw()
        gtp.gtp_type = "g_pdu"
        gtp.seq = self.getGTPUSeq()
        gtp.teid = self.sgsn_teid_d

        gtp.load = payload

        gtp.show2()
        hexdump(gtp)

        super().sendGTPUMsg(raw(gtp), SGSN.GTP_U_IP, GGSN.GTP_U_PORT)


class SGSN(GSN):
    GTP_C_IP = "200.0.0.1"
    GTP_U_IP = "200.0.0.1"
    teid_c = 1
    teid_d = 1

    def __init__(self):
        super(SGSN, self).__init__(SGSN.GTP_C_IP, SGSN.GTP_C_PORT, SGSN.GTP_U_IP, SGSN.GTP_U_PORT)

        SGSN.teid_d = SGSN.teid_d + 1
        SGSN.teid_c = SGSN.teid_c + 1
        self.teid_c = SGSN.teid_c
        self.teid_d = SGSN.teid_d

        self.ggsn_teid_c = 1
        self.ggsn_teid_d = 1

    #, imsi, msisdn, imei
    def sendCreatePDPContextRequest(self, imsi,
                                    GSNAddressForSignaling,
                                    GSNAddressForUserTraffic,
                                    msisdn, imei):
        gtp = GTPHeader() / GTPCreatePDPContextRequest()
        # Fill in GTP Header
        gtp.S = 1
        gtp.gtp_type = "create_pdp_context_req"
        gtp.seq = self.getGTPCSeq()

        gtp.IE_list.clear()
        gtp.IE_list.append(IE_IMSI(imsi = imsi))
        gtp.IE_list.append(IE_TEIDI(TEIDI = self.teid_d))
        gtp.IE_list.append(IE_TEICP(TEICI = self.teid_c))
        gtp.IE_list.append(IE_NSAPI())
        gtp.IE_list.append(IE_GSNAddress(address = GSNAddressForSignaling))
        gtp.IE_list.append(IE_GSNAddress(address = GSNAddressForUserTraffic))
        gtp.IE_list.append(IE_MSInternationalNumber(digits = msisdn, length = 7))
        gtp.IE_list.append(IE_NotImplementedTLV(ietype=135, length=15, data=RandString(15)))
        gtp.IE_list.append(IE_IMEI(IMEI = imei, length = 8))

        gtp.show2()
        hexdump(gtp)

        super().sendGTPCMsg(raw(gtp), GGSN.GTP_C_IP, GGSN.GTP_C_PORT)

    def sendGTPU(self, payload):
        gtp = GTP_U_Header()/Raw()
        gtp.gtp_type = "g_pdu"
        gtp.seq = self.getGTPUSeq()
        gtp.teid = self.ggsn_teid_d

        gtp.load = payload

        gtp.show2()
        hexdump(gtp)

        super().sendGTPUMsg(raw(gtp), GGSN.GTP_U_IP, GGSN.GTP_U_PORT)

#   def receiveAndCheck(self, imsi, msisdn, imei)
class Test(object):
    def __init__(self):
        self.sgsn = SGSN()
        self.ggsn = GGSN()

    def main(self):
        self.emulatePDPContextCreation()
        self.emulateTraffic()

    def emulatePDPContextCreation(self):
        # Emulate Control plain
        self.sgsn.sendCreatePDPContextRequest(
            208101166102614,  # IMSI
            "192.168.1.1",  # GSNAddressForSignaling
            "192.168.1.2",  # GSNAddressForUserTraffic
            33610328579,  # MSISDN
            3517510449245601)  # IMEI

        self.ggsn.sendCreatePDPContextResponse(
            "10.132.1.1",  # EndUserIP
            "10.10.10.1",  # GSNAddressForSignaling
            "10.10.10.1",  # GSNAddressForUserTraffic
        )

    def emulateTraffic(self):
        # Emulate traffic
        dump = rdpcap("imo.cap")
        for packet in dump:
            # TODO Need to check if IP leayer is avaliable
            if packet[IP].src == "192.168.169.22":
                self.sgsn.sendGTPU(raw(packet[IP]))
            elif packet[IP].src == "192.168.169.1":
                self.ggsn.sendGTPU(raw(packet[IP]))


def main():
    test = Test()
    test.main()

if __name__ == "__main__":
    main()




#bind_layers(GTPHeader, GTPCreatePDPContextRequest1, gtp_type=16)



