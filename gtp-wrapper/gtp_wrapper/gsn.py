import scapy.all
from scapy.contrib.gtp import *
from socketut import UDPSocket

class IMSI_TEST(Packet):
    name = "IMEI"
    fields_desc = [ PacketListField("IE_list", [ IE_IMSI() ,
                                                 IE_NotImplementedTLV(ietype=135, length=15,data=RandString(15)) ],
                                                IE_Dispatcher) ]


class GTPCreatePDPContextRequest2(Packet):
    # 3GPP TS 29.060 V9.1.0 (2009-12)
    name = "GTP Create PDP Context Request"
    fields_desc = [ PacketListField("IE_list", [ IE_IMSI(),
                                                 IE_TEIDI(),
                                                 IE_TEICP(),
                                                 IE_NSAPI(),
                                                 IE_GSNAddress(),
                                                 IE_GSNAddress(),
                                                 IE_MSInternationalNumber(),
                                                 IE_NotImplementedTLV(ietype=135, length=15,data=RandString(15)),
                                                 IE_IMEI() ],
                                                    IE_Dispatcher) ]
    def hashret(self):
        return struct.pack("H", self.seq)

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

    #def receiveCreatePDPContextRequest(self):


    def sendCreatePDPContextResponse(self):


    def sendGTPU(self, payload):
        gtp = GTP_U_Header()/Raw()
        gtp.gtp_type = 255
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
        gtp = GTPHeader() / GTPCreatePDPContextRequest2()
        # Fill in GTP Header
        gtp.S = 1
        gtp.gtp_type = 16
        gtp.seq = self.getGTPCSeq()

        # IMSI
        gtp.IE_list[0].imsi = imsi

        # TEID
        gtp.IE_list[1].TEIDI = self.teid_d
        gtp.IE_list[2].TEICI = self.teid_c

        # GSN Address
        gtp.IE_list[4].address = GSNAddressForSignaling
        gtp.IE_list[5].address = GSNAddressForUserTraffic

        # MSISDN
        gtp.IE_list[6].digits = msisdn
        gtp.IE_list[6].length = 7

        # IMEI
        gtp.IE_list[8].IMEI = imei
        gtp.IE_list[8].length = 8

        gtp.show2()
        hexdump(gtp)

        super().sendGTPCMsg(raw(gtp), GGSN.GTP_C_IP, GGSN.GTP_C_PORT)

    def sendGTPU(self, payload):
        gtp = GTP_U_Header()/Raw()
        gtp.gtp_type = 255
        gtp.seq = self.getGTPUSeq()
        gtp.teid = self.ggsn_teid_d

        gtp.load = payload

        gtp.show2()
        hexdump(gtp)

        super().sendGTPUMsg(raw(gtp), GGSN.GTP_U_IP, GGSN.GTP_U_PORT)

    def test(self):
        imsi = IMSI_TEST()
        imsi.IE_list[0].imsi = 208101166102614

        imsi.show2()
        hexdump(imsi)

#   def receiveAndCheck(self, imsi, msisdn, imei)
#   def sendgtpu(file_pcap)

def main():
    sgsn = SGSN()
    ggsn = GGSN()

    payload = IP()
    sgsn.sendGTPU(raw(payload))

    sgsn.sendCreatePDPContextRequest(
        208101166102614, #IMSI
        "192.168.1.1",
        "192.168.1.2",
        33610328579, #MSISDN
        3517510449245601) #IMEI
    sgsn.test()
    ggsn.sendGTPU(raw(payload))

    # def Main()
    #    sgsn = SGSN()
    #    ggsn = GGSN()

    #    ggsn.receiveAndCheck()
    #    sgsn.sendCreatePDPContextRequest()

    #    ggsn.receivegtpu()
    #    sgsn.sendgtpu("var\gtp.pcap")


    # my code here

if __name__ == "__main__":
    main()




#bind_layers(GTPHeader, GTPCreatePDPContextRequest1, gtp_type=16)



