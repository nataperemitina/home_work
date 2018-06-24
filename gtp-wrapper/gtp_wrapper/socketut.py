import socket,sys
import fcntl

class RawSocket:
    def SendMsg(self):
        ETH_P_ALL = 3

        HOST = socket.gethostbyname(socket.gethostname())
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        print(HOST)
        s.bind(("test", ETH_P_ALL))
        print("set sockopt")
        #fcntl.ioctl(s, socket.SIO_RCVALL, socket.RCVALL_ON)
        #s.setsockopt(socket.SOL_SOCKET, 25, str("test" +'\0').encode('utf-8'))
        print("recv")
        print(s.recv(1500))
        print ("got")

class UDPSocket:
    MAX_PACKET_SIZE = 1500

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data, ip, port):
        self.socket.sendto(data, (ip, port))

    def recv(self):
        return self.socket.recvfrom(UDPSocket.MAX_PACKET_SIZE)

    def bind(self, ip, port):
        self.socket.bind((ip, port))